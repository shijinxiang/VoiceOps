<template>
  <div class="min-h-screen flex flex-col bg-[#f8fafc] text-slate-800 font-sans antialiased">
    <!-- Top Navigation Bar -->
    <header class="border-b border-slate-200/80 bg-white/95 backdrop-blur sticky top-0 z-40 px-6 py-3.5 shadow-xs">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <!-- Brand & Platform Info -->
        <div class="flex items-center space-x-3.5">
          <div class="w-9 h-9 rounded-xl bg-slate-900 text-white flex items-center justify-center shadow-xs font-semibold text-base tracking-wider">
            VO
          </div>
          <div>
            <div class="flex items-center space-x-2">
              <h1 class="font-bold text-base text-slate-900 tracking-tight">VoiceOps</h1>
              <span class="px-2 py-0.5 text-[11px] font-medium rounded-full bg-slate-100 text-slate-600 border border-slate-200/80">
                企业售后工作台
              </span>
            </div>
            <p class="text-xs text-slate-500 mt-0.5">客户语音速记 · 售后政策核对 · 订单关联 · 坐席工单流转系统</p>
          </div>
        </div>

        <!-- Top Right Actions -->
        <div class="flex items-center space-x-3">
          <div class="hidden sm:flex items-center space-x-2 px-3 py-1.5 bg-slate-50 border border-slate-200/80 rounded-lg text-xs text-slate-600">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>服务接入就绪</span>
          </div>

          <button 
            @click="initNewSession" 
            class="flex items-center space-x-1.5 px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-medium rounded-lg transition shadow-xs active:scale-95"
          >
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>录入新会话</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Container -->
    <div class="flex-1 max-w-7xl w-full mx-auto flex overflow-hidden">
      <!-- Left Sidebar: Session List -->
      <aside class="w-80 border-r border-slate-200 bg-white flex flex-col shrink-0">
        <!-- Search & Filter Header -->
        <div class="p-3.5 border-b border-slate-100 space-y-2.5">
          <div class="flex items-center justify-between text-xs">
            <span class="font-semibold text-slate-700">售后会话列表</span>
            <span class="px-1.5 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-600">{{ filteredSessions.length }} 项</span>
          </div>
          <div class="relative">
            <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="搜索编号、客户姓名或电话..." 
              class="w-full pl-8 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-slate-400 focus:bg-white"
            />
          </div>
        </div>

        <!-- Session Cards List -->
        <div class="flex-1 overflow-y-auto p-2.5 space-y-1.5">
          <div 
            v-for="s in filteredSessions" 
            :key="s.id"
            @click="selectSession(s)"
            :class="[
              'p-3 rounded-xl border transition cursor-pointer text-left',
              currentSession?.id === s.id 
                ? 'bg-slate-50 border-slate-300 shadow-xs ring-1 ring-slate-300' 
                : 'bg-white border-slate-200/70 hover:border-slate-300 hover:bg-slate-50/50'
            ]"
          >
            <div class="flex items-center justify-between mb-1.5">
              <span class="font-mono text-xs font-semibold text-slate-800">{{ s.session_code }}</span>
              <span 
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-medium',
                  s.status === 'completed' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                  s.status === 'pending_confirmation' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                  'bg-sky-50 text-sky-700 border border-sky-200'
                ]"
              >
                {{ statusText(s.status) }}
              </span>
            </div>

            <div class="text-xs font-medium text-slate-700 flex items-center justify-between">
              <span>客户: {{ s.customer_name_masked || '匿名客户' }}</span>
              <span class="font-mono text-slate-500 text-[11px]">{{ s.customer_phone_masked || '未留手机' }}</span>
            </div>

            <div class="text-[11px] text-slate-400 mt-2 flex items-center justify-between">
              <span>渠道: {{ s.channel || '语音热线' }}</span>
              <span>{{ formatDate(s.created_at) }}</span>
            </div>
          </div>

          <div v-if="filteredSessions.length === 0" class="text-center py-12 text-slate-400 text-xs">
            暂无匹配的会话记录
          </div>
        </div>
      </aside>

      <!-- Main Workspace -->
      <main class="flex-1 overflow-y-auto p-6 space-y-5 bg-[#f8fafc]">
        <!-- Empty State -->
        <div v-if="!currentSession" class="flex flex-col items-center justify-center h-full py-24 text-slate-400">
          <div class="w-12 h-12 rounded-2xl bg-white border border-slate-200 flex items-center justify-center text-slate-400 mb-3 shadow-xs">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 100-6 3 3 0 000 6z" />
            </svg>
          </div>
          <p class="text-sm font-medium text-slate-600">请选择左侧会话或点击上方录入新会话</p>
          <p class="text-xs text-slate-400 mt-1">支持录音速记、政策合规核对、订单查询与工单审批全流程</p>
        </div>

        <template v-else>
          <!-- Session Header Card -->
          <div class="bg-white border border-slate-200/90 rounded-xl p-4 shadow-xs flex flex-wrap items-center justify-between gap-4">
            <div class="space-y-1">
              <div class="flex items-center space-x-2.5">
                <h2 class="text-base font-bold text-slate-900 font-mono">{{ currentSession.session_code }}</h2>
                <span class="px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
                  渠道: {{ currentSession.channel }}
                </span>
                <span 
                  :class="[
                    'px-2.5 py-0.5 rounded text-xs font-medium',
                    currentSession.status === 'completed' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                    currentSession.status === 'pending_confirmation' ? 'bg-amber-50 text-amber-700 border border-amber-200' :
                    'bg-sky-50 text-sky-700 border border-sky-200'
                  ]"
                >
                  {{ statusText(currentSession.status) }}
                </span>
              </div>
              <p class="text-xs text-slate-500">
                客户档案: <span class="text-slate-800 font-medium">{{ currentSession.customer_name_masked }}</span> 
                <span class="mx-1 text-slate-300">|</span> 
                联系电话: <span class="font-mono text-slate-700">{{ currentSession.customer_phone_masked }}</span>
                <span class="mx-1 text-slate-300">|</span> 
                录入时间: {{ formatDate(currentSession.created_at) }}
              </p>
            </div>

            <div class="flex items-center space-x-2">
              <button 
                @click="reloadCurrentSession" 
                class="flex items-center space-x-1 px-3 py-1.5 bg-white hover:bg-slate-50 text-slate-600 border border-slate-200 rounded-lg text-xs font-medium transition"
              >
                <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>刷新状态</span>
              </button>
            </div>
          </div>

          <!-- Stepper Navigation -->
          <div class="grid grid-cols-4 gap-2 text-xs font-medium text-slate-500">
            <div :class="['p-2 rounded-lg border text-center transition', audioFiles.length > 0 ? 'bg-white border-slate-300 text-slate-800 shadow-xs' : 'bg-slate-50/70 border-slate-200/80']">
              1. 录音导入
            </div>
            <div :class="['p-2 rounded-lg border text-center transition', transcriptions.length > 0 ? 'bg-white border-slate-300 text-slate-800 shadow-xs' : 'bg-slate-50/70 border-slate-200/80']">
              2. 隐私脱敏速记
            </div>
            <div :class="['p-2 rounded-lg border text-center transition', agentResult ? 'bg-white border-slate-300 text-slate-800 shadow-xs' : 'bg-slate-50/70 border-slate-200/80']">
              3. 政策与单据核验
            </div>
            <div :class="['p-2 rounded-lg border text-center transition', currentWorkOrder ? 'bg-emerald-50 border-emerald-300 text-emerald-800 shadow-xs' : 'bg-slate-50/70 border-slate-200/80']">
              4. 坐席审核建单
            </div>
          </div>

          <!-- Step 1: Audio Upload Card -->
          <div class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">1</span>
                <h3 class="font-semibold text-slate-800 text-sm">售后录音导入</h3>
              </div>
              <span class="text-xs text-slate-400">支持 WAV / MP3 标准语音格式</span>
            </div>

            <!-- Upload Area -->
            <div 
              class="border-2 border-dashed border-slate-200 hover:border-slate-400 rounded-xl p-6 text-center cursor-pointer transition bg-slate-50/50 hover:bg-slate-50"
              @click="$refs.audioInput.click()"
            >
              <input 
                ref="audioInput" 
                type="file" 
                accept="audio/*" 
                class="hidden" 
                @change="handleFileUpload" 
              />
              <div class="w-10 h-10 mx-auto rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-500 mb-2 shadow-2xs">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <p class="text-xs font-semibold text-slate-700">点击上传或将售后录音拖曳至此</p>
              <p class="text-[11px] text-slate-400 mt-1">系统将自动执行语音文件完整性检验与降噪处理</p>
            </div>

            <!-- Uploaded Audio List -->
            <div v-if="audioFiles.length > 0" class="space-y-2 pt-1">
              <div 
                v-for="a in audioFiles" 
                :key="a.id"
                class="bg-slate-50 border border-slate-200/80 rounded-xl p-3 flex items-center justify-between"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-lg bg-white border border-slate-200 flex items-center justify-center text-slate-600">
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-xs font-semibold text-slate-800">{{ a.original_filename }}</p>
                    <p class="text-[11px] text-slate-400">时长: {{ a.duration_seconds }}s · 文件大小: {{ (a.file_size_bytes/1024).toFixed(1) }} KB</p>
                  </div>
                </div>

                <button 
                  @click="triggerASR(a.id)" 
                  :disabled="isTranscribing"
                  class="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white text-xs font-medium rounded-lg transition shadow-xs"
                >
                  <svg v-if="isTranscribing" class="animate-spin -ml-0.5 mr-1 h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                  </svg>
                  <span>{{ isTranscribing ? '速记解析中...' : '生成文字速记' }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Step 2: Transcript & Privacy Masking Card -->
          <div v-if="transcriptions.length > 0" class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">2</span>
                <h3 class="font-semibold text-slate-800 text-sm">录音速记与合规脱敏</h3>
              </div>
              <div class="flex items-center space-x-2 text-xs">
                <span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-medium">
                  客户隐私已脱敏保护
                </span>
                <span class="text-slate-400 text-[11px]">处理耗时: {{ transcriptions[0].processing_time_ms }}ms</span>
              </div>
            </div>

            <!-- Transcript Content -->
            <div class="space-y-3">
              <div class="bg-slate-50/80 border border-slate-200/80 rounded-xl p-4">
                <div class="flex items-center justify-between text-xs text-slate-500 mb-2">
                  <span class="font-medium text-slate-600">录音文字记录 (手机号、姓名等隐私敏感信息已掩码脱敏):</span>
                  <span v-if="transcriptions[0].is_manually_edited" class="text-amber-600 font-medium">✓ 坐席已人工校对</span>
                </div>
                <p class="text-xs text-slate-800 leading-relaxed font-sans bg-white p-3 rounded-lg border border-slate-200">
                  {{ transcriptions[0].edited_text || transcriptions[0].masked_text }}
                </p>
              </div>

              <!-- Action Bar -->
              <div class="flex items-center justify-between pt-1">
                <button 
                  @click="isEditingText = !isEditingText" 
                  class="text-xs font-medium text-slate-600 hover:text-slate-900 transition flex items-center space-x-1"
                >
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                  </svg>
                  <span>{{ isEditingText ? '收起校对' : '坐席手工校对' }}</span>
                </button>

                <button 
                  @click="runAgentWorkflow" 
                  :disabled="isAnalyzing"
                  class="px-4 py-2 bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white text-xs font-semibold rounded-lg transition shadow-xs flex items-center space-x-1.5"
                >
                  <svg v-if="isAnalyzing" class="animate-spin -ml-0.5 mr-1 h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                  </svg>
                  <span>{{ isAnalyzing ? '核验政策与关联单据中...' : '核验售后政策与关联单据' }}</span>
                </button>
              </div>

              <!-- Inline Revision Box -->
              <div v-if="isEditingText" class="mt-2 space-y-2 bg-slate-50 p-3 rounded-xl border border-slate-200">
                <textarea 
                  v-model="editBuffer" 
                  rows="3" 
                  class="w-full bg-white border border-slate-300 rounded-lg p-2.5 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-slate-400"
                  placeholder="修正文字速记中的错漏字词..."
                ></textarea>
                <div class="flex justify-end">
                  <button 
                    @click="saveManualRevision" 
                    class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white text-xs font-medium rounded-lg transition"
                  >
                    保存修订
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3: Policy Citations & Order Details Cards -->
          <div v-if="agentResult" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Left: Applicable Policy Guidelines -->
            <div class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
              <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                <div class="flex items-center space-x-2">
                  <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">3A</span>
                  <h4 class="font-semibold text-slate-800 text-xs">适用售后规章依据</h4>
                </div>
                <span class="text-[11px] text-slate-400">规章库核验</span>
              </div>

              <div v-if="agentResult.citations && agentResult.citations.length > 0" class="space-y-2">
                <div 
                  v-for="c in agentResult.citations" 
                  :key="c.policy_code"
                  class="bg-slate-50 border border-slate-200/80 rounded-lg p-3 text-xs space-y-1"
                >
                  <div class="flex items-center justify-between">
                    <span class="font-semibold text-slate-900">[{{ c.policy_code }}] {{ c.title }}</span>
                    <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-200 text-slate-700 font-mono">匹配度 {{ (c.score * 100).toFixed(0) }}%</span>
                  </div>
                  <p class="text-slate-600 text-[11px] leading-relaxed">{{ c.snippet }}</p>
                </div>
              </div>
              <div v-else class="text-xs text-amber-800 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                未检索到完全匹配的售后规章条款，请依据特殊政策人工判定。
              </div>
            </div>

            <!-- Right: Order Lookup Details -->
            <div class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
              <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                <div class="flex items-center space-x-2">
                  <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">3B</span>
                  <h4 class="font-semibold text-slate-800 text-xs">关联系统订单详情</h4>
                </div>
                <span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px] font-medium border border-slate-200">
                  诉求分类: {{ intentText(agentResult.intent) }}
                </span>
              </div>

              <div v-if="agentResult.order_data" class="bg-slate-50 border border-slate-200/80 rounded-lg p-3 text-xs space-y-2">
                <div class="flex justify-between">
                  <span class="text-slate-500">订单编号:</span>
                  <span class="text-slate-900 font-mono font-semibold">{{ agentResult.order_data.order_id }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-500">购买商品:</span>
                  <span class="text-slate-900 font-medium">{{ agentResult.order_data.product_name }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-500">订单金额与状态:</span>
                  <span class="text-slate-800">￥{{ agentResult.order_data.order_amount }} ({{ agentResult.order_data.shipping_status }})</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-500">承运物流:</span>
                  <span class="text-slate-800 font-mono">{{ agentResult.order_data.shipping_company }} {{ agentResult.order_data.tracking_number }}</span>
                </div>
              </div>
              <div v-else class="text-xs text-slate-500 p-3 bg-slate-50 border border-slate-200 rounded-lg">
                {{ agentResult.order_id ? `系统未查到单号 ${agentResult.order_id} 的对应记录` : '录音中未提取到有效单号' }}
              </div>
            </div>
          </div>

          <!-- Step 4: Staff Review & Work Order Approval -->
          <div v-if="agentResult" class="bg-white border-2 border-slate-900 rounded-xl p-5 shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">4</span>
                <h3 class="font-bold text-slate-900 text-sm">坐席人工审核建单</h3>
              </div>
              <span class="text-xs text-slate-500">必须经客服终审确认 · 防误操作门禁</span>
            </div>

            <div class="space-y-3">
              <div>
                <label class="text-xs font-semibold text-slate-700 block mb-1.5">拟定处置方案与审批结论 (可直接调整):</label>
                <textarea 
                  v-model="proposalBuffer" 
                  rows="2"
                  class="w-full bg-slate-50 border border-slate-300 rounded-lg p-3 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-slate-900 focus:bg-white leading-relaxed"
                ></textarea>
              </div>

              <div class="flex flex-wrap items-center justify-between gap-3 pt-2">
                <div class="text-xs text-slate-500">
                  审核坐席: <span class="font-semibold text-slate-800">客服工号 #1042</span>
                </div>

                <button 
                  @click="confirmWorkOrder" 
                  :disabled="isConfirming || currentWorkOrder?.status === 'CONFIRMED'"
                  class="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 disabled:bg-emerald-600 disabled:opacity-90 text-white font-semibold text-xs rounded-lg shadow-xs transition flex items-center space-x-1.5"
                >
                  <svg v-if="isConfirming" class="animate-spin -ml-0.5 mr-1 h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                  </svg>
                  <span>{{ currentWorkOrder?.status === 'CONFIRMED' ? '✓ 工单已审批建单并派发通知' : '审核通过，正式建单并触发流转通知' }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Step 5: Confirmed Work Order Details -->
          <div v-if="currentWorkOrder" class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-md bg-emerald-600 text-white text-[11px] font-semibold flex items-center justify-center">✓</span>
                <h3 class="font-semibold text-slate-800 text-sm">工单流转凭证</h3>
              </div>
              <span class="text-xs px-2.5 py-0.5 rounded font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                工单号: {{ currentWorkOrder.ticket_number }}
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span class="text-slate-500">工单当前状态:</span>
                <p class="text-emerald-700 font-bold mt-1 text-xs">已派发已建单 ({{ currentWorkOrder.status }})</p>
              </div>
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span class="text-slate-500">关联业务订单:</span>
                <p class="text-slate-800 font-mono font-semibold mt-1">{{ currentWorkOrder.order_id || '无' }}</p>
              </div>
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span class="text-slate-500">防重事务标识:</span>
                <p class="text-slate-500 font-mono truncate mt-1 text-[11px]">{{ currentWorkOrder.idempotency_key }}</p>
              </div>
            </div>
          </div>

          <!-- Step 6: Operation Audit Trail Log -->
          <div v-if="traces.length > 0" class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between pb-2 border-b border-slate-100">
              <h3 class="font-semibold text-slate-800 text-xs">系统操作流水与流转轨迹</h3>
              <span class="text-[11px] text-slate-400">共计 {{ traces.length }} 节点</span>
            </div>

            <div class="space-y-1.5">
              <div 
                v-for="t in traces" 
                :key="t.id"
                class="bg-slate-50 border border-slate-200/60 rounded-lg p-2.5 text-xs space-y-1"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span class="w-4 h-4 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center font-mono text-[10px]">
                      {{ t.step_index }}
                    </span>
                    <span class="font-medium text-slate-700">{{ actionTypeText(t.action_type) }}</span>
                  </div>
                  <span class="text-slate-400 font-mono text-[11px]">{{ t.latency_ms }} ms</span>
                </div>
                <div class="grid grid-cols-2 gap-2 text-[11px] font-mono text-slate-500 bg-white p-2 rounded border border-slate-200/80">
                  <div class="truncate">
                    <span class="text-slate-400">入参:</span> {{ JSON.stringify(t.input_payload) }}
                  </div>
                  <div class="truncate">
                    <span class="text-slate-400">回执:</span> {{ JSON.stringify(t.output_payload) }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = '/api/v1'

const sessions = ref<any[]>([])
const currentSession = ref<any>(null)
const audioFiles = ref<any[]>([])
const transcriptions = ref<any[]>([])
const agentResult = ref<any>(null)
const currentWorkOrder = ref<any>(null)
const traces = ref<any[]>([])
const searchQuery = ref('')

const isTranscribing = ref(false)
const isAnalyzing = ref(false)
const isConfirming = ref(false)
const isEditingText = ref(false)
const editBuffer = ref('')
const proposalBuffer = ref('')

const filteredSessions = computed(() => {
  if (!searchQuery.value.trim()) return sessions.value
  const q = searchQuery.value.toLowerCase()
  return sessions.value.filter(s => 
    (s.session_code && s.session_code.toLowerCase().includes(q)) ||
    (s.customer_name_masked && s.customer_name_masked.includes(q)) ||
    (s.customer_phone_masked && s.customer_phone_masked.includes(q))
  )
})

const statusText = (status: string) => {
  switch (status) {
    case 'completed': return '已结单'
    case 'pending_confirmation': return '待审核建单'
    default: return '流转中'
  }
}

const intentText = (intent: string) => {
  switch (intent) {
    case 'return_goods': return '7天无理由退货'
    case 'repair_goods': return '保修/维修申请'
    case 'logistics_inquiry': return '物流催查件'
    default: return intent || '常规售后'
  }
}

const actionTypeText = (type: string) => {
  switch (type) {
    case 'speech_to_text': return '录音转写速记'
    case 'pii_masking': return '隐私脱敏校验'
    case 'policy_search': return '适用规章检索'
    case 'order_lookup': return '系统订单比对'
    case 'ticket_create': return '工单生成与派发'
    default: return type
  }
}

const fetchSessions = async () => {
  try {
    const res = await axios.get(`${API_BASE}/sessions`)
    sessions.value = res.data
    if (sessions.value.length > 0 && !currentSession.value) {
      await selectSession(sessions.value[0])
    }
  } catch (e) {
    console.error('Fetch sessions failed', e)
  }
}

const selectSession = async (s: any) => {
  try {
    const res = await axios.get(`${API_BASE}/sessions/${s.id}`)
    currentSession.value = res.data
    audioFiles.value = res.data.audio_files || []
    transcriptions.value = res.data.transcriptions || []
    traces.value = res.data.traces || []
    if (res.data.work_orders && res.data.work_orders.length > 0) {
      currentWorkOrder.value = res.data.work_orders[0]
    } else {
      currentWorkOrder.value = null
    }
    if (transcriptions.value.length > 0) {
      editBuffer.value = transcriptions.value[0].edited_text || transcriptions.value[0].masked_text
    }
  } catch (e) {
    console.error('Load session details error', e)
  }
}

const initNewSession = async () => {
  try {
    const res = await axios.post(`${API_BASE}/sessions`, {
      customer_name: "张伟",
      customer_phone: "13812345678",
      channel: "电话热线"
    })
    await fetchSessions()
    await selectSession(res.data)
  } catch (e) {
    alert("创建会话失败")
  }
}

const reloadCurrentSession = async () => {
  if (currentSession.value) {
    await selectSession(currentSession.value)
  }
}

const handleFileUpload = async (event: any) => {
  const file = event.target.files[0]
  if (!file || !currentSession.value) return

  const formData = new FormData()
  formData.append('session_id', currentSession.value.id)
  formData.append('file', file)

  try {
    await axios.post(`${API_BASE}/audio/upload`, formData)
    await reloadCurrentSession()
  } catch (e: any) {
    alert(e.response?.data?.detail || "上传失败")
  }
}

const triggerASR = async (audioId: string) => {
  isTranscribing.value = true
  try {
    await axios.post(`${API_BASE}/transcriptions/process/${audioId}`)
    await reloadCurrentSession()
  } catch (e: any) {
    alert(e.response?.data?.detail || "生成速记失败")
  } finally {
    isTranscribing.value = false
  }
}

const saveManualRevision = async () => {
  if (transcriptions.value.length === 0) return
  const tid = transcriptions.value[0].id
  try {
    await axios.put(`${API_BASE}/transcriptions/${tid}/edit`, {
      edited_text: editBuffer.value
    })
    isEditingText.value = false
    await reloadCurrentSession()
  } catch (e: any) {
    alert(e.response?.data?.detail || "保存失败")
  }
}

const runAgentWorkflow = async () => {
  if (!currentSession.value) return
  isAnalyzing.value = true
  try {
    const res = await axios.post(`${API_BASE}/agent/run`, {
      session_id: currentSession.value.id
    })
    agentResult.value = res.data
    proposalBuffer.value = res.data.proposal
    await reloadCurrentSession()
  } catch (e: any) {
    alert(e.response?.data?.detail || "核验失败")
  } finally {
    isAnalyzing.value = false
  }
}

const confirmWorkOrder = async () => {
  if (!currentSession.value || !agentResult.value) return
  isConfirming.value = true
  try {
    const idemKey = `IDEM-${currentSession.value.id.slice(0, 8)}-${Date.now()}`
    const res = await axios.post(`${API_BASE}/work-orders/confirm`, {
      session_id: currentSession.value.id,
      order_id: agentResult.value.order_id,
      ticket_type: agentResult.value.ticket_type,
      solution_proposal: proposalBuffer.value,
      policy_citation: agentResult.value.citations,
      idempotency_key: idemKey,
      confirmed_by: "坐席工号 #1042"
    })
    currentWorkOrder.value = res.data
    await reloadCurrentSession()
  } catch (e: any) {
    alert(e.response?.data?.detail || "确认建单失败")
  } finally {
    isConfirming.value = false
  }
}

const formatDate = (iso: string) => {
  if (!iso) return ''
  return new Date(iso).toLocaleTimeString()
}

onMounted(() => {
  fetchSessions()
})
</script>
