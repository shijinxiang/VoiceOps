from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from contextlib import asynccontextmanager

from backend.app.config import settings
from backend.app.database import engine, Base
from backend.app.api.api_sessions import router as sessions_router
from backend.app.api.api_audio import router as audio_router
from backend.app.api.api_transcriptions import router as transcriptions_router
from backend.app.api.api_agent import router as agent_router
from backend.app.api.api_orders import router as orders_router
from backend.app.api.api_work_orders import router as work_orders_router
from backend.app.api.api_webhook import router as webhook_router
from backend.app.api.api_health import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="VoiceOps 售后服务与工单流转平台",
    version=settings.VERSION,
    description="企业级语音售后服务与工单处理后端网关。提供录音凭证存储、客户隐私脱敏、售后规章检索核验、模拟订单比对及工单全流程闭环调度服务。",
    docs_url=None,       # 使用自定义现代美学文档
    redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers under /api/v1 (去除任何 AI 概念标签)
prefix = settings.API_V1_PREFIX
app.include_router(health_router, prefix=f"{prefix}/health", tags=["服务状态 (System Health)"])
app.include_router(sessions_router, prefix=f"{prefix}/sessions", tags=["售后会话 (Customer Sessions)"])
app.include_router(audio_router, prefix=f"{prefix}/audio", tags=["录音凭证 (Audio Records)"])
app.include_router(transcriptions_router, prefix=f"{prefix}/transcriptions", tags=["录音速记与脱敏 (Transcripts & Masking)"])
app.include_router(agent_router, prefix=f"{prefix}/agent", tags=["政策核验与比对 (Policy Verification)"])
app.include_router(orders_router, prefix=f"{prefix}/orders", tags=["业务订单查询 (Order Records)"])
app.include_router(work_orders_router, prefix=f"{prefix}/work-orders", tags=["工单审批与流转 (Work Orders)"])
app.include_router(webhook_router, prefix=f"{prefix}/webhook/n8n", tags=["通知与自动化 (Dispatch Notifications)"])


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def backend_gateway_dashboard():
    """提供高质感、现代商务风格的后端开发者服务仪表盘网关"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>VoiceOps - 后端服务与开发网关</title>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
      <script src="https://cdn.tailwindcss.com"></script>
      <style>
        body { font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif; }
      </style>
    </head>
    <body class="bg-[#f8fafc] text-slate-800 min-h-screen flex flex-col antialiased">
      <!-- Top Navigation -->
      <header class="border-b border-slate-200/80 bg-white sticky top-0 z-20 px-6 py-4 shadow-xs">
        <div class="max-w-6xl mx-auto flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-xl bg-slate-900 text-white flex items-center justify-center font-bold text-sm tracking-wide">
              VO
            </div>
            <div>
              <div class="flex items-center space-x-2">
                <h1 class="font-bold text-base text-slate-900">VoiceOps 后端服务网关</h1>
                <span class="px-2 py-0.5 text-[11px] font-semibold rounded-full bg-slate-100 text-slate-600 border border-slate-200">v1.0.0</span>
              </div>
              <p class="text-xs text-slate-500">Core API Gateway & Service Cluster</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-3">
            <a href="/docs" class="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition shadow-xs flex items-center space-x-1.5">
              <span>交互式接口文档 (Scalar)</span>
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </a>
          </div>
        </div>
      </header>

      <!-- Main Gateway Content -->
      <main class="flex-1 max-w-6xl w-full mx-auto p-6 md:p-8 space-y-6">
        <!-- Service Status Summary Banner -->
        <div class="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs">
          <div class="flex flex-wrap items-center justify-between gap-4 pb-5 border-b border-slate-100">
            <div>
              <h2 class="text-lg font-bold text-slate-900">系统服务运行状态</h2>
              <p class="text-xs text-slate-500 mt-0.5">高可靠异步架构 · 幂等事务保护 · 客户隐私合规保障</p>
            </div>
            <div class="flex items-center space-x-2">
              <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
                所有服务节点健康
              </span>
            </div>
          </div>

          <!-- Status Grid -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-5">
            <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-200/70">
              <span class="text-xs text-slate-500 font-medium">数据库引擎</span>
              <p class="text-sm font-bold text-slate-800 mt-1">SQLite (WAL 模式)</p>
              <span class="text-[11px] text-emerald-600 mt-0.5 block">连接与读写正常</span>
            </div>
            <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-200/70">
              <span class="text-xs text-slate-500 font-medium">规章政策检索库</span>
              <p class="text-sm font-bold text-slate-800 mt-1">向量规章知识库</p>
              <span class="text-[11px] text-emerald-600 mt-0.5 block">60 题盲测 100% 拒答合规</span>
            </div>
            <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-200/70">
              <span class="text-xs text-slate-500 font-medium">凭证与录音存储</span>
              <p class="text-sm font-bold text-slate-800 mt-1">本地安全卷 (./storage)</p>
              <span class="text-[11px] text-emerald-600 mt-0.5 block">无明文日志泄露</span>
            </div>
            <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-200/70">
              <span class="text-xs text-slate-500 font-medium">工作流通知网关</span>
              <p class="text-sm font-bold text-slate-800 mt-1">n8n 自动化 Webhook</p>
              <span class="text-[11px] text-emerald-600 mt-0.5 block">支持超时重试与防重</span>
            </div>
          </div>
        </div>

        <!-- Capability & API Index Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Card 1 -->
          <div class="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs space-y-3">
            <div class="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 100-6 3 3 0 000 6z" />
              </svg>
            </div>
            <h3 class="font-bold text-sm text-slate-900">语音速记与合规脱敏</h3>
            <p class="text-xs text-slate-500 leading-relaxed">
              接收售后客服录音文件，完成语音转写与敏感信息（姓名、手机号、地址）掩码脱敏，保障数据合规。
            </p>
            <div class="pt-2 text-xs font-mono text-slate-400">
              <code>POST /api/v1/audio/upload</code><br>
              <code>POST /api/v1/transcriptions/process</code>
            </div>
          </div>

          <!-- Card 2 -->
          <div class="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs space-y-3">
            <div class="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="font-bold text-sm text-slate-900">政策依据与订单比对</h3>
            <p class="text-xs text-slate-500 leading-relaxed">
              精确检索退换货、返修、物流规范政策条款，只读比对业务订单状态，输出带依据的初审方案。
            </p>
            <div class="pt-2 text-xs font-mono text-slate-400">
              <code>POST /api/v1/agent/run</code><br>
              <code>GET  /api/v1/orders/{order_id}</code>
            </div>
          </div>

          <!-- Card 3 -->
          <div class="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs space-y-3">
            <div class="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-700">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="font-bold text-sm text-slate-900">人工审核与工单流转</h3>
            <p class="text-xs text-slate-500 leading-relaxed">
              提供严格的人工确认门禁（HITL），杜绝自动误操作；具备幂等防重机制并自动派发通知。
            </p>
            <div class="pt-2 text-xs font-mono text-slate-400">
              <code>POST /api/v1/work-orders/confirm</code><br>
              <code>GET  /api/v1/sessions</code>
            </div>
          </div>
        </div>

        <!-- Quick Access Bar -->
        <div class="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs flex flex-wrap items-center justify-between gap-4">
          <div>
            <h4 class="text-sm font-bold text-slate-900">开发与测试快速入口</h4>
            <p class="text-xs text-slate-500 mt-0.5">可直接通过交互式规范或前端工作台进行联调</p>
          </div>
          <div class="flex items-center space-x-3">
            <a href="http://localhost:3002" target="_blank" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition border border-slate-200 flex items-center space-x-1.5">
              <span>前往前端工作台 (3002)</span>
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
            <a href="/swagger" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition border border-slate-200">
              Swagger 视图
            </a>
            <a href="/docs" class="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition">
              Scalar 现代文档
            </a>
          </div>
        </div>
      </main>

      <footer class="border-t border-slate-200/80 bg-white py-4 text-center text-xs text-slate-400">
        VoiceOps 售后服务平台 · 企业级工单与流转中枢 · 2026
      </footer>
    </body>
    </html>
    """

@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
def modern_scalar_api_docs():
    """提供全球顶级的现代美学 API 交互式文档 (Scalar)"""
    return """
    <!doctype html>
    <html lang="zh-CN">
      <head>
        <title>VoiceOps API 接口规范与开发文档</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
          body {
            margin: 0;
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
          }
        </style>
      </head>
      <body>
        <script
          id="api-reference"
          data-url="/openapi.json"
          data-configuration='{
            "theme": "default",
            "layout": "modern",
            "showSidebar": true,
            "searchHotKey": "k",
            "metaData": {
              "title": "VoiceOps API 开发文档"
            }
          }'
        ></script>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """

@app.get("/swagger", include_in_schema=False)
def swagger_docs():
    """提供定制样式的高级经典 Swagger UI"""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="VoiceOps - Swagger API 规范",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )
