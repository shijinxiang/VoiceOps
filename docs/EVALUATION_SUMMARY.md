# VoiceOps 全阶段评测与复现总览报告 (Evaluation Master Summary)

本报告汇总了 VoiceOps 项目各阶段的审核指标、通过标准、实测数据与复现指南。所有评测数据均严格列出分子、分母、数据版本与硬件环境。

---

## 1. 评测硬件与基础配置

| 项 | 配置参数 |
|---|---|
| **操作系统** | Windows 11 64-bit / Linux Ubuntu 22.04 LTS (Docker) |
| **GPU / 算力** | NVIDIA GeForce RTX 4060 Laptop (8GB VRAM) / CUDA 12.x |
| **CPU / 内存** | AMD Ryzen 7 8845H (16 vCPU) / 32 GB RAM |
| **基础语言与环境** | Python 3.12, Node.js 20, Docker 26.x |
| **基础大模型** | Qwen/Qwen2.5-7B-Instruct (4-bit GPTQ / Int4 Quantized) |
| **ASR 模型** | Faster-Whisper Small / Base (Chinese) |
| **向量检索库** | pgvector (PostgreSQL 16) / SQLite WAL 本地缓存 |

---

## 2. 核心指标总览看板

```
========================================================================================
阶段 (周期)      考核核心指标                  通过门槛           实测结果         判定
----------------------------------------------------------------------------------------
第 1 周 技术验证   异常场景覆盖数               ≥ 10/10           10/10 (100%)    通过
第 4 周 语音脱敏   清晰组 CER                  ≤ 15.0%           0.53%           通过
                 噪声组 CER                  ≤ 30.0%           2.59%           通过
                 异常文件拦截率               10/10 (100%)      10/10 (100%)    通过
                 未脱敏日志外泄数             0                 0 (严格合规)     通过
第 5-6 周 知识RAG 盲测有依据正确率             ≥ 36/45 (80%)     37/45 (82.2%)   通过
                 盲测无依据拒答率             ≥ 14/15 (93.3%)   15/15 (100%)    通过
                 出处引用支撑率               ≥ 90.0%           90.2%           通过
第 7 周 Agent工单 30 复杂场景回放成功率         ≥ 29/30 (96.7%)   30/30 (100%)    通过
                 未人工确认违规建单数         0                 0 (严格HITL)    通过
                 并发/重复请求导致重复工单     0                 0 (幂等保护)     通过
                 工具调用轨迹完整留存率       100%              30/30 (100%)    通过
第 8 周 n8n 编排  正常通知投递成功率           100%              10/10 (100%)    通过
                 网络超时注入重试成功率       100%              10/10 (100%)    通过
                 重复 Webhook 防重拦截率      100%              10/10 (100%)    通过
第 9 周 前端闭环   E2E 端到端操作脚本通过率     12/12 (100%)      12/12 (100%)    通过
                 桌面与移动端布局自适应       无阻断缺陷        全部适配         通过
第 10 周 MVP部署  5 并发 API 请求错误率        < 1.0%            0.0% (0/30)     通过
                 P95 请求延迟                ≤ 6000 ms         491 ms          通过
                 任务丢失数与重复工单数       0                 0 / 0           通过
                 灾备热备份与冷恢复测试       数据 100% 恢复    校验成功         通过
第 11 周 微调实验  Base 模型意图提取准确率       对照组            66.7% (40/60)   完成
                 Few-Shot CoT 准确率         技术路线对比      88.3% (53/60)   完成
                 QLoRA 领域适配微调准确率     技术路线对比      93.3% (56/60)   完成
                 微调 JSON 格式合规率         -                 98.3% (59/60)   完成
========================================================================================
```

---

## 3. 一键复现测试指令指南

在项目根目录下，运行以下指令可随时复现各模块评测结果：

### 3.1 基础接口与环境校验
```bash
python scripts/verify_tech_baseline.py
pytest tests/test_api_baseline.py -v
```

### 3.2 第 4 周：ASR 转写与脱敏评测 (CER)
```bash
python evaluations/eval_cer.py
# 报告输出于: docs/evaluations/WEEK4_ASR_REPORT.md
```

### 3.3 第 5–6 周：知识库与 RAG 盲测 (60 题)
```bash
python evaluations/eval_rag.py
# 报告输出于: docs/evaluations/WEEK5_6_RAG_REPORT.md
```

### 3.4 第 7 周：Agent 与工单 30 场景回放
```bash
python evaluations/eval_agent.py
# 报告输出于: docs/evaluations/WEEK7_AGENT_REPORT.md
```

### 3.5 第 8 周：n8n 自动化与超时容灾演练
```bash
python evaluations/eval_n8n.py
# 报告输出于: docs/evaluations/WEEK8_N8N_REPORT.md
```

### 3.6 第 9 周：前端 12 条 E2E 交互测试
```bash
python evaluations/eval_frontend_e2e.py
# 报告输出于: docs/evaluations/WEEK9_FRONTEND_REPORT.md
```

### 3.7 第 10 周：高并发压测与备份恢复
```bash
# 并发性能测试 (5 并发 workers)
python evaluations/benchmark_load.py

# 备份与恢复脚本演练 (PowerShell 或 Linux Bash)
powershell -ExecutionPolicy Bypass -File scripts/backup.ps1
powershell -ExecutionPolicy Bypass -File scripts/restore.ps1 backups/backup_voiceops_*.tar.gz
```

### 3.8 第 11 周：Prompt vs QLoRA 微调评测 (60 题隔离测试集)
```bash
python evaluations/eval_prompt_vs_finetune.py
# 报告输出于: docs/evaluations/WEEK11_FINETUNE_REPORT.md
```

---

## 4. 详细评测分项归档目录

- [第 1 周 技术验证报告](specs/WEEK1_VERIFICATION_REPORT.md)
- [第 4 周 语音脱敏 CER 报告](evaluations/WEEK4_ASR_REPORT.md)
- [第 5–6 周 知识库与 RAG 盲测报告](evaluations/WEEK5_6_RAG_REPORT.md)
- [第 7 周 Agent 场景回放报告](evaluations/WEEK7_AGENT_REPORT.md)
- [第 8 周 n8n 自动化与重试报告](evaluations/WEEK8_N8N_REPORT.md)
- [第 9 周 前端端到端闭环报告](evaluations/WEEK9_FRONTEND_REPORT.md)
- [第 10 周 MVP 并发压测与容灾报告](evaluations/WEEK10_MVP_DEPLOY_REPORT.md)
- [第 11 周 提示词与 QLoRA 实验报告](evaluations/WEEK11_FINETUNE_REPORT.md)
