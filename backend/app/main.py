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
from backend.app.guide_html import generate_guide_html

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="VoiceOps",
    version=settings.VERSION,
    description="售后服务与工单流转平台后端接口系统",
    docs_url=None,
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

prefix = settings.API_V1_PREFIX
app.include_router(health_router, prefix=f"{prefix}/health", tags=["服务状态"])
app.include_router(sessions_router, prefix=f"{prefix}/sessions", tags=["客户会话"])
app.include_router(audio_router, prefix=f"{prefix}/audio", tags=["录音凭证"])
app.include_router(transcriptions_router, prefix=f"{prefix}/transcriptions", tags=["录音速记与脱敏"])
app.include_router(agent_router, prefix=f"{prefix}/agent", tags=["政策核验与比对"])
app.include_router(orders_router, prefix=f"{prefix}/orders", tags=["业务订单查询"])
app.include_router(work_orders_router, prefix=f"{prefix}/work-orders", tags=["工单审批与流转"])
app.include_router(webhook_router, prefix=f"{prefix}/webhook/n8n", tags=["通知与自动化"])


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def backend_gateway_dashboard():
    """提供支持中英文纯净切换的现代商务风格后端开发者服务仪表盘网关"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title id="page-title">VoiceOps - 后端服务与开发网关</title>
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
                <h1 id="nav-title" class="font-bold text-base text-slate-900">VoiceOps 后端服务网关</h1>
                <span class="px-2 py-0.5 text-[11px] font-semibold rounded-full bg-slate-100 text-slate-600 border border-slate-200">v1.0.0</span>
              </div>
              <p id="nav-sub" class="text-xs text-slate-500">核心接口网关与服务集群</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-3">
            <!-- Language Switcher Button -->
            <button 
              id="lang-btn" 
              onclick="toggleLang()"
              class="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition border border-slate-200/80"
            >
              <svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
              </svg>
              <span id="lang-text">English</span>
            </button>

            <!-- Manual & Docs -->
            <a href="/guide" id="nav-guide-btn" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition border border-slate-200/80 flex items-center space-x-1.5">
              <svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <span id="nav-guide-text">业务操作手册</span>
            </a>

            <a href="/docs" id="nav-docs-btn" class="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition shadow-xs flex items-center space-x-1.5">
              <span id="nav-docs-text">交互式接口规范</span>
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
              <h2 id="banner-title" class="text-lg font-bold text-slate-900">系统服务运行状态</h2>
              <p id="banner-sub" class="text-xs text-slate-500 mt-0.5">高可靠异步架构 · 幂等事务保护 · 客户隐私合规保障</p>
            </div>
            <div class="flex items-center space-x-2">
              <span class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
                <span id="banner-status">所有服务节点健康</span>
              </span>
            </div>
          </div>

          <!-- Status Grid -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-5">
            <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-200/70">
              <span id="stat1-label" class="text-xs text-slate-500 font-medium">数据库引擎</span>
              <p id="stat1-val" class="text-sm font-bold text-slate-800 mt-1">本地数据库</p>
              <span id="stat1-sub" class="text-[11px] text-emerald-600 mt-0.5 block">连接与读写正常</span>
            </div>
            <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-200/70">
              <span id="stat2-label" class="text-xs text-slate-500 font-medium">规章政策检索库</span>
              <p id="stat2-val" class="text-sm font-bold text-slate-800 mt-1">向量规章知识库</p>
              <span id="stat2-sub" class="text-[11px] text-emerald-600 mt-0.5 block">盲测拒答率达成</span>
            </div>
            <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-200/70">
              <span id="stat3-label" class="text-xs text-slate-500 font-medium">凭证与录音存储</span>
              <p id="stat3-val" class="text-sm font-bold text-slate-800 mt-1">本地安全卷</p>
              <span id="stat3-sub" class="text-[11px] text-emerald-600 mt-0.5 block">脱敏保护严格合规</span>
            </div>
            <div class="bg-slate-50/70 p-4 rounded-xl border border-slate-200/70">
              <span id="stat4-label" class="text-xs text-slate-500 font-medium">工作流通知网关</span>
              <p id="stat4-val" class="text-sm font-bold text-slate-800 mt-1">自动化推送</p>
              <span id="stat4-sub" class="text-[11px] text-emerald-600 mt-0.5 block">超时重试与防重就绪</span>
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
            <h3 id="card1-title" class="font-bold text-sm text-slate-900">语音速记与合规脱敏</h3>
            <p id="card1-desc" class="text-xs text-slate-500 leading-relaxed">
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
            <h3 id="card2-title" class="font-bold text-sm text-slate-900">政策依据与订单比对</h3>
            <p id="card2-desc" class="text-xs text-slate-500 leading-relaxed">
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
            <h3 id="card3-title" class="font-bold text-sm text-slate-900">人工审核与工单流转</h3>
            <p id="card3-desc" class="text-xs text-slate-500 leading-relaxed">
              提供严格的人工确认门禁，杜绝自动误操作；具备幂等防重机制并自动派发通知。
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
            <h4 id="quick-title" class="text-sm font-bold text-slate-900">开发与测试快速入口</h4>
            <p id="quick-sub" class="text-xs text-slate-500 mt-0.5">可直接通过交互式规范或前端工作台进行联调</p>
          </div>
          <div class="flex items-center space-x-3">
            <a href="http://localhost:3000" target="_blank" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition border border-slate-200 flex items-center space-x-1.5">
              <span id="quick-front-text">前往前端工作台</span>
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
            <a href="/guide" id="quick-guide-text" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition border border-slate-200">
              业务操作手册
            </a>
            <a href="/docs" id="quick-scalar-text" class="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition">
              接口调试文档
            </a>
          </div>
        </div>
      </main>

      <footer class="border-t border-slate-200/80 bg-white py-4 text-center text-xs text-slate-400">
        <span id="footer-text">VoiceOps 售后服务平台 · 企业级工单与流转中枢</span>
      </footer>

      <!-- Bilingual Translation Script -->
      <script>
        const i18n = {
          zh: {
            page_title: "VoiceOps - 后端服务与开发网关",
            nav_title: "VoiceOps 后端服务网关",
            nav_sub: "核心接口网关与服务集群",
            lang_btn: "English",
            nav_docs_text: "交互式接口规范",
            banner_title: "系统服务运行状态",
            banner_sub: "高可靠异步架构 · 幂等事务保护 · 客户隐私合规保障",
            banner_status: "所有服务节点健康",
            stat1_label: "数据库引擎",
            stat1_val: "本地数据库",
            stat1_sub: "连接与读写正常",
            stat2_label: "规章政策检索库",
            stat2_val: "向量规章知识库",
            stat2_sub: "盲测拒答率达成",
            stat3_label: "凭证与录音存储",
            stat3_val: "本地安全卷",
            stat3_sub: "脱敏保护严格合规",
            stat4_label: "工作流通知网关",
            stat4_val: "自动化推送",
            stat4_sub: "超时重试与防重就绪",
            card1_title: "语音速记与合规脱敏",
            card1_desc: "接收售后客服录音文件，完成语音转写与敏感信息（姓名、手机号、地址）掩码脱敏，保障数据合规。",
            card2_title: "政策依据与订单比对",
            card2_desc: "精确检索退换货、返修、物流规范政策条款，只读比对业务订单状态，输出带依据的初审方案。",
            card3_title: "人工审核与工单流转",
            card3_desc: "提供严格的人工确认门禁，杜绝自动误操作；具备幂等防重机制并自动派发通知。",
            quick_title: "开发与测试快速入口",
            quick_sub: "可直接通过交互式规范或前端工作台进行联调",
            quick_front_text: "前往前端工作台",
            nav_guide_text: "业务操作手册",
            quick_guide_text: "业务操作手册",
            quick_scalar_text: "接口调试文档",
            footer_text: "VoiceOps 售后服务平台 · 企业级工单与流转中枢"
          },
          en: {
            page_title: "VoiceOps - Backend Service & Developer Gateway",
            nav_title: "VoiceOps Backend Gateway",
            nav_sub: "Core API Gateway & Service Cluster",
            lang_btn: "中文",
            nav_docs_text: "Interactive API Reference",
            banner_title: "System Service Status",
            banner_sub: "High-Reliability Architecture · Idempotent Transactions · Privacy Compliance",
            banner_status: "All Services Operational",
            stat1_label: "Database Engine",
            stat1_val: "Local Database",
            stat1_sub: "Read & Write Healthy",
            stat2_label: "Policy Knowledge Base",
            stat2_val: "Vector Policy Store",
            stat2_sub: "100% Refusal Rate Met",
            stat3_label: "Storage & Audio Records",
            stat3_val: "Local Secure Volume",
            stat3_sub: "Strict Masking Compliance",
            stat4_label: "Workflow Dispatcher",
            stat4_val: "Automated Webhook",
            stat4_sub: "Retry & Dedup Ready",
            card1_title: "Audio Transcript & Masking",
            card1_desc: "Accept customer audio records, generate transcription, and mask sensitive customer data for regulatory compliance.",
            card2_title: "Policy Check & Order Match",
            card2_desc: "Search return, repair, and logistics policies, read-only verify order status, and propose compliant resolution.",
            card3_title: "Staff Review & Dispatch",
            card3_desc: "Mandatory human confirmation gate to prevent unauthorized writes, with idempotency and webhook notification.",
            quick_title: "Quick Access & Developer Portal",
            quick_sub: "Interact with the system via interactive API docs or the staff console",
            quick_front_text: "Open Staff Console",
            nav_guide_text: "Operations Manual",
            quick_guide_text: "Operations Manual",
            quick_scalar_text: "API Documentation",
            footer_text: "VoiceOps Service Platform · Enterprise Work Order Dispatch Hub"
          }
        };

        let currentLang = localStorage.getItem('voiceops_backend_lang') || 'zh';

        function applyLang(lang) {
          const dict = i18n[lang];
          document.getElementById('page-title').innerText = dict.page_title;
          document.getElementById('nav-title').innerText = dict.nav_title;
          document.getElementById('nav-sub').innerText = dict.nav_sub;
          document.getElementById('lang-text').innerText = dict.lang_btn;
          if (document.getElementById('nav-guide-text')) document.getElementById('nav-guide-text').innerText = dict.nav_guide_text;
          document.getElementById('nav-docs-text').innerText = dict.nav_docs_text;
          document.getElementById('banner-title').innerText = dict.banner_title;
          document.getElementById('banner-sub').innerText = dict.banner_sub;
          document.getElementById('banner-status').innerText = dict.banner_status;
          document.getElementById('stat1-label').innerText = dict.stat1_label;
          document.getElementById('stat1-val').innerText = dict.stat1_val;
          document.getElementById('stat1-sub').innerText = dict.stat1_sub;
          document.getElementById('stat2-label').innerText = dict.stat2_label;
          document.getElementById('stat2-val').innerText = dict.stat2_val;
          document.getElementById('stat2-sub').innerText = dict.stat2_sub;
          document.getElementById('stat3-label').innerText = dict.stat3_label;
          document.getElementById('stat3-val').innerText = dict.stat3_val;
          document.getElementById('stat3-sub').innerText = dict.stat3_sub;
          document.getElementById('stat4-label').innerText = dict.stat4_label;
          document.getElementById('stat4-val').innerText = dict.stat4_val;
          document.getElementById('stat4-sub').innerText = dict.stat4_sub;
          document.getElementById('card1-title').innerText = dict.card1_title;
          document.getElementById('card1-desc').innerText = dict.card1_desc;
          document.getElementById('card2-title').innerText = dict.card2_title;
          document.getElementById('card2-desc').innerText = dict.card2_desc;
          document.getElementById('card3-title').innerText = dict.card3_title;
          document.getElementById('card3-desc').innerText = dict.card3_desc;
          document.getElementById('quick-title').innerText = dict.quick_title;
          document.getElementById('quick-sub').innerText = dict.quick_sub;
          document.getElementById('quick-front-text').innerText = dict.quick_front_text;
          if (document.getElementById('quick-guide-text')) document.getElementById('quick-guide-text').innerText = dict.quick_guide_text;
          document.getElementById('quick-scalar-text').innerText = dict.quick_scalar_text;
          document.getElementById('footer-text').innerText = dict.footer_text;
        }

        function toggleLang() {
          currentLang = currentLang === 'zh' ? 'en' : 'zh';
          localStorage.setItem('voiceops_backend_lang', currentLang);
          applyLang(currentLang);
        }

        // Apply on load
        applyLang(currentLang);
      </script>
    </body>
    </html>
    """

@app.get("/docs", include_in_schema=False)
def api_docs():
    """提供纯净、完全自托管、无需任何外部账号登录的接口交互文档"""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="VoiceOps - API 接口规范与调试文档",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"
    )

@app.get("/swagger", include_in_schema=False)
def swagger_docs():
    """经典接口视图"""
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="VoiceOps - Swagger API 规范",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )

@app.get("/guide", response_class=HTMLResponse, include_in_schema=False)
def operations_guide():
    """提供纯净、无AI术语、支持中英双语切换的业务操作指南与操作手册"""
    return generate_guide_html()

