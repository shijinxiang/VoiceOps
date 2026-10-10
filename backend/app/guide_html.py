# -*- coding: utf-8 -*-
"""
VoiceOps Operations Manual and User Guide HTML Generator
Enterprise minimalist design with ivory/slate palette, bilingual (ZH/EN) support,
and zero AI buzzwords.
"""

def generate_guide_html() -> str:
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title id="doc-title">VoiceOps - 业务使用指南与操作手册</title>
  <link rel="icon" type="image/png" href="/static/logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body { font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif; }
    html { scroll-behavior: smooth; }
  </style>
</head>
<body class="bg-[#f8fafc] text-slate-800 min-h-screen flex flex-col antialiased">
  <!-- Top Navigation Bar -->
  <header class="border-b border-slate-200/80 bg-white sticky top-0 z-40 px-6 py-3.5 shadow-xs">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <!-- Brand & Title -->
      <div class="flex items-center space-x-3">
        <img src="/static/logo.png" alt="VoiceOps Logo" class="w-8 h-8 rounded-lg shadow-xs object-cover" />
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="font-bold text-base text-slate-900 tracking-tight" id="nav-brand-title">VoiceOps 操作手册</h1>
            <span class="px-2 py-0.5 text-[11px] font-medium rounded-full bg-slate-100 text-slate-600 border border-slate-200/80" id="nav-badge">业务规程与操作规范</span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center space-x-3">
        <!-- Workbench Link -->
        <a 
          href="http://localhost:3000" 
          target="_blank"
          class="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg transition shadow-xs"
        >
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          <span id="nav-btn-workbench">返回工作台</span>
        </a>

        <!-- API Reference -->
        <a 
          href="/docs" 
          target="_blank"
          class="hidden sm:flex items-center space-x-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-lg transition border border-slate-200/80"
        >
          <svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span id="nav-btn-docs">接口文档</span>
        </a>

        <!-- Language Toggle -->
        <button 
          id="lang-btn" 
          onclick="toggleDocLang()"
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

  <!-- Main Content Layout -->
  <div class="flex-1 max-w-7xl w-full mx-auto px-6 py-8 flex flex-col md:flex-row gap-8">
    <!-- Left Sticky Sidebar TOC -->
    <aside class="md:w-64 shrink-0">
      <div class="sticky top-20 bg-white border border-slate-200/80 rounded-2xl p-5 shadow-xs space-y-4">
        <h3 class="font-bold text-xs uppercase tracking-wider text-slate-400" id="toc-header">目录导航</h3>
        <nav class="space-y-1.5 text-xs font-medium text-slate-600">
          <a href="#section-overview" class="block px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition" id="toc-overview">1. 业务概述与支持场景</a>
          <a href="#section-audio" class="block px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition" id="toc-audio">2. 录音导入与音频规范</a>
          <a href="#section-privacy" class="block px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition" id="toc-privacy">3. 隐私脱敏速记规则</a>
          <a href="#section-policy" class="block px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition" id="toc-policy">4. 政策规章与单据核验</a>
          <a href="#section-review" class="block px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition" id="toc-review">5. 坐席审核与防重建单</a>
          <a href="#section-audit" class="block px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition" id="toc-audit">6. 自动化通知与全链路审计</a>
          <a href="#section-faq" class="block px-3 py-2 rounded-lg hover:bg-slate-100 hover:text-slate-900 transition" id="toc-faq">7. 常见问题与操作指引</a>
        </nav>
      </div>
    </aside>

    <!-- Right Main Articles -->
    <main class="flex-1 min-w-0 space-y-8">
      
      <!-- Top Banner Summary -->
      <section class="bg-white border border-slate-200/80 rounded-2xl p-6 md:p-8 shadow-xs">
        <div class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 mb-3">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5"></span>
          <span id="banner-tag">生产系统业务规程</span>
        </div>
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight" id="banner-title">VoiceOps 售后服务平台操作手册</h2>
        <p class="text-sm text-slate-600 mt-2 leading-relaxed" id="banner-desc">
          本手册为 VoiceOps 售后服务质检与工单流转系统的全业务操作规范。涵盖录音音频导入、客户隐私合规脱敏、规章条款自动检索、关联单据比对、坐席强制人工复核门禁与防重事务建单机制。
        </p>
      </section>

      <!-- Section 1: 业务概述与支持场景 -->
      <section id="section-overview" class="bg-white border border-slate-200/80 rounded-2xl p-6 md:p-8 shadow-xs space-y-4">
        <div class="flex items-center space-x-3 pb-3 border-b border-slate-100">
          <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-xs">01</div>
          <h3 class="text-lg font-bold text-slate-900" id="sec1-title">业务概述与支持场景</h3>
        </div>
        <p class="text-sm text-slate-600 leading-relaxed" id="sec1-p1">
          VoiceOps 专注于大型电商与品牌制造企业的售后服务智能化流转，严格对标国家三包法规与企业内部规章，标准化覆盖以下三大核心业务类型：
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          <div class="bg-slate-50/80 p-4 rounded-xl border border-slate-200/70 space-y-2">
            <span class="inline-block px-2 py-0.5 rounded text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200" id="sec1-tag1">七天无理由退货</span>
            <h4 class="font-bold text-sm text-slate-800" id="sec1-t1">退货与退款</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec1-d1">
              签收之日起 7 个自然日内提出。要求商品未激活、原包装配件完好且防伪标识未拆毁。非质量问题由客户自行承担寄回运费。
            </p>
          </div>
          <div class="bg-slate-50/80 p-4 rounded-xl border border-slate-200/70 space-y-2">
            <span class="inline-block px-2 py-0.5 rounded text-[11px] font-semibold bg-amber-50 text-amber-700 border border-amber-200" id="sec1-tag2">法定三包保修</span>
            <h4 class="font-bold text-sm text-slate-800" id="sec1-t2">性能故障与维修</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec1-d2">
              法定 1 年质保期内，因产品自身硬件缺陷导致的性能故障（如断电、花屏、充不进电）。需由售后服务中心开具专业检测单后执行换新或免费寄修。
            </p>
          </div>
          <div class="bg-slate-50/80 p-4 rounded-xl border border-slate-200/70 space-y-2">
            <span class="inline-block px-2 py-0.5 rounded text-[11px] font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200" id="sec1-tag3">物流在途协同</span>
            <h4 class="font-bold text-sm text-slate-800" id="sec1-t3">物流催查与异常</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec1-d3">
              针对物流节点停滞超 48 小时、包裹破损拒收或在途丢失异常，系统协同承运商发起优先催派或先行补发机制。
            </p>
          </div>
        </div>
      </section>

      <!-- Section 2: 录音导入与音频规范 -->
      <section id="section-audio" class="bg-white border border-slate-200/80 rounded-2xl p-6 md:p-8 shadow-xs space-y-4">
        <div class="flex items-center space-x-3 pb-3 border-b border-slate-100">
          <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-xs">02</div>
          <h3 class="text-lg font-bold text-slate-900" id="sec2-title">录音导入与音频规范</h3>
        </div>
        <p class="text-sm text-slate-600 leading-relaxed" id="sec2-p1">
          录音文件是售后事实复核与争议判定的原始凭据。系统提供高可用音频上传网关，执行前端校验与服务端完整性验证。
        </p>
        <div class="space-y-3 pt-1">
          <div class="flex items-start space-x-3 p-3 bg-slate-50/80 rounded-xl border border-slate-200/70 text-xs text-slate-700">
            <span class="font-bold text-slate-900 shrink-0" id="sec2-item1-lbl">格式要求:</span>
            <span id="sec2-item1-val">支持标准通话录音格式 WAV、MP3、M4A、FLAC 等。推荐采样率 16kHz 及以上单/双声道。</span>
          </div>
          <div class="flex items-start space-x-3 p-3 bg-slate-50/80 rounded-xl border border-slate-200/70 text-xs text-slate-700">
            <span class="font-bold text-slate-900 shrink-0" id="sec2-item2-lbl">容量限制:</span>
            <span id="sec2-item2-val">单次录音文件推荐在 20MB 以内，通话时长建议在 15 分钟以内。超大音频建议进行分段上传。</span>
          </div>
          <div class="flex items-start space-x-3 p-3 bg-slate-50/80 rounded-xl border border-slate-200/70 text-xs text-slate-700">
            <span class="font-bold text-slate-900 shrink-0" id="sec2-item3-lbl">操作流程:</span>
            <span id="sec2-item3-val">在控制台录音卡片点击上传或将文件直接拖入上传区域，系统即刻校验并生成文件大小、时长及音频播放组件，随后即可点击“生成速记”。</span>
          </div>
        </div>
      </section>

      <!-- Section 3: 隐私脱敏与速记规则 -->
      <section id="section-privacy" class="bg-white border border-slate-200/80 rounded-2xl p-6 md:p-8 shadow-xs space-y-4">
        <div class="flex items-center space-x-3 pb-3 border-b border-slate-100">
          <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-xs">03</div>
          <h3 class="text-lg font-bold text-slate-900" id="sec3-title">隐私脱敏与速记规则</h3>
        </div>
        <p class="text-sm text-slate-600 leading-relaxed" id="sec3-p1">
          为严格遵从《中华人民共和国个人信息保护法》(PIPL) 与企业数据安全审计，系统在转写音频的同时，由后端脱敏引擎执行强规则隐私脱敏：
        </p>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border border-slate-200 rounded-lg overflow-hidden">
            <thead class="bg-slate-100 text-slate-700 font-semibold">
              <tr>
                <th class="p-3 border-b border-slate-200" id="sec3-th1">敏感数据类型</th>
                <th class="p-3 border-b border-slate-200" id="sec3-th2">脱敏脱敏规则</th>
                <th class="p-3 border-b border-slate-200" id="sec3-th3">原始示例</th>
                <th class="p-3 border-b border-slate-200" id="sec3-th4">合规脱敏呈现</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-slate-600">
              <tr>
                <td class="p-3 font-medium text-slate-800" id="sec3-r1-c1">手机号码</td>
                <td class="p-3" id="sec3-r1-c2">保留前 3 位和后 4 位，中间 4 位星号替换</td>
                <td class="p-3 font-mono">13812345678</td>
                <td class="p-3 font-mono text-emerald-700 font-semibold">138****5678</td>
              </tr>
              <tr>
                <td class="p-3 font-medium text-slate-800" id="sec3-r2-c1">真实姓名</td>
                <td class="p-3" id="sec3-r2-c2">保留首位姓氏，名字全部以星号隐蔽</td>
                <td class="p-3 font-mono">张三丰</td>
                <td class="p-3 font-mono text-emerald-700 font-semibold">张**</td>
              </tr>
              <tr>
                <td class="p-3 font-medium text-slate-800" id="sec3-r3-c1">身份证/银行卡</td>
                <td class="p-3" id="sec3-r3-c2">首尾截断脱敏，核心数字强掩码遮蔽</td>
                <td class="p-3 font-mono">310101199001011234</td>
                <td class="p-3 font-mono text-emerald-700 font-semibold">3101**********1234</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="p-3.5 bg-blue-50/70 border border-blue-200/80 rounded-xl text-xs text-blue-900 leading-relaxed">
          <strong id="sec3-tip-lbl">坐席人工校对功能：</strong>
          <span id="sec3-tip-val">由于通话中可能存在客户方言发音、杂音干扰或专业术语，坐席可随时点击“坐席校对”手动修改错别字或调整语句，保存后作为后续判据的唯一基准事实。</span>
        </div>
      </section>

      <!-- Section 4: 政策检索与单据核验 -->
      <section id="section-policy" class="bg-white border border-slate-200/80 rounded-2xl p-6 md:p-8 shadow-xs space-y-4">
        <div class="flex items-center space-x-3 pb-3 border-b border-slate-100">
          <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-xs">04</div>
          <h3 class="text-lg font-bold text-slate-900" id="sec4-title">政策检索与单据核验</h3>
        </div>
        <p class="text-sm text-slate-600 leading-relaxed" id="sec4-p1">
          本环节旨在为坐席提供清晰客观的法律规章与中台订单事实依据，杜绝主观臆断：
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 bg-slate-50/80 rounded-xl border border-slate-200/70 space-y-2">
            <h4 class="font-bold text-sm text-slate-900 flex items-center space-x-1.5" id="sec4-col1-t">
              <span>规章政策知识库匹配</span>
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec4-col1-d">
              系统对速记事实进行条款检索，列出匹配的正式规章名称与详细条例，并标注匹配度（如 92%）。若诉求超出标准规程，系统直接拒绝强行归类并提醒人工专案判定，彻底杜绝虚假幻觉。
            </p>
          </div>
          <div class="p-4 bg-slate-50/80 rounded-xl border border-slate-200/70 space-y-2">
            <h4 class="font-bold text-sm text-slate-900 flex items-center space-x-1.5" id="sec4-col2-t">
              <span>业务订单只读核验</span>
            </h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec4-col2-d">
              联动订单中台只读接口，从录音提取订单编号（如 ORD-2026-8891），真实呈现商品信息、实付金额、购买下单时间与物流承运商状态，帮助坐席核对诉求真实性。
            </p>
          </div>
        </div>
      </section>

      <!-- Section 5: 坐席审核与防重建单 -->
      <section id="section-review" class="bg-white border border-slate-200/80 rounded-2xl p-6 md:p-8 shadow-xs space-y-4">
        <div class="flex items-center space-x-3 pb-3 border-b border-slate-100">
          <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-xs">05</div>
          <h3 class="text-lg font-bold text-slate-900" id="sec5-title">坐席审核与防重建单</h3>
        </div>
        <p class="text-sm text-slate-600 leading-relaxed" id="sec5-p1">
          VoiceOps 坚持严格的企业级安全与管理责任制，实施以下两大约束原则：
        </p>
        <div class="space-y-3">
          <div class="p-4 bg-amber-50/60 border border-amber-200/80 rounded-xl space-y-1.5">
            <h4 class="font-bold text-xs text-amber-900 uppercase tracking-wide" id="sec5-h1">原则一：强制人工复核门禁 (Human-in-the-Loop)</h4>
            <p class="text-xs text-amber-800 leading-relaxed" id="sec5-d1">
              严禁系统自动创建工单。系统推荐的初审处置结论仅供坐席参考，最终处置结论必须由持证坐席人工核准，坐席可在线修改结论文字后点击“审核通过，正式建单”。
            </p>
          </div>
          <div class="p-4 bg-slate-50/80 border border-slate-200/70 rounded-xl space-y-1.5">
            <h4 class="font-bold text-xs text-slate-900 uppercase tracking-wide" id="sec5-h2">原则二：防重事务幂等机制 (Idempotency Protection)</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec5-d2">
              建单请求携带唯一的防重幂等标识。防止由于网络抖动、浏览器重复点击造成的多次建单事故。一旦建单完成，系统生成永久不可篡改的“工单流转凭证”（包含工单号、审核坐席、处置结论与时间戳）。
            </p>
          </div>
        </div>
      </section>

      <!-- Section 6: 自动化通知与全链路审计 -->
      <section id="section-audit" class="bg-white border border-slate-200/80 rounded-2xl p-6 md:p-8 shadow-xs space-y-4">
        <div class="flex items-center space-x-3 pb-3 border-b border-slate-100">
          <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-xs">06</div>
          <h3 class="text-lg font-bold text-slate-900" id="sec6-title">自动化通知与全链路审计</h3>
        </div>
        <p class="text-sm text-slate-600 leading-relaxed" id="sec6-p1">
          工单审核成功后，系统即刻触发下游自动化流转，并建立完整的质检审计流水：
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 bg-slate-50/80 rounded-xl border border-slate-200/70 space-y-2">
            <h4 class="font-bold text-sm text-slate-900" id="sec6-c1-t">下游自动化流转推送</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec6-c1-d">
              通过内部事件网关或 n8n Webhook，将工单数据即时下发至售后仓储系统、物流催派系统与财务打款流水，并向客户手机推送办理进度。
            </p>
          </div>
          <div class="p-4 bg-slate-50/80 rounded-xl border border-slate-200/70 space-y-2">
            <h4 class="font-bold text-sm text-slate-900" id="sec6-c2-t">全链路操作流水审计</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec6-c2-d">
              工作台底部流转流水卡片完整记录“语音转写 → 隐私脱敏 → 规章检索 → 订单比对 → 工单派发”五个关键节点的执行耗时 (ms) 及完整入参回执，确保质检复查全程可溯。
            </p>
          </div>
        </div>
      </section>

      <!-- Section 7: 常见问题与操作指引 -->
      <section id="section-faq" class="bg-white border border-slate-200/80 rounded-2xl p-6 md:p-8 shadow-xs space-y-4">
        <div class="flex items-center space-x-3 pb-3 border-b border-slate-100">
          <div class="w-7 h-7 rounded-lg bg-slate-900 text-white flex items-center justify-center font-bold text-xs">07</div>
          <h3 class="text-lg font-bold text-slate-900" id="sec7-title">常见问题与操作指引</h3>
        </div>
        <div class="space-y-3 pt-1">
          <div class="p-4 bg-slate-50/80 rounded-xl border border-slate-200/70 space-y-1">
            <h4 class="font-bold text-xs text-slate-900" id="sec7-q1">Q: 已经审核建单的会话还能再次修改吗？</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec7-a1">
              答：不能。为保障财务与业务审计安全，一旦正式审核建单，会话进入结单保护状态。坐席点击已结单会话可完整查阅工单号、审核凭证及初审结论，如需补充说明需在 ERP 中发起关联工单。
            </p>
          </div>
          <div class="p-4 bg-slate-50/80 rounded-xl border border-slate-200/70 space-y-1">
            <h4 class="font-bold text-xs text-slate-900" id="sec7-q2">Q: 如何在左侧列表只查看等待处理的会话？</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec7-a2">
              答：工作台左侧提供了【全部】、【待审核】、【已结单】快捷筛选标签，点击【待审核】标签即可过滤出尚未建单的所有会话，亦可在搜索框输入客户电话或编号进行精确检索。
            </p>
          </div>
          <div class="p-4 bg-slate-50/80 rounded-xl border border-slate-200/70 space-y-1">
            <h4 class="font-bold text-xs text-slate-900" id="sec7-q3">Q: 提示“未检索到完全匹配的规章条款”时该如何处理？</h4>
            <p class="text-xs text-slate-600 leading-relaxed" id="sec7-a3">
              答：这代表客户诉求属于特殊个案或超出标准退换货维修政策。此时坐席应根据企业特殊审批权限或线下沟通结果，在“工单审核”卡片中手动填写处置结论后确认建单。
            </p>
          </div>
        </div>
      </section>

    </main>
  </div>

  <!-- Footer -->
  <footer class="border-t border-slate-200/80 bg-white py-6 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-3">
      <span id="footer-copy">VoiceOps 售后服务平台 · 企业级工单与流转操作手册</span>
      <div class="flex items-center space-x-4">
        <a href="http://localhost:3000" class="hover:text-slate-800 transition" id="footer-wb">售后工作台</a>
        <a href="/docs" class="hover:text-slate-800 transition" id="footer-api">API 规范</a>
        <a href="#doc-title" class="hover:text-slate-800 transition" id="footer-top">回到顶部 ↑</a>
      </div>
    </div>
  </footer>

  <!-- Bilingual Dictionary & Logic -->
  <script>
    const guideI18n = {
      zh: {
        doc_title: "VoiceOps - 业务使用指南与操作手册",
        nav_brand_title: "VoiceOps 操作手册",
        nav_badge: "业务规程与操作规范",
        nav_btn_workbench: "返回工作台",
        nav_btn_docs: "接口文档",
        lang_btn_text: "English",
        toc_header: "目录导航",
        toc_overview: "1. 业务概述与支持场景",
        toc_audio: "2. 录音导入与音频规范",
        toc_privacy: "3. 隐私脱敏速记规则",
        toc_policy: "4. 政策规章与单据核验",
        toc_review: "5. 坐席审核与防重建单",
        toc_audit: "6. 自动化通知与全链路审计",
        toc_faq: "7. 常见问题与操作指引",
        banner_tag: "生产系统业务规程",
        banner_title: "VoiceOps 售后服务平台操作手册",
        banner_desc: "本手册为 VoiceOps 售后服务质检与工单流转系统的全业务操作规范。涵盖录音音频导入、客户隐私合规脱敏、规章条款自动检索、关联单据比对、坐席强制人工复核门禁与防重事务建单机制。",
        sec1_title: "业务概述与支持场景",
        sec1_p1: "VoiceOps 专注于大型电商与品牌制造企业的售后服务智能化流转，严格对标国家三包法规与企业内部规章，标准化覆盖以下三大核心业务类型：",
        sec1_tag1: "七天无理由退货",
        sec1_t1: "退货与退款",
        sec1_d1: "签收之日起 7 个自然日内提出。要求商品未激活、原包装配件完好且防伪标识未拆毁。非质量问题由客户自行承担寄回运费。",
        sec1_tag2: "法定三包保修",
        sec1_t2: "性能故障与维修",
        sec1_d2: "法定 1 年质保期内，因产品自身硬件缺陷导致的性能故障（如断电、花屏、充不进电）。需由售后服务中心开具专业检测单后执行换新或免费寄修。",
        sec1_tag3: "物流在途协同",
        sec1_t3: "物流催查与异常",
        sec1_d3: "针对物流节点停滞超 48 小时、包裹破损拒收或在途丢失异常，系统协同承运商发起优先催派或先行补发机制。",
        sec2_title: "录音导入与音频规范",
        sec2_p1: "录音文件是售后事实复核与争议判定的原始凭据。系统提供高可用音频上传网关，执行前端校验与服务端完整性验证。",
        sec2_item1_lbl: "格式要求:",
        sec2_item1_val: "支持标准通话录音格式 WAV、MP3、M4A、FLAC 等。推荐采样率 16kHz 及以上单/双声道。",
        sec2_item2_lbl: "容量限制:",
        sec2_item2_val: "单次录音文件推荐在 20MB 以内，通话时长建议在 15 分钟以内。超大音频建议进行分段上传。",
        sec2_item3_lbl: "操作流程:",
        sec2_item3_val: "在控制台录音卡片点击上传或将文件直接拖入上传区域，系统即刻校验并生成文件大小、时长及音频播放组件，随后即可点击“生成速记”。",
        sec3_title: "隐私脱敏与速记规则",
        sec3_p1: "为严格遵从《中华人民共和国个人信息保护法》(PIPL) 与企业数据安全审计，系统在转写音频的同时，由后端脱敏引擎执行强规则隐私脱敏：",
        sec3_th1: "敏感数据类型",
        sec3_th2: "脱敏规则",
        sec3_th3: "原始示例",
        sec3_th4: "合规脱敏呈现",
        sec3_r1_c1: "手机号码",
        sec3_r1_c2: "保留前 3 位和后 4 位，中间 4 位星号替换",
        sec3_r2_c1: "真实姓名",
        sec3_r2_c2: "保留首位姓氏，名字全部以星号隐蔽",
        sec3_r3_c1: "身份证/银行卡",
        sec3_r3_c2: "首尾截断脱敏，核心数字强掩码遮蔽",
        sec3_tip_lbl: "坐席人工校对功能：",
        sec3_tip_val: "由于通话中可能存在客户方言发音、杂音干扰或专业术语，坐席可随时点击“坐席校对”手动修改错别字或调整语句，保存后作为后续判据的唯一基准事实。",
        sec4_title: "政策检索与单据核验",
        sec4_p1: "本环节旨在为坐席提供清晰客观的法律规章与中台订单事实依据，杜绝主观臆断：",
        sec4_col1_t: "规章政策知识库匹配",
        sec4_col1_d: "系统对速记事实进行条款检索，列出匹配的正式规章名称与详细条例，并标注匹配度（如 92%）。若诉求超出标准规程，系统直接拒绝强行归类并提醒人工专案判定，彻底杜绝虚假幻觉。",
        sec4_col2_t: "业务订单只读核验",
        sec4_col2_d: "联动订单中台只读接口，从录音提取订单编号（如 ORD-2026-8891），真实呈现商品信息、实付金额、购买下单时间与物流承运商状态，帮助坐席核对诉求真实性。",
        sec5_title: "坐席审核与防重建单",
        sec5_p1: "VoiceOps 坚持严格的企业级安全与管理责任制，实施以下两大约束原则：",
        sec5_h1: "原则一：强制人工复核门禁 (Human-in-the-Loop)",
        sec5_d1: "严禁系统自动创建工单。系统推荐的初审处置结论仅供坐席参考，最终处置结论必须由持证坐席人工核准，坐席可在线修改结论文字后点击“审核通过，正式建单”。",
        sec5_h2: "原则二：防重事务幂等机制 (Idempotency Protection)",
        sec5_d2: "建单请求携带唯一的防重幂等标识。防止由于网络抖动、浏览器重复点击造成的多次建单事故。一旦建单完成，系统生成永久不可篡改的“工单流转凭证”（包含工单号、审核坐席、处置结论与时间戳）。",
        sec6_title: "自动化通知与全链路审计",
        sec6_p1: "工单审核成功后，系统即刻触发下游自动化流转，并建立完整的质检审计流水：",
        sec6_c1_t: "下游自动化流转推送",
        sec6_c1_d: "通过内部事件网关或 n8n Webhook，将工单数据即时下发至售后仓储系统、物流催派系统与财务打款流水，并向客户手机推送办理进度。",
        sec6_c2_t: "全链路操作流水审计",
        sec6_c2_d: "工作台底部流转流水卡片完整记录“语音转写 → 隐私脱敏 → 规章检索 → 订单比对 → 工单派发”五个关键节点的执行耗时 (ms) 及完整入参回执，确保质检复查全程可溯。",
        sec7_title: "常见问题与操作指引",
        sec7_q1: "Q: 已经审核建单的会话还能再次修改吗？",
        sec7_a1: "答：不能。为保障财务与业务审计安全，一旦正式审核建单，会话进入结单保护状态。坐席点击已结单会话可完整查阅工单号、审核凭证及初审结论，如需补充说明需在 ERP 中发起关联工单。",
        sec7_q2: "Q: 如何在左侧列表只查看等待处理的会话？",
        sec7_a2: "答：工作台左侧提供了【全部】、【待审核】、【已结单】快捷筛选标签，点击【待审核】标签即可过滤出尚未建单的所有会话，亦可在搜索框输入客户电话或编号进行精确检索。",
        sec7_q3: "Q: 提示“未检索到完全匹配的规章条款”时该如何处理？",
        sec7_a3: "答：这代表客户诉求属于特殊个案或超出标准退换货维修政策。此时坐席应根据企业特殊审批权限或线下沟通结果，在“工单审核”卡片中手动填写处置结论后确认建单。",
        footer_copy: "VoiceOps 售后服务平台 · 企业级工单与流转操作手册",
        footer_wb: "售后工作台",
        footer_api: "API 规范",
        footer_top: "回到顶部 ↑"
      },
      en: {
        doc_title: "VoiceOps - Operations Manual & Guidelines",
        nav_brand_title: "VoiceOps Manual",
        nav_badge: "Operations Manual & Standards",
        nav_btn_workbench: "Open Workbench",
        nav_btn_docs: "API Reference",
        lang_btn_text: "中文",
        toc_header: "Table of Contents",
        toc_overview: "1. Overview & Scopes",
        toc_audio: "2. Audio Import & Specs",
        toc_privacy: "3. Privacy Masking & Notes",
        toc_policy: "4. Policy & Order Checks",
        toc_review: "5. Seat Approval & Gate",
        toc_audit: "6. Automation & Audit Trails",
        toc_faq: "7. FAQ & Troubleshooting",
        banner_tag: "Production Operational Guide",
        banner_title: "VoiceOps Operations Manual",
        banner_desc: "Comprehensive manual and guidelines for the VoiceOps service intelligence and work order dispatch platform, covering audio upload, PII data masking, policy matching, read-only order validation, human approval gates, and idempotent dispatch.",
        sec1_title: "Overview & Business Scopes",
        sec1_p1: "VoiceOps is designed for enterprise e-commerce and retail customer service operations, strictly aligned with consumer protection laws and internal guidelines across 3 core scenarios:",
        sec1_tag1: "7-Day Return",
        sec1_t1: "Return & Refund",
        sec1_d1: "Submitted within 7 calendar days of receipt. Product must be unactivated, original packaging intact, and anti-counterfeit seals unbroken. Return freight borne by customer unless defective.",
        sec1_tag2: "Statutory Warranty",
        sec1_t2: "Defects & Repair",
        sec1_d2: "Valid for 1 year under statutory warranty for hardware defects (power loss, display failure, battery). Authorized service center inspection report required for free replacement or repair.",
        sec1_tag3: "In-Transit Tracking",
        sec1_t3: "Logistics Inquiry",
        sec1_d3: "For packages stalled in transit over 48 hours, package damage on arrival, or lost in transit, automated carrier coordination issues priority expedited delivery or proactive re-shipment.",
        sec2_title: "Audio Import & Specifications",
        sec2_p1: "Call audio serves as the foundational evidence for service verification and dispute resolution. The platform provides secure upload gateways with client-side and server-side integrity checks.",
        sec2_item1_lbl: "Format:",
        sec2_item1_val: "Standard call recording formats supported: WAV, MP3, M4A, FLAC. Recommended 16kHz or higher single/dual channel audio.",
        sec2_item2_lbl: "File Size:",
        sec2_item2_val: "Recommended under 20MB per recording, duration under 15 minutes. Large files should be split into segments.",
        sec2_item3_lbl: "Procedure:",
        sec2_item3_val: "Click or drag audio files onto the upload card. The system validates file integrity, displays size/duration, and enables the audio player. Click 'Transcribe' to process.",
        sec3_title: "Privacy Masking & Notes",
        sec3_p1: "In strict compliance with Personal Information Protection Law (PIPL) and data security audit requirements, customer sensitive data is masked automatically upon transcription:",
        sec3_th1: "Sensitive Data",
        sec3_th2: "Masking Rule",
        sec3_th3: "Raw Sample",
        sec3_th4: "Masked Output",
        sec3_r1_c1: "Phone Number",
        sec3_r1_c2: "First 3 and last 4 digits preserved, middle 4 replaced by asterisks",
        sec3_r2_c1: "Customer Name",
        sec3_r2_c2: "First letter/surname kept, subsequent characters masked",
        sec3_r3_c1: "National ID / Card",
        sec3_r3_c2: "Truncated and masked with asterisks",
        sec3_tip_lbl: "Seat Revision Feature: ",
        sec3_tip_val: "In case of local accents, ambient noise, or specialized terms, agents can click 'Manual Edit' to revise transcript text and save. The revised text serves as the single source of truth.",
        sec4_title: "Policy Search & Order Verification",
        sec4_p1: "Provides objective policy guidelines and order records to eliminate guesswork and subjective errors:",
        sec4_col1_t: "Policy Knowledge Retrieval",
        sec4_col1_d: "Matches transcript facts against verified company policies, returning exact clause titles, detailed excerpts, and match scores (e.g. 92%). When an inquiry falls outside policies, the system refuses to guess and prompts manual review.",
        sec4_col2_t: "Read-Only Order Verification",
        sec4_col2_d: "Queries central order systems in read-only mode using extracted order IDs (e.g. ORD-2026-8891), displaying product name, amount, order date, and shipping status to verify facts.",
        sec5_title: "Seat Approval & Idempotent Dispatch",
        sec5_p1: "VoiceOps adheres to strict enterprise governance standards with two non-negotiable principles:",
        sec5_h1: "Principle 1: Mandatory Human Approval Gate",
        sec5_d1: "Fully automated work order dispatch without human confirmation is strictly prohibited. The system-suggested resolution is an aid; authorized agents must verify and approve every ticket.",
        sec5_h2: "Principle 2: Idempotent Dispatch Protection",
        sec5_d2: "Every submission contains a unique idempotency key to prevent accidental duplicate work orders caused by network latency or repeated clicks. Once confirmed, an immutable work order voucher is generated.",
        sec6_title: "Automation & Audit Trails",
        sec6_p1: "Upon approval, downstream automations are dispatched and full-lifecycle audit trails are established:",
        sec6_c1_t: "Downstream Automation Dispatch",
        sec6_c1_d: "Triggers webhooks to warehouse management, carrier dispatch, and refund accounting systems while sending SMS notifications to customers.",
        sec6_c2_t: "End-to-End Audit Trail",
        sec6_c2_d: "The audit trail logs execution time (ms), input payloads, and output receipts across all 5 operational steps: Speech-to-Text, Masking, Policy Search, Order Check, and Ticket Dispatch.",
        sec7_title: "FAQ & Troubleshooting",
        sec7_q1: "Q: Can approved work orders be modified?",
        sec7_a1: "A: No. To preserve financial and legal audit integrity, approved tickets are locked in completed status. Agents can review full vouchers and proposals anytime. Supplementary actions require ERP ticket creation.",
        sec7_q2: "Q: How do I filter only pending sessions in the workbench?",
        sec7_a2: "A: Click the 'Pending' filter tab in the left sidebar to isolate sessions awaiting review. You can also search by phone number or session code in the search bar.",
        sec7_q3: "Q: What should I do if no policy is matched?",
        sec7_a3: "A: This indicates an edge case or inquiry outside standard policy rules. Staff should determine the resolution based on manager authorization and input the decision manually in the review card.",
        footer_copy: "VoiceOps Platform · Enterprise Operations Manual & Guidelines",
        footer_wb: "Workbench",
        footer_api: "API Docs",
        footer_top: "Back to Top ↑"
      }
    };

    let docLang = localStorage.getItem('voiceops_guide_lang') || localStorage.getItem('voiceops_lang') || 'zh';

    function applyDocLang(lang) {
      const dict = guideI18n[lang] || guideI18n.zh;
      for (const [key, val] of Object.entries(dict)) {
        const el = document.getElementById(key.replace(/_/g, '-'));
        if (el) el.innerText = val;
      }
      document.title = dict.doc_title;
      document.getElementById('lang-btn-text').innerText = lang === 'zh' ? 'English' : '中文';
    }

    function toggleDocLang() {
      docLang = docLang === 'zh' ? 'en' : 'zh';
      localStorage.setItem('voiceops_guide_lang', docLang);
      localStorage.setItem('voiceops_lang', docLang);
      applyDocLang(docLang);
    }

    applyDocLang(docLang);
  </script>
</body>
</html>
"""
