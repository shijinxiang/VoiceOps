import re
import time
from typing import Dict, Any, List, Optional
from backend.app.services.rag_service import rag_service
from backend.app.services.order_service import order_service
from backend.app.services.masking_service import masking_service

class AgentService:
    """
    After-Sales Reasoning Agent.
    Orchestrates Intent Router, RAG Retrieval, Order Lookup,
    and Draft Proposal Generation with Full Trace Auditing.
    """

    INTENT_KEYWORDS = {
        "RETURN": ["退货", "退款", "不想要", "买错", "换码", "退回", "过敏", "拒收退"],
        "REPAIR": ["维修", "换新", "保修", "送修", "寄修", "坏了", "故障", "不加热", "充不进电", "碎屏", "异响", "变砖", "连击"],
        "LOGISTICS": ["快递", "物流", "派送", "顺丰", "运单", "催单", "改地址", "延误", "签收", "丰巢", "自提柜", "少件", "破损"]
    }

    SECURITY_PROMPT_INJECTION_PATTERNS = [
        re.compile(r'ignore\s+previous\s+instructions', re.IGNORECASE),
        re.compile(r'print\s+database\s+password', re.IGNORECASE),
        re.compile(r'管理员.*命令.*越权.*退款', re.IGNORECASE),
        re.compile(r'数据库账号.*客户信息', re.IGNORECASE),
        re.compile(r'shutdown\s+-s', re.IGNORECASE)
    ]

    def check_security_violation(self, text: str) -> bool:
        for pattern in self.SECURITY_PROMPT_INJECTION_PATTERNS:
            if pattern.search(text):
                return True
        return False

    def classify_intent(self, text: str) -> str:
        if self.check_security_violation(text):
            return "OUT_OF_SCOPE"

        scores = {"RETURN": 0, "REPAIR": 0, "LOGISTICS": 0}
        for intent, kw_list in self.INTENT_KEYWORDS.items():
            for kw in kw_list:
                if kw in text:
                    scores[intent] += 1

        best_intent = max(scores, key=scores.get)
        if scores[best_intent] == 0:
            return "OUT_OF_SCOPE"
        return best_intent

    def extract_order_id(self, text: str) -> Optional[str]:
        # Match formats like ORD-20261001-8848 or ORD202610018848
        match = re.search(r'ORD[-\s]?\d{8}[-\s]?\d{4}', text, re.IGNORECASE)
        if match:
            raw = match.group(0).upper().replace(" ", "")
            if "-" not in raw:
                # Format to standard ORD-YYYYMMDD-XXXX
                return f"ORD-{raw[3:11]}-{raw[11:]}"
            return raw
        return None

    async def analyze_and_draft(self, customer_text: str, session_id: str) -> Dict[str, Any]:
        """
        Run multi-step agent reasoning pipeline with trace recording.
        """
        traces: List[Dict[str, Any]] = []
        step_idx = 1

        # Step 1: Security & Intent Classification
        t0 = time.perf_counter()
        is_attack = self.check_security_violation(customer_text)
        if is_attack:
            latency = int((time.perf_counter() - t0) * 1000)
            trace = {
                "step_index": step_idx,
                "action_type": "security_check",
                "input_payload": {"text": masking_service.mask_text(customer_text)},
                "output_payload": {"threat_detected": True, "action": "BLOCKED"},
                "latency_ms": latency
            }
            traces.append(trace)
            return {
                "intent": "OUT_OF_SCOPE",
                "is_attack": True,
                "proposal": "检测到安全策略违规或恶意指令，系统已阻断执行并记录审计日志。",
                "ticket_type": "SECURITY_ALERT",
                "order_id": None,
                "citations": [],
                "requires_human_confirm": False,
                "suggested_status": "REFUSED_SECURITY_ALERT",
                "traces": traces
            }

        intent = self.classify_intent(customer_text)
        latency = int((time.perf_counter() - t0) * 1000)
        traces.append({
            "step_index": step_idx,
            "action_type": "intent_classification",
            "input_payload": {"text": masking_service.mask_text(customer_text)},
            "output_payload": {"intent": intent},
            "latency_ms": latency
        })
        step_idx += 1

        # Step 2: Order Lookup
        t0 = time.perf_counter()
        order_id = self.extract_order_id(customer_text)
        order_data = None
        if order_id:
            order_data = order_service.get_order(order_id)
        
        latency = int((time.perf_counter() - t0) * 1000)
        traces.append({
            "step_index": step_idx,
            "action_type": "order_lookup",
            "input_payload": {"extracted_order_id": order_id},
            "output_payload": {
                "found": order_data is not None, 
                "order": masking_service.sanitize_for_audit_log(order_data) if order_data else None
            },
            "latency_ms": latency
        })
        step_idx += 1

        # Step 3: RAG Retrieval
        t0 = time.perf_counter()
        rag_res = rag_service.search(customer_text, top_k=2)
        latency = int((time.perf_counter() - t0) * 1000)
        traces.append({
            "step_index": step_idx,
            "action_type": "rag_retrieval",
            "input_payload": {"query": masking_service.mask_text(customer_text)},
            "output_payload": {
                "is_grounded": rag_res["is_grounded"],
                "max_score": rag_res["max_score"],
                "citation_codes": [c["policy_code"] for c in rag_res["citations"]]
            },
            "latency_ms": latency
        })
        step_idx += 1

        # Step 4: Decision & Draft Formulation
        t0 = time.perf_counter()
        proposal = ""
        ticket_type = intent
        requires_human = True
        suggested_status = "PENDING_CONFIRMATION"

        if intent == "OUT_OF_SCOPE" or not rag_res["is_grounded"]:
            proposal = "很抱歉，此问题超出常规售后支持范围或无明确政策依据。建议转接资深人工客服处理。"
            ticket_type = "OUT_OF_SCOPE"
            requires_human = False
            suggested_status = "REFUSED_OUT_OF_SCOPE"
        elif order_id and not order_data:
            proposal = f"客户提及订单号 {order_id}，但在系统中未检索到对应记录。请坐席核实订单号真实性。"
            ticket_type = "INVALID_ORDER"
            requires_human = False
            suggested_status = "REJECTED_ORDER_NOT_FOUND"
        elif "摔碎" in customer_text or "进水" in customer_text or "拆开" in customer_text:
            proposal = "经检测分析，故障属于进水/物理碎裂/私自拆机等非保修范围，依据政策 REP-002 提供有偿寄修更换方案。"
            ticket_type = "REPAIR"
            suggested_status = "PAID_REPAIR_PROPOSAL"
        elif intent == "RETURN":
            if "过敏" in customer_text:
                proposal = "客户反馈过敏反应，依据特殊政策 RET-004 凭二级及以上公立医院诊断证明申请全额退款，品牌方承担运费。"
            else:
                proposal = "符合售后退货标准，依据 RET-001/RET-002 审核商品完好度后安排顺丰寄回退款。"
        elif intent == "REPAIR":
            proposal = "硬件功能故障，签收仍在保修期内，依据 REP-001/REP-003 提供双向顺丰到付免费寄修或换新服务。"
        elif intent == "LOGISTICS":
            proposal = "针对物流诉求，依据 LOG-001/LOG-002/LOG-004 登记物流异常工单，已核查物流状态并协同承运商跟进。"
            ticket_type = "LOGISTICS_EXPEDITE"

        latency = int((time.perf_counter() - t0) * 1000)
        traces.append({
            "step_index": step_idx,
            "action_type": "ticket_generation",
            "input_payload": {"intent": intent, "has_order": order_data is not None},
            "output_payload": {"ticket_type": ticket_type, "proposal": proposal},
            "latency_ms": latency
        })

        return {
            "intent": intent,
            "is_attack": False,
            "proposal": proposal,
            "ticket_type": ticket_type,
            "order_id": order_id,
            "order_data": order_data,
            "citations": rag_res["citations"],
            "requires_human_confirm": requires_human,
            "suggested_status": suggested_status,
            "traces": traces
        }

agent_service = AgentService()
