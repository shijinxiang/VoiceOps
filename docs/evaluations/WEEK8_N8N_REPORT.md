# VoiceOps 第 8 周 n8n 工作流自动化与容错评测报告 (Week 8 n8n Evaluation Report)

- **评测时间**: 2026-10-05
- **工作流文件**: `n8n/workflows/voiceops_workorder_notification.json`
- **通知仿真服务**: Mailpit (端口 8025/1025)
- **评测内容**: 正常建单通知与状态回写、人为超时/网络异常重试、重复 Webhook 幂等性校验

---

## 1. 核心指标汇总与通过标准判定

| 考核项 | 目标考核通过标准 | 实测结果 | 最终判定 |
|---|---|---|---|
| **正常流程通知与回写** | 100% 成功回写工单状态 | 全部通知并回写成功 (状态: SYNCED_N8N) | **PASS** |
| **失败异常与重试可见性** | 具备可见失败态并可重试 | 标记为 NOTIFICATION_FAILED，记录错误原因 | **PASS** |
| **重复 Webhook 幂等防护** | 0 重复建单，无失控重复通知 | 幂等状态机吸收重复回调，单号与状态稳定 | **PASS** |

---

## 2. 异常注入与容错测试明细表

| 序号 | 测试场景 | 注入条件 | 预期终态 | 实际结果 | 判定 |
|---|---|---|---|---|---|
| 1 | 正常流程触发与状态回写 | 工单确认后触发 Webhook 并收到成功回调 | 工单状态变为 SYNCED_N8N，通知记录已留存 | 工单状态: SYNCED_N8N | PASS |
| 2 | 人为注入超时与通知失败 | SMTP 服务器离线或网络 504 超时 | 工单状态标记为可见的 NOTIFICATION_FAILED 并支持人工重试 | 工单状态: NOTIFICATION_FAILED | PASS |
| 3 | 重复 Webhook 幂等防护 | 下游网络抖动导致相同 Webhook 重发两次 | 状态保持幂等，不重复建单且不产生非预期状态混乱 | 两次调用状态均稳定为: SYNCED_N8N | PASS |

---

## 3. n8n 工作流架构说明
1. **Webhook 节点**: 监听 `/webhook/voiceops-workorder`，严格校验请求体 `ticket_number` 与 `ticket_type`。
2. **多路路由分发**: 依据工单类型 (`RETURN`, `REPAIR`, `LOGISTICS_EXPEDITE`) 路由至不同通知模板。
3. **邮件发送 (Mailpit)**: 投递至本地邮件测试服务，方便在无公网邮箱凭证的环境下 100% 验证与审查邮件内容。
4. **状态回写闭环**: 通过 HTTP Request 节点调用 `/api/v1/webhook/n8n/callback` 回写工单状态。

---

## 4. 阶段验收结论
- [x] 正常流程全部通知成功
- [x] 失败有可见状态且可重试
- [x] 重复 Webhook 不重复建单或发送不可控的重复通知
- **审核结论**: **第 8 周 n8n 自动化阶段全部通过！**
