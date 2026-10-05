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
                {{ t('badge_workbench') }}
              </span>
            </div>
            <p class="text-xs text-slate-500 mt-0.5">{{ t('subtitle') }}</p>
          </div>
        </div>

        <!-- Top Right Actions -->
        <div class="flex items-center space-x-3">
          <!-- Language Toggle Button -->
          <button 
            @click="toggleLang"
            class="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-medium rounded-lg transition border border-slate-200/80"
            :title="currentLang === 'zh' ? 'Switch to English' : '切换为中文'"
          >
            <svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
            </svg>
            <span class="font-semibold">{{ currentLang === 'zh' ? 'English' : '中文' }}</span>
          </button>

          <div class="hidden sm:flex items-center space-x-2 px-3 py-1.5 bg-slate-50 border border-slate-200/80 rounded-lg text-xs text-slate-600">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>{{ t('service_ready') }}</span>
          </div>

          <button 
            @click="initNewSession" 
            class="flex items-center space-x-1.5 px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-medium rounded-lg transition shadow-xs active:scale-95"
          >
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>{{ t('btn_new_session') }}</span>
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
            <span class="font-semibold text-slate-700">{{ t('session_list_title') }}</span>
            <span class="px-1.5 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-600">{{ filteredSessions.length }} {{ t('items_unit') }}</span>
          </div>
          <div class="relative">
            <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              v-model="searchQuery" 
              type="text" 
              :placeholder="t('search_placeholder')" 
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
              <span>{{ t('customer_prefix') }} {{ s.customer_name_masked || t('anonymous_customer') }}</span>
              <span class="font-mono text-slate-500 text-[11px]">{{ s.customer_phone_masked || t('no_phone') }}</span>
            </div>

            <div class="text-[11px] text-slate-400 mt-2 flex items-center justify-between">
              <span>{{ t('channel_prefix') }} {{ channelText(s.channel) }}</span>
              <span>{{ formatDate(s.created_at) }}</span>
            </div>
          </div>

          <div v-if="filteredSessions.length === 0" class="text-center py-12 text-slate-400 text-xs">
            {{ t('no_sessions_found') }}
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
          <p class="text-sm font-medium text-slate-600">{{ t('empty_select_prompt') }}</p>
          <p class="text-xs text-slate-400 mt-1">{{ t('empty_select_sub') }}</p>
        </div>

        <template v-else>
          <!-- Session Header Card -->
          <div class="bg-white border border-slate-200/90 rounded-xl p-4 shadow-xs flex flex-wrap items-center justify-between gap-4">
            <div class="space-y-1">
              <div class="flex items-center space-x-2.5">
                <h2 class="text-base font-bold text-slate-900 font-mono">{{ currentSession.session_code }}</h2>
                <span class="px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-600 border border-slate-200">
                  {{ t('channel_prefix') }} {{ channelText(currentSession.channel) }}
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
                {{ t('customer_profile') }} <span class="text-slate-800 font-medium">{{ currentSession.customer_name_masked }}</span> 
                <span class="mx-1 text-slate-300">|</span> 
                {{ t('contact_phone') }} <span class="font-mono text-slate-700">{{ currentSession.customer_phone_masked }}</span>
                <span class="mx-1 text-slate-300">|</span> 
                {{ t('created_time') }} {{ formatDate(currentSession.created_at) }}
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
                <span>{{ t('btn_refresh') }}</span>
              </button>
            </div>
          </div>

          <!-- Stepper Navigation -->
          <div class="grid grid-cols-4 gap-2 text-xs font-medium text-slate-500">
            <div :class="['p-2 rounded-lg border text-center transition', audioFiles.length > 0 ? 'bg-white border-slate-300 text-slate-800 shadow-xs' : 'bg-slate-50/70 border-slate-200/80']">
              {{ t('step_1') }}
            </div>
            <div :class="['p-2 rounded-lg border text-center transition', transcriptions.length > 0 ? 'bg-white border-slate-300 text-slate-800 shadow-xs' : 'bg-slate-50/70 border-slate-200/80']">
              {{ t('step_2') }}
            </div>
            <div :class="['p-2 rounded-lg border text-center transition', agentResult ? 'bg-white border-slate-300 text-slate-800 shadow-xs' : 'bg-slate-50/70 border-slate-200/80']">
              {{ t('step_3') }}
            </div>
            <div :class="['p-2 rounded-lg border text-center transition', currentWorkOrder ? 'bg-emerald-50 border-emerald-300 text-emerald-800 shadow-xs' : 'bg-slate-50/70 border-slate-200/80']">
              {{ t('step_4') }}
            </div>
          </div>

          <!-- Step 1: Audio Upload Card -->
          <div class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">1</span>
                <h3 class="font-semibold text-slate-800 text-sm">{{ t('card1_title') }}</h3>
              </div>
              <span class="text-xs text-slate-400">{{ t('card1_format_tip') }}</span>
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
              <p class="text-xs font-semibold text-slate-700">{{ t('card1_upload_prompt') }}</p>
              <p class="text-[11px] text-slate-400 mt-1">{{ t('card1_upload_desc') }}</p>
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
                    <p class="text-[11px] text-slate-400">{{ t('audio_duration') }} {{ a.duration_seconds }}s · {{ t('audio_size') }} {{ (a.file_size_bytes/1024).toFixed(1) }} KB</p>
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
                  <span>{{ isTranscribing ? t('btn_transcribing') : t('btn_transcribe') }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Step 2: Transcript & Privacy Masking Card -->
          <div v-if="transcriptions.length > 0" class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">2</span>
                <h3 class="font-semibold text-slate-800 text-sm">{{ t('card2_title') }}</h3>
              </div>
              <div class="flex items-center space-x-2 text-xs">
                <span class="px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-medium">
                  {{ t('card2_privacy_tag') }}
                </span>
                <span class="text-slate-400 text-[11px]">{{ t('process_duration') }} {{ transcriptions[0].processing_time_ms }}ms</span>
              </div>
            </div>

            <!-- Transcript Content -->
            <div class="space-y-3">
              <div class="bg-slate-50/80 border border-slate-200/80 rounded-xl p-4">
                <div class="flex items-center justify-between text-xs text-slate-500 mb-2">
                  <span class="font-medium text-slate-600">{{ t('card2_content_label') }}</span>
                  <span v-if="transcriptions[0].is_manually_edited" class="text-amber-600 font-medium">{{ t('card2_edited_tag') }}</span>
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
                  <span>{{ isEditingText ? t('btn_collapse_edit') : t('btn_manual_edit') }}</span>
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
                  <span>{{ isAnalyzing ? t('btn_verifying') : t('btn_verify_policy') }}</span>
                </button>
              </div>

              <!-- Inline Revision Box -->
              <div v-if="isEditingText" class="mt-2 space-y-2 bg-slate-50 p-3 rounded-xl border border-slate-200">
                <textarea 
                  v-model="editBuffer" 
                  rows="3" 
                  class="w-full bg-white border border-slate-300 rounded-lg p-2.5 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-slate-400"
                  :placeholder="t('edit_placeholder')"
                ></textarea>
                <div class="flex justify-end">
                  <button 
                    @click="saveManualRevision" 
                    class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-white text-xs font-medium rounded-lg transition"
                  >
                    {{ t('btn_save_revision') }}
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
                  <h4 class="font-semibold text-slate-800 text-xs">{{ t('card3a_title') }}</h4>
                </div>
                <span class="text-[11px] text-slate-400">{{ t('card3a_sub') }}</span>
              </div>

              <div v-if="agentResult.citations && agentResult.citations.length > 0" class="space-y-2">
                <div 
                  v-for="c in agentResult.citations" 
                  :key="c.policy_code"
                  class="bg-slate-50 border border-slate-200/80 rounded-lg p-3 text-xs space-y-1"
                >
                  <div class="flex items-center justify-between">
                    <span class="font-semibold text-slate-900">[{{ c.policy_code }}] {{ c.title }}</span>
                    <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-200 text-slate-700 font-mono">{{ t('match_score') }} {{ (c.score * 100).toFixed(0) }}%</span>
                  </div>
                  <p class="text-slate-600 text-[11px] leading-relaxed">{{ c.snippet }}</p>
                </div>
              </div>
              <div v-else class="text-xs text-amber-800 p-3 bg-amber-50 border border-amber-200 rounded-lg">
                {{ t('no_policy_matched') }}
              </div>
            </div>

            <!-- Right: Order Lookup Details -->
            <div class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
              <div class="flex items-center justify-between pb-2 border-b border-slate-100">
                <div class="flex items-center space-x-2">
                  <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">3B</span>
                  <h4 class="font-semibold text-slate-800 text-xs">{{ t('card3b_title') }}</h4>
                </div>
                <span class="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-[11px] font-medium border border-slate-200">
                  {{ t('intent_prefix') }} {{ intentText(agentResult.intent) }}
                </span>
              </div>

              <div v-if="agentResult.order_data" class="bg-slate-50 border border-slate-200/80 rounded-lg p-3 text-xs space-y-2">
                <div class="flex justify-between">
                  <span class="text-slate-500">{{ t('order_id_label') }}</span>
                  <span class="text-slate-900 font-mono font-semibold">{{ agentResult.order_data.order_id }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-500">{{ t('order_product_label') }}</span>
                  <span class="text-slate-900 font-medium">{{ agentResult.order_data.product_name }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-500">{{ t('order_amount_status_label') }}</span>
                  <span class="text-slate-800 font-medium">￥{{ agentResult.order_data.order_amount }} ({{ agentResult.order_data.shipping_status }})</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-500">{{ t('order_shipping_label') }}</span>
                  <span class="text-slate-800 font-mono">{{ agentResult.order_data.shipping_company }} {{ agentResult.order_data.tracking_number }}</span>
                </div>
              </div>
              <div v-else class="text-xs text-slate-500 p-3 bg-slate-50 border border-slate-200 rounded-lg">
                {{ agentResult.order_id ? `${t('order_not_found')} ${agentResult.order_id}` : t('order_not_extracted') }}
              </div>
            </div>
          </div>

          <!-- Step 4: Staff Review & Work Order Approval -->
          <div v-if="agentResult" class="bg-white border-2 border-slate-900 rounded-xl p-5 shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-md bg-slate-900 text-white text-[11px] font-semibold flex items-center justify-center">4</span>
                <h3 class="font-bold text-slate-900 text-sm">{{ t('card4_title') }}</h3>
              </div>
              <span class="text-xs text-slate-500">{{ t('card4_sub') }}</span>
            </div>

            <div class="space-y-3">
              <div>
                <label class="text-xs font-semibold text-slate-700 block mb-1.5">{{ t('card4_proposal_label') }}</label>
                <textarea 
                  v-model="proposalBuffer" 
                  rows="2"
                  class="w-full bg-slate-50 border border-slate-300 rounded-lg p-3 text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-slate-900 focus:bg-white leading-relaxed"
                ></textarea>
              </div>

              <div class="flex flex-wrap items-center justify-between gap-3 pt-2">
                <div class="text-xs text-slate-500">
                  {{ t('card4_operator') }}
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
                  <span>{{ currentWorkOrder?.status === 'CONFIRMED' ? t('btn_confirmed_state') : t('btn_confirm_ticket') }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Step 5: Confirmed Work Order Details -->
          <div v-if="currentWorkOrder" class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-100">
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5 rounded-md bg-emerald-600 text-white text-[11px] font-semibold flex items-center justify-center">✓</span>
                <h3 class="font-semibold text-slate-800 text-sm">{{ t('card5_title') }}</h3>
              </div>
              <span class="text-xs px-2.5 py-0.5 rounded font-mono font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                {{ t('ticket_number_prefix') }} {{ currentWorkOrder.ticket_number }}
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span class="text-slate-500">{{ t('ticket_status_label') }}</span>
                <p class="text-emerald-700 font-bold mt-1 text-xs">{{ t('ticket_status_created') }} ({{ currentWorkOrder.status }})</p>
              </div>
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span class="text-slate-500">{{ t('ticket_linked_order') }}</span>
                <p class="text-slate-800 font-mono font-semibold mt-1">{{ currentWorkOrder.order_id || t('none_value') }}</p>
              </div>
              <div class="bg-slate-50 p-3 rounded-lg border border-slate-200/80">
                <span class="text-slate-500">{{ t('ticket_idempotency_key') }}</span>
                <p class="text-slate-500 font-mono truncate mt-1 text-[11px]">{{ currentWorkOrder.idempotency_key }}</p>
              </div>
            </div>
          </div>

          <!-- Step 6: Operation Audit Trail Log -->
          <div v-if="traces.length > 0" class="bg-white border border-slate-200/90 rounded-xl p-5 shadow-xs space-y-3">
            <div class="flex items-center justify-between pb-2 border-b border-slate-100">
              <h3 class="font-semibold text-slate-800 text-xs">{{ t('card6_title') }}</h3>
              <span class="text-[11px] text-slate-400">{{ t('trace_nodes_count', { count: traces.length }) }}</span>
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
                    <span class="text-slate-400">{{ t('trace_in') }}</span> {{ JSON.stringify(t.input_payload) }}
                  </div>
                  <div class="truncate">
                    <span class="text-slate-400">{{ t('trace_out') }}</span> {{ JSON.stringify(t.output_payload) }}
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

// --- Language & i18n Dictionary ---
type Locale = 'zh' | 'en'
const currentLang = ref<Locale>((localStorage.getItem('voiceops_lang') as Locale) || 'zh')

const messages = {
  zh: {
    badge_workbench: '企业售后工作台',
    subtitle: '客户语音速记 · 售后政策核对 · 订单关联 · 坐席工单流转系统',
    service_ready: '服务运行就绪',
    btn_new_session: '录入新会话',
    session_list_title: '售后会话列表',
    items_unit: '项',
    search_placeholder: '搜索编号、客户姓名或手机号...',
    no_sessions_found: '暂无匹配的会话记录',
    status_completed: '已结单',
    status_pending_confirmation: '待审核建单',
    status_processing: '流转中',
    customer_prefix: '客户: ',
    anonymous_customer: '匿名客户',
    no_phone: '未留手机',
    channel_prefix: '渠道: ',
    channel_voice: '电话热线',
    empty_select_prompt: '请选择左侧会话或点击上方录入新会话',
    empty_select_sub: '支持录音速记、政策合规核对、订单查询与工单审批全流程',
    customer_profile: '客户档案: ',
    contact_phone: '联系电话: ',
    created_time: '录入时间: ',
    btn_refresh: '刷新状态',
    step_1: '1. 录音导入',
    step_2: '2. 隐私脱敏速记',
    step_3: '3. 政策与单据核验',
    step_4: '4. 坐席审核建单',
    card1_title: '售后录音导入',
    card1_format_tip: '支持标准音频格式',
    card1_upload_prompt: '点击上传或将售后录音拖曳至此',
    card1_upload_desc: '系统将自动执行语音文件完整性检验与降噪处理',
    audio_duration: '时长: ',
    audio_size: '文件大小: ',
    btn_transcribe: '生成文字速记',
    btn_transcribing: '速记解析中...',
    card2_title: '录音速记与合规脱敏',
    card2_privacy_tag: '客户隐私已脱敏保护',
    process_duration: '处理耗时: ',
    card2_content_label: '录音文字记录（手机号、姓名等隐私敏感信息已掩码脱敏）:',
    card2_edited_tag: '✓ 坐席已人工校对',
    btn_manual_edit: '坐席手工校对',
    btn_collapse_edit: '收起校对',
    edit_placeholder: '修正文字速记中的错漏字词...',
    btn_save_revision: '保存修订',
    btn_verify_policy: '核验售后政策与关联单据',
    btn_verifying: '核验政策与关联单据中...',
    card3a_title: '适用售后规章依据',
    card3a_sub: '规章库核验',
    match_score: '匹配度',
    no_policy_matched: '未检索到完全匹配的售后规章条款，请依据特殊政策人工判定。',
    card3b_title: '关联系统订单详情',
    intent_prefix: '诉求分类: ',
    intent_return: '七天无理由退货',
    intent_repair: '保修与维修申请',
    intent_logistics: '物流催查件',
    intent_other: '常规售后',
    order_id_label: '订单编号:',
    order_product_label: '购买商品:',
    order_amount_status_label: '订单金额与状态:',
    order_shipping_label: '承运物流:',
    order_not_found: '系统未查到单号记录',
    order_not_extracted: '录音中未提取到有效单号',
    card4_title: '坐席人工审核建单',
    card4_sub: '必须经客服终审确认 · 防误操作门禁',
    card4_proposal_label: '拟定处置方案与审批结论（可直接调整）:',
    card4_operator: '审核坐席: 客服工号 1042',
    btn_confirm_ticket: '审核通过，正式建单并触发流转通知',
    btn_confirmed_state: '✓ 工单已审批建单并派发通知',
    card5_title: '工单流转凭证',
    ticket_number_prefix: '工单号: ',
    ticket_status_label: '工单当前状态:',
    ticket_status_created: '已派发已建单',
    ticket_linked_order: '关联业务订单:',
    ticket_idempotency_key: '防重事务标识:',
    none_value: '无',
    card6_title: '系统操作流水与流转轨迹',
    trace_nodes_count: '共计 {count} 节点',
    trace_in: '入参:',
    trace_out: '回执:',
    action_stt: '录音转写速记',
    action_mask: '隐私脱敏校验',
    action_policy: '适用规章检索',
    action_order: '系统订单比对',
    action_ticket: '工单生成与派发',
    alert_create_failed: '创建会话失败',
    alert_upload_failed: '上传失败',
    alert_transcribe_failed: '生成速记失败',
    alert_save_failed: '保存失败',
    alert_verify_failed: '核验失败',
    alert_confirm_failed: '确认建单失败'
  },
  en: {
    badge_workbench: 'Operations Console',
    subtitle: 'Audio Memo · Policy Verification · Order Matching · Ticket Dispatch System',
    service_ready: 'Service Ready',
    btn_new_session: 'New Session',
    session_list_title: 'Customer Sessions',
    items_unit: 'items',
    search_placeholder: 'Search code, customer name or phone...',
    no_sessions_found: 'No matching sessions found',
    status_completed: 'Completed',
    status_pending_confirmation: 'Pending Approval',
    status_processing: 'In Progress',
    customer_prefix: 'Customer: ',
    anonymous_customer: 'Anonymous',
    no_phone: 'No Phone',
    channel_prefix: 'Channel: ',
    channel_voice: 'Voice Hotline',
    empty_select_prompt: 'Select a session or create a new one to begin',
    empty_select_sub: 'Complete workflow for audio memo, policy check, order query, and ticket approval',
    customer_profile: 'Customer: ',
    contact_phone: 'Phone: ',
    created_time: 'Created: ',
    btn_refresh: 'Refresh Status',
    step_1: '1. Audio Import',
    step_2: '2. Masked Memo',
    step_3: '3. Policy & Order',
    step_4: '4. Ticket Review',
    card1_title: 'Audio Recording Import',
    card1_format_tip: 'Standard Audio Formats Supported',
    card1_upload_prompt: 'Click or drag customer audio here to upload',
    card1_upload_desc: 'Automatic file integrity validation and noise reduction',
    audio_duration: 'Duration: ',
    audio_size: 'File Size: ',
    btn_transcribe: 'Generate Transcript',
    btn_transcribing: 'Transcribing...',
    card2_title: 'Transcript & Privacy Masking',
    card2_privacy_tag: 'Customer Privacy Protected',
    process_duration: 'Latency: ',
    card2_content_label: 'Audio Record (Customer phone and personal data masked for compliance):',
    card2_edited_tag: '✓ Manually Revised',
    btn_manual_edit: 'Manual Revision',
    btn_collapse_edit: 'Collapse Editor',
    edit_placeholder: 'Correct text and phrasing in transcript...',
    btn_save_revision: 'Save Revision',
    btn_verify_policy: 'Verify Policy & Match Order',
    btn_verifying: 'Verifying Policy & Orders...',
    card3a_title: 'Applicable Policy Guidelines',
    card3a_sub: 'Policy Verification',
    match_score: 'Match Score',
    no_policy_matched: 'No exact policy terms matched. Manual review required.',
    card3b_title: 'Linked Order Details',
    intent_prefix: 'Category: ',
    intent_return: '7-Day Return',
    intent_repair: 'Repair & Warranty',
    intent_logistics: 'Logistics Inquiry',
    intent_other: 'General Inquiry',
    order_id_label: 'Order ID:',
    order_product_label: 'Product:',
    order_amount_status_label: 'Amount & Status:',
    order_shipping_label: 'Logistics Carrier:',
    order_not_found: 'Order not found for',
    order_not_extracted: 'No order ID extracted from audio',
    card4_title: 'Staff Review & Approval',
    card4_sub: 'Mandatory Human Approval Gate · Error Prevention',
    card4_proposal_label: 'Proposed Resolution & Approval Note (Editable):',
    card4_operator: 'Reviewer: Staff #1042',
    btn_confirm_ticket: 'Approve & Dispatch Work Order',
    btn_confirmed_state: '✓ Work Order Approved & Dispatched',
    card5_title: 'Work Order Voucher',
    ticket_number_prefix: 'Ticket #: ',
    ticket_status_label: 'Ticket Status:',
    ticket_status_created: 'Dispatched & Created',
    ticket_linked_order: 'Linked Order:',
    ticket_idempotency_key: 'Idempotency Key:',
    none_value: 'None',
    card6_title: 'Operation Audit Trail & Flow',
    trace_nodes_count: '{count} Nodes Total',
    trace_in: 'Input:',
    trace_out: 'Output:',
    action_stt: 'Audio Transcription',
    action_mask: 'Privacy Masking',
    action_policy: 'Policy Search',
    action_order: 'Order Verification',
    action_ticket: 'Ticket Dispatch',
    alert_create_failed: 'Failed to create session',
    alert_upload_failed: 'Upload failed',
    alert_transcribe_failed: 'Transcription failed',
    alert_save_failed: 'Save failed',
    alert_verify_failed: 'Verification failed',
    alert_confirm_failed: 'Approval failed'
  }
}

const t = (key: string, params?: Record<string, any>) => {
  const dict = messages[currentLang.value] as any
  let val = dict[key] || key
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      val = val.replace(`{${k}}`, v)
    }
  }
  return val
}

const toggleLang = () => {
  currentLang.value = currentLang.value === 'zh' ? 'en' : 'zh'
  localStorage.setItem('voiceops_lang', currentLang.value)
}

// --- Application State ---
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
    case 'completed': return t('status_completed')
    case 'pending_confirmation': return t('status_pending_confirmation')
    default: return t('status_processing')
  }
}

const channelText = (ch: string) => {
  if (!ch || ch === 'web_upload' || ch === '电话热线') {
    return t('channel_voice')
  }
  return ch
}

const intentText = (intent: string) => {
  switch (intent) {
    case 'return_goods': return t('intent_return')
    case 'repair_goods': return t('intent_repair')
    case 'logistics_inquiry': return t('intent_logistics')
    default: return intent ? t('intent_other') : t('intent_other')
  }
}

const actionTypeText = (type: string) => {
  switch (type) {
    case 'speech_to_text': return t('action_stt')
    case 'pii_masking': return t('action_mask')
    case 'policy_search': return t('action_policy')
    case 'order_lookup': return t('action_order')
    case 'ticket_create': return t('action_ticket')
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
      customer_name: currentLang.value === 'zh' ? "张伟" : "David Zhang",
      customer_phone: "13812345678",
      channel: currentLang.value === 'zh' ? "电话热线" : "Voice Hotline"
    })
    await fetchSessions()
    await selectSession(res.data)
  } catch (e) {
    alert(t('alert_create_failed'))
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
    alert(e.response?.data?.detail || t('alert_upload_failed'))
  }
}

const triggerASR = async (audioId: string) => {
  isTranscribing.value = true
  try {
    await axios.post(`${API_BASE}/transcriptions/process/${audioId}`)
    await reloadCurrentSession()
  } catch (e: any) {
    alert(e.response?.data?.detail || t('alert_transcribe_failed'))
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
    alert(e.response?.data?.detail || t('alert_save_failed'))
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
    alert(e.response?.data?.detail || t('alert_verify_failed'))
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
      confirmed_by: currentLang.value === 'zh' ? "坐席工号 1042" : "Staff #1042"
    })
    currentWorkOrder.value = res.data
    await reloadCurrentSession()
  } catch (e: any) {
    alert(e.response?.data?.detail || t('alert_confirm_failed'))
  } finally {
    isConfirming.value = false
  }
}

const formatDate = (iso: string) => {
  if (!iso) return ''
  const locale = currentLang.value === 'zh' ? 'zh-CN' : 'en-US'
  return new Date(iso).toLocaleTimeString(locale)
}

onMounted(() => {
  fetchSessions()
})
</script>
