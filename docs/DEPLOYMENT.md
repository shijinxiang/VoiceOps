# VoiceOps 生产与本地部署指南 (Deployment Guide)

VoiceOps 支持 **Docker Compose 一键全栈容器化部署** 以及 **本地源码开发部署**。

---

## 1. 方式一：Docker Compose 一键部署（推荐）

适用于全新的 Linux 服务器（Ubuntu 22.04+、Debian 12+、CentOS 9+）或已安装 Docker Desktop 的 Windows/macOS 开发机。

### 1.1 依赖环境要求
- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **显卡 (可选)**: 若需 GPU 推理，安装 `nvidia-container-toolkit`；默认自带 CPU 回退。

### 1.2 一键克隆与启动
```bash
# 1. 克隆代码仓库
git clone https://github.com/shijinxiang/VoiceOps.git
cd VoiceOps

# 2. 一键启动全套微服务编排
docker compose up -d --build

# 3. 检查容器运行状态与健康检查
docker compose ps
```

容器组包含：
- `voiceops-frontend`: 前端控制台 (端口 **3000**)
- `voiceops-backend`: FastAPI 核心后端 (端口 **8000**)
- `voiceops-postgres`: 向量数据库 PostgreSQL 16 + pgvector (端口 **5432**)
- `voiceops-redis`: 异步任务缓存 Redis 7 (端口 **6379**)
- `voiceops-n8n`: 自动化工作流引擎 n8n (端口 **5678**)
- `voiceops-mailpit`: 本地邮件通知仿真接收器 (端口 **8025**)

### 1.3 访问服务
- **VoiceOps 售后控制台**: [http://localhost:3000](http://localhost:3000)
- **API 交互式文档 (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Mailpit 模拟邮件收件箱**: [http://localhost:8025](http://localhost:8025)
- **n8n 工作流控制台**: [http://localhost:5678](http://localhost:5678)

---

## 2. 方式二：本地极简开发环境直接启动

适合本地快速调试，无需安装庞大的 Docker 依赖。

### 2.1 后端启动
```bash
# 进入工程根目录
cd VoiceOps

# 安装 Python 依赖 (推荐 Python 3.10 - 3.13)
pip install -r backend/requirements.txt

# 启动 FastAPI 后端服务
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2.2 前端启动
```bash
cd frontend

# 安装依赖
npm install

# 启动 Vite 开发热更新服务器
npm run dev
# 访问 http://localhost:3000 即可开始调试
```

---

## 3. 持久化与数据备份恢复演练

### 3.1 备份数据
```bash
# Linux
chmod +x scripts/backup.sh
./scripts/backup.sh

# Windows PowerShell
.\scripts\backup.ps1
```

### 3.2 灾难恢复演练
```bash
# Linux
./scripts/restore.sh ./backups/20261005_120000

# Windows PowerShell
.\scripts\restore.ps1 -BackupDir .\backups\20261005_120000
```
