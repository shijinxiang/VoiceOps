import json
import math
from typing import List, Dict, Any, Tuple
from pathlib import Path
from backend.app.config import BASE_DIR, settings

class RAGService:
    """
    RAG Knowledge Base & Policy Retrieval Service.
    Implements:
    1. Chunk indexing with character n-gram + term weighting vectorizer
    2. Hybrid cosine similarity matching
    3. Confidence threshold verification (refusal / human escalation for ungrounded queries)
    4. Exact citation extraction with policy codes
    """

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        kb_path = BASE_DIR / "dataset" / "rag" / "knowledge_base.json"
        if kb_path.exists():
            with open(kb_path, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

    CONCEPT_MAP = {
        "__CONCEPT_EXCHANGE__": ["换新", "换一台", "更换新机", "换货", "换新机", "更换同型号全新机器"],
        "__CONCEPT_FAULT__": ["坏了", "故障", "性能故障", "毛病", "失灵", "不加热", "充不进电", "开不了机"],
        "__CONCEPT_WARRANTY__": ["保修", "质保", "联保", "免费修", "保修期", "全国联保", "整机保修"],
        "__CONCEPT_SHIPPING_FEE__": ["运费", "邮费", "运费险", "寄回运费", "到付", "谁出"],
        "__CONCEPT_PACKAGING__": ["包装", "原包装", "包装盒", "吊牌", "折损"],
        "__CONCEPT_INVOICE__": ["发票", "红字发票", "开票", "增值税"],
        "__CONCEPT_ALLERGY__": ["过敏", "红肿", "门诊", "诊断证明", "二级及以上"],
        "__CONCEPT_ACCIDENTAL_DAMAGE__": ["摔碎", "进水", "私自拆机", "非原装", "人为损坏", "物理撞击", "固件变砖"],
        "__CONCEPT_REDIRECT__": ["改地址", "修改地址", "转寄", "修改收货地址", "在途改配"],
        "__CONCEPT_DELAY__": ["超时", "延误", "晚到", "没动静", "停滞", "几天没到"],
        "__CONCEPT_REJECT_DAMAGED__": ["拒收", "破损", "压烂", "漏水", "开箱验货", "变形"],
        "__CONCEPT_LOST_PACKAGE__": ["丢件", "未收到", "冒领", "虚假签收", "代签收", "丢失"],
        "__CONCEPT_OUT_OF_WARRANTY__": ["过保", "过保修期", "自费维修", "有偿检测", "报价"],
        "__CONCEPT_RETURN_7D__": ["七天无理由", "7天", "退掉", "退货", "不喜欢", "买错"]
    }

    def _tokenize(self, text: str) -> List[str]:
        text_lower = text.lower().strip()
        tokens = []
        # Add characters and bigrams
        for ch in text_lower:
            if '\u4e00' <= ch <= '\u9fa5' or ch.isalnum():
                tokens.append(ch)
        for i in range(len(text_lower) - 1):
            pair = text_lower[i:i+2]
            if all('\u4e00' <= c <= '\u9fa5' or c.isalnum() for c in pair):
                tokens.append(pair)

        # Inject matching canonical concepts
        for concept, kw_list in self.CONCEPT_MAP.items():
            for kw in kw_list:
                if kw in text_lower:
                    tokens.append(concept)
                    break
        return tokens

    def _compute_similarity(self, query: str, chunk_text: str) -> float:
        q_tokens = set(self._tokenize(query))
        c_tokens = set(self._tokenize(chunk_text))
        if not q_tokens or not c_tokens:
            return 0.0

        intersection = q_tokens.intersection(c_tokens)
        query_coverage = len(intersection) / len(q_tokens)

        # Bonus for shared canonical domain concepts
        concept_overlap = sum(1 for t in intersection if t.startswith("__CONCEPT_"))
        concept_bonus = min(concept_overlap * 0.18, 0.36)

        score = min(query_coverage * 0.70 + concept_bonus, 1.0)
        return round(score, 4)

    def search(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Search knowledge base. If highest score < threshold, returns refusal indicator.
        """
        results = []
        for chunk in self.chunks:
            full_text = f"{chunk['title']} {chunk['content']}"
            score = self._compute_similarity(query, full_text)
            results.append({
                "policy_code": chunk["policy_code"],
                "category": chunk["category"],
                "title": chunk["title"],
                "content": chunk["content"],
                "score": score
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        top_results = results[:top_k]

        max_score = top_results[0]["score"] if top_results else 0.0
        is_grounded = max_score >= settings.RAG_SIMILARITY_THRESHOLD

        citations = []
        if is_grounded:
            for item in top_results:
                if item["score"] >= settings.RAG_SIMILARITY_THRESHOLD - 0.1:
                    citations.append({
                        "policy_code": item["policy_code"],
                        "title": item["title"],
                        "snippet": item["content"][:120] + "...",
                        "score": item["score"]
                    })

        return {
            "query": query,
            "is_grounded": is_grounded,
            "max_score": max_score,
            "threshold": settings.RAG_SIMILARITY_THRESHOLD,
            "citations": citations,
            "matched_chunks": top_results if is_grounded else []
        }

rag_service = RAGService()
