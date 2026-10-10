# -*- coding: utf-8 -*-
"""
VoiceOps API Documentation HTML Generator
Modern Enterprise Redesign combining:
1. Heavily styled, modern luxury SaaS theme for Interactive Swagger UI (zero 2015 clutter)
2. Seamless instant toggle to Stripe-style 3-column Redoc specification view
3. Cohesive slate & ivory visual language, bilingual (ZH/EN), zero third-party AI chatbots.
"""

def generate_docs_html() -> str:
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title id="page-title">VoiceOps - API 接口规范与调试控制台</title>
  <link rel="icon" type="image/png" href="/static/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS for Navigation and Shell -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Swagger UI Core Assets -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>

  <!-- Redoc Assets -->
  <script src="https://cdn.jsdelivr.net/npm/redoc@latest/bundles/redoc.standalone.js"></script>

  <style>
    body {
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #f8fafc;
      color: #1e293b;
    }
    .font-mono-code {
      font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
    }

    /* ==========================================================================
       VoiceOps Modern Swagger UI Theme Overrides
       Transforming raw 2015 Swagger UI into a 2026 Executive SaaS Console
       ========================================================================== */

    /* Hide ugly default topbar */
    .swagger-ui .topbar {
      display: none !important;
    }

    .swagger-ui {
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
      color: #1e293b !important;
    }

    #swagger-ui-container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 24px 20px 80px 20px;
    }

    /* Swagger Main Information Card */
    .swagger-ui .information-container {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 16px !important;
      padding: 28px 32px !important;
      margin-bottom: 24px !important;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03) !important;
    }
    .swagger-ui .info {
      margin: 0 !important;
    }
    .swagger-ui .info .title {
      font-size: 22px !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      letter-spacing: -0.02em !important;
      display: flex !important;
      align-items: center !important;
      gap: 12px !important;
    }
    .swagger-ui .info .title small {
      background: #f1f5f9 !important;
      border: 1px solid #e2e8f0 !important;
      color: #475569 !important;
      padding: 2px 10px !important;
      border-radius: 9999px !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      top: 0 !important;
      vertical-align: middle !important;
    }
    .swagger-ui .info .title small.version-stamp {
      background: #f1f5f9 !important;
    }
    .swagger-ui .info .description {
      font-size: 13px !important;
      color: #64748b !important;
      line-height: 1.6 !important;
      margin-top: 10px !important;
    }
    .swagger-ui .info .description p {
      margin: 4px 0 !important;
    }
    .swagger-ui .info .base-url {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 12px !important;
      color: #475569 !important;
      background: #f8fafc !important;
      border: 1px solid #e2e8f0 !important;
      padding: 4px 10px !important;
      border-radius: 6px !important;
      display: inline-block !important;
      margin-top: 8px !important;
    }

    /* Scheme & Server Select Box */
    .swagger-ui .scheme-container {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 12px !important;
      padding: 14px 24px !important;
      margin-bottom: 24px !important;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
    }

    /* Tag Section Groups */
    .swagger-ui .opblock-tag-section {
      margin-bottom: 28px !important;
    }
    .swagger-ui .opblock-tag {
      font-size: 16px !important;
      font-weight: 700 !important;
      color: #0f172a !important;
      border-bottom: 1px solid #e2e8f0 !important;
      padding: 12px 2px !important;
      margin-bottom: 14px !important;
      display: flex !important;
      align-items: center !important;
    }
    .swagger-ui .opblock-tag small {
      font-size: 12px !important;
      color: #64748b !important;
      font-weight: 500 !important;
      margin-left: 10px !important;
    }

    /* ==========================================
       Operation Block Card Redesign (The Key Fix)
       ========================================== */
    .swagger-ui .opblock {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 12px !important;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
      margin: 0 0 10px 0 !important;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
      overflow: hidden !important;
    }
    .swagger-ui .opblock:hover {
      border-color: #cbd5e1 !important;
      box-shadow: 0 4px 10px -2px rgba(0, 0, 0, 0.04) !important;
    }
    .swagger-ui .opblock .opblock-summary {
      padding: 11px 18px !important;
      border-bottom: none !important;
      display: flex !important;
      align-items: center !important;
      background: transparent !important;
    }

    /* Modern HTTP Method Badges */
    .swagger-ui .opblock .opblock-summary-method {
      border-radius: 6px !important;
      font-size: 11px !important;
      font-weight: 800 !important;
      min-width: 66px !important;
      text-align: center !important;
      padding: 4px 8px !important;
      font-family: 'JetBrains Mono', monospace !important;
      letter-spacing: 0.04em !important;
      text-shadow: none !important;
      border: none !important;
    }

    /* GET (Emerald) */
    .swagger-ui .opblock.opblock-get {
      border-left: 4px solid #10b981 !important;
      background: #ffffff !important;
    }
    .swagger-ui .opblock.opblock-get .opblock-summary-method {
      background: #10b981 !important;
      color: #ffffff !important;
    }

    /* POST (Indigo) */
    .swagger-ui .opblock.opblock-post {
      border-left: 4px solid #6366f1 !important;
      background: #ffffff !important;
    }
    .swagger-ui .opblock.opblock-post .opblock-summary-method {
      background: #6366f1 !important;
      color: #ffffff !important;
    }

    /* PUT (Amber) */
    .swagger-ui .opblock.opblock-put {
      border-left: 4px solid #f59e0b !important;
      background: #ffffff !important;
    }
    .swagger-ui .opblock.opblock-put .opblock-summary-method {
      background: #f59e0b !important;
      color: #ffffff !important;
    }

    /* DELETE (Rose) */
    .swagger-ui .opblock.opblock-delete {
      border-left: 4px solid #f43f5e !important;
      background: #ffffff !important;
    }
    .swagger-ui .opblock.opblock-delete .opblock-summary-method {
      background: #f43f5e !important;
      color: #ffffff !important;
    }

    /* Path & Descriptions */
    .swagger-ui .opblock .opblock-summary-path {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 13px !important;
      font-weight: 600 !important;
      color: #0f172a !important;
      padding-left: 12px !important;
    }
    .swagger-ui .opblock .opblock-summary-path__deprecated {
      text-decoration: line-through !important;
      color: #94a3b8 !important;
    }
    .swagger-ui .opblock .opblock-summary-description {
      font-size: 12px !important;
      color: #64748b !important;
      font-weight: 500 !important;
      margin-left: 12px !important;
    }

    /* Opblock Expanded Details */
    .swagger-ui .opblock-body {
      background: #f8fafc !important;
      border-top: 1px solid #f1f5f9 !important;
      padding: 24px 28px !important;
    }
    .swagger-ui .opblock .opblock-section-header {
      background: transparent !important;
      box-shadow: none !important;
      padding: 8px 0 !important;
    }
    .swagger-ui .opblock .opblock-section-header h4 {
      font-size: 12px !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.05em !important;
      color: #475569 !important;
    }

    /* Parameters Table */
    .swagger-ui table.parameters {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 8px !important;
      overflow: hidden !important;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
    }
    .swagger-ui table.parameters thead th {
      background: #f8fafc !important;
      color: #475569 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.05em !important;
      border-bottom: 1px solid #e2e8f0 !important;
      padding: 10px 14px !important;
    }
    .swagger-ui table.parameters tbody tr td {
      padding: 12px 14px !important;
      border-bottom: 1px solid #f1f5f9 !important;
    }
    .swagger-ui .parameters-col_name {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 12px !important;
      color: #0f172a !important;
      font-weight: 600 !important;
    }
    .swagger-ui .parameters-col_description {
      font-size: 12px !important;
      color: #475569 !important;
    }
    .swagger-ui .parameter__name.required:after {
      color: #f43f5e !important;
    }

    /* Form Controls & Inputs */
    .swagger-ui input[type=text],
    .swagger-ui textarea,
    .swagger-ui select {
      background: #ffffff !important;
      border: 1px solid #cbd5e1 !important;
      border-radius: 6px !important;
      padding: 7px 12px !important;
      font-size: 12px !important;
      font-family: 'JetBrains Mono', monospace !important;
      color: #1e293b !important;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
      outline: none !important;
      transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    .swagger-ui input[type=text]:focus,
    .swagger-ui textarea:focus,
    .swagger-ui select:focus {
      border-color: #64748b !important;
      box-shadow: 0 0 0 2px #e2e8f0 !important;
    }

    /* Modern Buttons */
    .swagger-ui .btn {
      border-radius: 6px !important;
      font-size: 12px !important;
      font-weight: 600 !important;
      box-shadow: none !important;
      transition: all 0.15s ease !important;
      text-shadow: none !important;
    }
    .swagger-ui .btn.try-out__btn {
      background: #ffffff !important;
      border: 1px solid #cbd5e1 !important;
      color: #334155 !important;
      padding: 5px 14px !important;
      font-weight: 600 !important;
    }
    .swagger-ui .btn.try-out__btn:hover {
      background: #f1f5f9 !important;
      border-color: #94a3b8 !important;
    }
    .swagger-ui .btn.execute {
      background: #0f172a !important;
      border: 1px solid #0f172a !important;
      color: #ffffff !important;
      padding: 7px 24px !important;
      font-weight: 600 !important;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }
    .swagger-ui .btn.execute:hover {
      background: #1e293b !important;
    }
    .swagger-ui .btn.cancel {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      color: #64748b !important;
      padding: 5px 14px !important;
    }
    .swagger-ui .btn.cancel:hover {
      background: #f1f5f9 !important;
    }

    /* Response & Results Section */
    .swagger-ui .responses-wrapper {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 8px !important;
      overflow: hidden !important;
      margin-top: 14px !important;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02) !important;
    }
    .swagger-ui .responses-table {
      background: transparent !important;
    }
    .swagger-ui .responses-table thead th {
      background: #f8fafc !important;
      color: #475569 !important;
      font-size: 11px !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      letter-spacing: 0.05em !important;
      border-bottom: 1px solid #e2e8f0 !important;
      padding: 10px 14px !important;
    }
    .swagger-ui .response-col_status {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 13px !important;
      font-weight: 700 !important;
    }
    .swagger-ui .response__status--200,
    .swagger-ui .response__status--201 {
      color: #10b981 !important;
    }
    .swagger-ui .response__status--400,
    .swagger-ui .response__status--422,
    .swagger-ui .response__status--500 {
      color: #f43f5e !important;
    }

    /* Code Blocks */
    .swagger-ui .highlight-code,
    .swagger-ui .microlight {
      background: #0f172a !important;
      color: #f1f5f9 !important;
      border-radius: 8px !important;
      padding: 16px !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 12px !important;
      line-height: 1.5 !important;
      border: 1px solid #1e293b !important;
    }

    /* Models / Schemas Card */
    .swagger-ui section.models {
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 16px !important;
      padding: 24px 28px !important;
      margin-top: 36px !important;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.03) !important;
    }
    .swagger-ui section.models h4 {
      font-size: 15px !important;
      font-weight: 700 !important;
      color: #0f172a !important;
      border-bottom: 1px solid #e2e8f0 !important;
      padding-bottom: 12px !important;
    }
    .swagger-ui .model-box {
      background: #f8fafc !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 8px !important;
      padding: 10px 14px !important;
      margin-top: 8px !important;
    }

    /* Hide Swagger Watermark / Footer */
    .swagger-ui .wrapper {
      padding: 0 !important;
    }
    .swagger-ui .info a {
      color: #4f46e5 !important;
      text-decoration: none !important;
    }
    .swagger-ui .info a:hover {
      text-decoration: underline !important;
    }

    /* Redoc custom overrides */
    #redoc-container {
      background: #ffffff;
      min-height: calc(100vh - 120px);
    }
    .redoc-wrap {
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased">

  <!-- Top Enterprise Navigation Bar -->
  <header class="border-b border-slate-200/80 bg-white sticky top-0 z-40 px-6 py-3.5 shadow-xs">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      
      <!-- Left Brand & Title -->
      <div class="flex items-center space-x-3">
        <img src="/static/logo.png" alt="VoiceOps Logo" class="w-8 h-8 rounded-lg shadow-xs object-cover" />
        <div class="flex items-center space-x-2.5">
          <h1 class="font-bold text-base text-slate-900 tracking-tight" id="nav-brand-title">VoiceOps API 规范文档</h1>
          <span class="px-2 py-0.5 text-[11px] font-semibold rounded-full bg-slate-100 text-slate-600 border border-slate-200">
            OpenAPI 3.1
          </span>
        </div>
      </div>

      <!-- Center View Switcher (Interactive vs 3-Column Document) -->
      <div class="hidden sm:flex items-center p-1 bg-slate-100 rounded-xl border border-slate-200/80">
        <button 
          id="btn-mode-interactive" 
          onclick="switchMode('interactive')"
          class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition bg-white text-slate-900 shadow-xs"
        >
          <svg class="w-3.5 h-3.5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <span id="tab-interactive-text">交互调试视图</span>
        </button>
        <button 
          id="btn-mode-redoc" 
          onclick="switchMode('redoc')"
          class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:text-slate-900 transition"
        >
          <svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span id="tab-redoc-text">规整三栏文档</span>
        </button>
      </div>

      <!-- Right Navigation Actions -->
      <div class="flex items-center space-x-3">
        <!-- Workbench -->
        <a 
          href="http://localhost:3000" 
          target="_blank"
          class="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition shadow-xs"
        >
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          <span id="nav-btn-wb">售后工作台</span>
        </a>

        <!-- Operations Manual -->
        <a 
          href="/guide" 
          target="_blank"
          class="hidden md:flex items-center space-x-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-lg transition border border-slate-200/80"
        >
          <svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <span id="nav-btn-manual">操作手册</span>
        </a>

        <!-- Language Switcher -->
        <button 
          id="lang-btn" 
          onclick="toggleDocsLang()"
          class="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition border border-slate-200/80"
        >
          <svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
          </svg>
          <span id="lang-btn-text">English</span>
        </button>
      </div>

    </div>
  </header>

  <!-- Subheader Overview Bar -->
  <div class="border-b border-slate-200/80 bg-white/70 backdrop-blur px-6 py-2.5">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between text-xs text-slate-500 gap-2">
      <div class="flex items-center space-x-3">
        <span class="inline-flex items-center text-emerald-700 font-medium">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5"></span>
          <span id="sub-status-text">服务在线 · 支持在线交互调试与数据模拟</span>
        </span>
        <span class="text-slate-300">|</span>
        <span class="font-mono-code text-slate-600">Base URL: /api/v1</span>
      </div>
      <div class="flex items-center space-x-3">
        <span id="sub-mode-hint" class="text-slate-400">自托管安全无登录 · 支持切换三栏文档模式</span>
      </div>
    </div>
  </div>

  <!-- Main View Container -->
  <main class="flex-1 w-full">
    <!-- View 1: Swagger UI Modern Interactive View -->
    <div id="swagger-ui-container"></div>

    <!-- View 2: Redoc 3-Column Clean Document View -->
    <div id="redoc-container" style="display: none;"></div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-200/80 bg-white py-4 text-center text-xs text-slate-400">
    <span id="footer-text">VoiceOps 售后服务平台 · API 接口规范与调试控制台 · 企业级高可用服务</span>
  </footer>

  <script>
    // --- View Mode Management ---
    let currentMode = localStorage.getItem('voiceops_api_view_mode') || 'interactive';
    let redocInitialized = false;

    function switchMode(mode) {
      currentMode = mode;
      localStorage.setItem('voiceops_api_view_mode', mode);

      const swaggerEl = document.getElementById('swagger-ui-container');
      const redocEl = document.getElementById('redoc-container');
      const btnInteractive = document.getElementById('btn-mode-interactive');
      const btnRedoc = document.getElementById('btn-mode-redoc');

      if (mode === 'interactive') {
        swaggerEl.style.display = 'block';
        redocEl.style.display = 'none';

        btnInteractive.className = 'flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition bg-white text-slate-900 shadow-xs';
        btnRedoc.className = 'flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:text-slate-900 transition';
      } else {
        swaggerEl.style.display = 'none';
        redocEl.style.display = 'block';

        btnRedoc.className = 'flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition bg-white text-slate-900 shadow-xs';
        btnInteractive.className = 'flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:text-slate-900 transition';

        if (!redocInitialized) {
          initRedoc();
          redocInitialized = true;
        }
      }
    }

    // --- Initialize Swagger UI ---
    window.addEventListener('load', () => {
      SwaggerUIBundle({
        url: '/openapi.json',
        dom_id: '#swagger-ui-container',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis
        ],
        layout: 'BaseLayout',
        docExpansion: 'list',
        defaultModelRendering: 'example',
        showExtensions: true,
        showCommonExtensions: true,
        displayRequestDuration: true
      });

      if (currentMode === 'redoc') {
        switchMode('redoc');
      }
    });

    // --- Initialize Redoc ---
    function initRedoc() {
      Redoc.init('/openapi.json', {
        theme: {
          colors: {
            primary: {
              main: '#0f172a'
            },
            success: {
              main: '#10b981'
            },
            warning: {
              main: '#f59e0b'
            },
            error: {
              main: '#f43f5e'
            },
            text: {
              primary: '#1e293b',
              secondary: '#64748b'
            },
            http: {
              get: '#10b981',
              post: '#6366f1',
              put: '#f59e0b',
              delete: '#f43f5e'
            }
          },
          typography: {
            fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif",
            fontSize: '13px',
            lineHeight: '1.6',
            headings: {
              fontFamily: "'Plus Jakarta Sans', system-ui, sans-serif",
              fontWeight: '700'
            },
            code: {
              fontFamily: "'JetBrains Mono', Consolas, monospace",
              fontSize: '12px'
            }
          },
          sidebar: {
            backgroundColor: '#f8fafc',
            textColor: '#334155',
            activeTextColor: '#0f172a'
          },
          rightPanel: {
            backgroundColor: '#0f172a',
            width: '42%'
          }
        },
        hideDownloadButton: false,
        disableSearch: false
      }, document.getElementById('redoc-container'));
    }

    // --- Bilingual Translation Logic ---
    const docsI18n = {
      zh: {
        page_title: "VoiceOps - API 接口规范与调试控制台",
        nav_brand_title: "VoiceOps API 规范文档",
        tab_interactive_text: "交互调试视图",
        tab_redoc_text: "规整三栏文档",
        nav_btn_wb: "售后工作台",
        nav_btn_manual: "操作手册",
        lang_btn_text: "English",
        sub_status_text: "服务在线 · 支持在线交互调试与数据模拟",
        sub_mode_hint: "自托管安全无登录 · 支持切换三栏文档模式",
        footer_text: "VoiceOps 售后服务平台 · API 接口规范与调试控制台 · 企业级高可用服务"
      },
      en: {
        page_title: "VoiceOps - API Specification & Debug Console",
        nav_brand_title: "VoiceOps API Reference",
        tab_interactive_text: "Interactive Console",
        tab_redoc_text: "3-Column Docs",
        nav_btn_wb: "Workbench",
        nav_btn_manual: "Manual",
        lang_btn_text: "中文",
        sub_status_text: "Service Online · Interactive testing & simulation enabled",
        sub_mode_hint: "Self-hosted & login-free · Switch between console and documentation",
        footer_text: "VoiceOps Platform · API Specifications & Interactive Console"
      }
    };

    let docLang = localStorage.getItem('voiceops_docs_lang') || localStorage.getItem('voiceops_lang') || 'zh';

    function applyDocsLang(lang) {
      const dict = docsI18n[lang] || docsI18n.zh;
      for (const [key, val] of Object.entries(dict)) {
        const el = document.getElementById(key.replace(/_/g, '-'));
        if (el) el.innerText = val;
      }
      document.title = dict.page_title;
      document.getElementById('lang-btn-text').innerText = lang === 'zh' ? 'English' : '中文';
    }

    function toggleDocsLang() {
      docLang = docLang === 'zh' ? 'en' : 'zh';
      localStorage.setItem('voiceops_docs_lang', docLang);
      localStorage.setItem('voiceops_lang', docLang);
      applyDocsLang(docLang);
    }

    applyDocsLang(docLang);
  </script>
</body>
</html>
"""
