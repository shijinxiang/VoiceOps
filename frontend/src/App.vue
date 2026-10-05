<template>
  <div class="min-h-screen flex flex-col bg-slate-950 text-slate-100">
    <!-- Header -->
    <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20 font-bold text-lg text-white">
          V
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="font-bold text-lg text-white tracking-wide">VoiceOps</h1>
            <span class="px-2 py-0.5 text-xs font-semibold rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">MVP v1.0</span>
          </div>
          <p class="text-xs text-slate-400">企业级语音售后智能工单与决策平台 (HITL & n8n 自动化闭环)</p>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <button 
          @click="initNewSession" 
          class="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-lg transition-all shadow-md shadow-blue-600/20 active:scale-95"
        >
          <span>+ 新建售后会话</span>
        </button>
      </div>
    </header>

    <!-- Main Container -->
    <div class="flex-1 flex overflow-hidden">
      <!-- Left Sidebar: Session List -->
      <aside class="w-80 border-r border-slate-800 bg-slate-900/40 flex flex-col shrink-0">
        <div class="p-4 border-b border-slate-800 flex items-center justify-between">
          <h2 class="text-sm font-semibold text-slate-300">历史售后会话</h2>
          <span class="text-xs bg-slate-800 px-2 py-0.5 rounded text-slate-400">{{ sessions.length }} 条</span>
        </div>
        <div class="flex-1 overflow-y-auto p-3 space-y-2">
          <div 
            v-for="s in sessions" 
            :key="s.id"
            @click="selectSession(s)"
            :class="[
              'p-3 rounded-xl border cursor-pointer transition-all',
              currentSession?.id === s.id 
                ? 'bg-blue-600/10 border-blue-500/40 shadow-sm' 
                : 'bg-slate-900/60 border-slate-800/80 hover:border-slate-700'
            ]"
          >
            <div class="flex items-center justify-between text-xs mb-1">
              <span class="font-mono text-slate-400">{{ s.session_code }}</span>
              <span 
                :class="[
                  'px-2 py-0.5 rounded text-[10px] font-medium uppercase',
                  s.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' :
                  s.status === 'pending_confirmation' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                  'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                ]"
              >
                {{ s.status }}
              </span>
            </div>
            <div class="text-sm font-medium text-slate-200">
              客户: {{ s.customer_name_masked || '匿名用户' }}
            </div>
            <div class="text-xs text-slate-500 mt-1 flex justify-between">
              <span>{{ s.customer_phone_masked || '未留电话' }}</span>
              <span>{{ formatDate(s.created_at) }}</span>
            </div>
          </div>
          <div v-if="sessions.length === 0" class="text-center py-10 text-slate-500 text-xs">
            暂无会话记录，点击右上角新建
          </div>
        </div>
      </aside>

      <!-- Center & Right: Detail & Workbench -->
      <main class="flex-1 overflow-y-auto p-6 space-y-6">
        <div v-if="!currentSession" class="flex flex-col items-center justify-center h-full text-slate-500">
          <div class="text-4xl mb-3">🎙️</div>
          <p class="text-base font-medium text-slate-400">请选择左侧会话或新建会话开始</p>
          <p class="text-xs text-slate-600 mt-1">支持短录音上传、智能脱敏、RAG知识检索、订单核实与人机协同建单</p>
        </div>

        <template v-else>
          <!-- Session Header Banner -->
          <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 flex flex-wrap items-center justify-between gap-4">
            <div>
              <div class="flex items-center space-x-3">
                <h2 class="text-xl font-bold text-white">{{ currentSession.session_code }}</h2>
                <span class="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded-md border border-slate-700">
                  渠道: {{ currentSession.channel }}
                </span>
                <span class="text-xs bg-blue-500/20 text-blue-400 px-2.5 py-1 rounded-md border border-blue-500/30 font-medium">
                  状态: {{ currentSession.status }}
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-1.5">
                客户信息: <span class="text-slate-200 font-medium">{{ currentSession.customer_name_masked }}</span> 
                ({{ currentSession.customer_phone_masked }}) | 创建于: {{ formatDate(currentSession.created_at) }}
              </p>
            </div>
            <div class="flex items-center space-x-2">
              <button 
                @click="reloadCurrentSession" 
                class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg border border-slate-700 transition"
              >
                刷新数据
              </button>
            </div>
          </div>

          <!-- Step 1: Audio Upload Card -->
          <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <div class="flex items-center space-x-2">
                <span class="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 text-xs font-bold flex items-center justify-center">1</span>
                <h3 class="font-semibold text-slate-200 text-sm">语音文件上传与解析 (WAV/MP3)</h3>
              </div>
              <span class="text-xs text-slate-500">支持最大 50MB, 时长 ≤ 10 分钟</span>
            </div>

            <!-- Upload Zone -->
            <div 
              class="border-2 border-dashed border-slate-700 hover:border-blue-500/50 rounded-xl p-6 text-center cursor-pointer transition bg-slate-950/40"
              @click="$refs.audioInput.click()"
            >
              <input 
                ref="audioInput" 
                type="file" 
                accept="audio/*" 
                class="hidden" 
                @change="handleFileUpload" 
              />
              <div class="text-2xl mb-2">📁</div>
              <p class="text-sm text-slate-300 font-medium">点击或拖拽上传客户售后录音</p>
              <p class="text-xs text-slate-500 mt-1">系统将自动执行文件完整性校验与静音探测 (VAD)</p>
            </div>

            <!-- Audio List if uploaded -->
            <div v-if="audioFiles.length > 0" class="space-y-2 mt-3">
              <div 
                v-for="a in audioFiles" 
                :key="a.id"
                class="bg-slate-800/40 border border-slate-700/60 rounded-xl p-3 flex items-center justify-between"
              >
                <div class="flex items-center space-x-3">
                  <div class="text-xl">🎵</div>
                  <div>
                    <p class="text-xs font-medium text-slate-200">{{ a.original_filename }}</p>
                    <p class="text-[10px] text-slate-400">时长: {{ a.duration_seconds }}s | 大小: {{ (a.file_size_bytes/1024).toFixed(1) }} KB</p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <button 
                    @click="triggerASR(a.id)" 
                    :disabled="isTranscribing"
                    class="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-xs font-medium rounded-lg shadow transition"
                  >
                    {{ isTranscribing ? '转写中...' : '开始转写与脱敏' }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 2: Transcription & Masking & Human Revision Card -->
          <div v-if="transcriptions.length > 0" class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <div class="flex items-center space-x-2">
                <span class="w-6 h-6 rounded-full bg-indigo-500/20 text-indigo-400 text-xs font-bold flex items-center justify-center">2</span>
                <h3 class="font-semibold text-slate-200 text-sm">语音转写文本与脱敏呈现 (PII Protection)</h3>
              </div>
              <div class="flex items-center space-x-2 text-xs">
                <span class="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded">
                  {{ transcriptions[0].asr_model }}
                </span>
                <span class="text-slate-500">耗时: {{ transcriptions[0].processing_time_ms }}ms</span>
              </div>
            </div>

            <!-- Content Area -->
            <div class="space-y-3">
              <div class="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
                <div class="flex items-center justify-between text-xs text-slate-400 mb-2">
                  <span>安全脱敏文本 (对对外日志与LLM呈现):</span>
                  <span v-if="transcriptions[0].is_manually_edited" class="text-amber-400 font-medium">✓ 人工已修订</span>
                </div>
                <p class="text-sm text-slate-200 leading-relaxed font-mono">
                  {{ transcriptions[0].edited_text || transcriptions[0].masked_text }}
                </p>
              </div>

              <!-- Inline Revision toggle -->
              <div class="flex items-center justify-between pt-1">
                <button 
                  @click="isEditingText = !isEditingText" 
                  class="text-xs text-blue-400 hover:text-blue-300 transition"
                >
                  {{ isEditingText ? '收起编辑' : '✏️ 坐席人工校对修订' }}
                </button>
                <button 
                  @click="runAgentWorkflow" 
                  :disabled="isAnalyzing"
                  class="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-xs font-semibold rounded-lg shadow-md shadow-blue-500/20 transition flex items-center space-x-2"
                >
                  <span>{{ isAnalyzing ? 'Agent 综合研判中...' : '启动 Agent 意图识别与决策' }}</span>
                </button>
              </div>

              <div v-if="isEditingText" class="mt-2 space-y-2">
                <textarea 
                  v-model="editBuffer" 
                  rows="3" 
                  class="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-sm text-slate-100 focus:outline-none focus:border-blue-500"
                  placeholder="修改转写文本..."
                ></textarea>
                <button 
                  @click="saveManualRevision" 
                  class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded-lg transition"
                >
                  保存修订
                </button>
              </div>
            </div>
          </div>

          <!-- Step 3: Agent Reasoning, Order Lookup & RAG Knowledge Card -->
          <div v-if="agentResult" class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- Left: RAG Policy Citations -->
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800/80 pb-2">
                <h4 class="font-semibold text-slate-200 text-sm flex items-center space-x-2">
                  <span class="w-5 h-5 rounded bg-emerald-500/20 text-emerald-400 text-xs flex items-center justify-center font-bold">R</span>
                  <span>知识库检索政策出处 (RAG)</span>
                </h4>
                <span class="text-[10px] text-slate-500">相似度阈值 ≥ 0.55</span>
              </div>

              <div v-if="agentResult.citations && agentResult.citations.length > 0" class="space-y-2">
                <div 
                  v-for="c in agentResult.citations" 
                  :key="c.policy_code"
                  class="bg-slate-950/60 border border-slate-800 rounded-xl p-3 text-xs space-y-1"
                >
                  <div class="flex items-center justify-between">
                    <span class="font-bold text-blue-400">[{{ c.policy_code }}] {{ c.title }}</span>
                    <span class="text-slate-500 font-mono">得分: {{ c.score }}</span>
                  </div>
                  <p class="text-slate-400 leading-relaxed">{{ c.snippet }}</p>
                </div>
              </div>
              <div v-else class="text-xs text-amber-400/80 p-3 bg-amber-500/5 border border-amber-500/20 rounded-xl">
                ⚠️ 未检索到高置信度售后政策条款，触发无依据拒答或需转人工高级客服。
              </div>
            </div>

            <!-- Right: Order Lookup & Intent -->
            <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-3">
              <div class="flex items-center justify-between border-b border-slate-800/80 pb-2">
                <h4 class="font-semibold text-slate-200 text-sm flex items-center space-x-2">
                  <span class="w-5 h-5 rounded bg-purple-500/20 text-purple-400 text-xs flex items-center justify-center font-bold">O</span>
                  <span>关联模拟订单详情 (只读)</span>
                </h4>
                <span class="text-xs px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 font-medium border border-purple-500/20">
                  意图: {{ agentResult.intent }}
                </span>
              </div>

              <div v-if="agentResult.order_data" class="bg-slate-950/60 border border-slate-800 rounded-xl p-3 text-xs space-y-2">
                <div class="flex justify-between">
                  <span class="text-slate-400">订单编号:</span>
                  <span class="text-slate-200 font-mono font-medium">{{ agentResult.order_data.order_id }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">商品名称:</span>
                  <span class="text-slate-200 font-medium">{{ agentResult.order_data.product_name }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">金额与签收:</span>
                  <span class="text-slate-200">￥{{ agentResult.order_data.order_amount }} ({{ agentResult.order_data.shipping_status }})</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">承运快递:</span>
                  <span class="text-slate-200">{{ agentResult.order_data.shipping_company }} ({{ agentResult.order_data.tracking_number }})</span>
                </div>
              </div>
              <div v-else class="text-xs text-slate-500 p-3 bg-slate-950/40 border border-slate-800/80 rounded-xl">
                {{ agentResult.order_id ? `订单号 ${agentResult.order_id} 未检索到对应订单数据` : '当前录音未提及明确订单号' }}
              </div>
            </div>
          </div>

          <!-- Step 4: Human-in-the-Loop Confirmation Card -->
          <div v-if="agentResult" class="bg-gradient-to-r from-blue-950/30 to-indigo-950/30 border border-blue-800/40 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-blue-800/30 pb-3">
              <div class="flex items-center space-x-2">
                <span class="w-6 h-6 rounded-full bg-blue-500 text-white text-xs font-bold flex items-center justify-center">4</span>
                <h3 class="font-bold text-white text-base">人工审核与工单确认 (Human-in-the-Loop)</h3>
              </div>
              <span class="text-xs text-blue-300/80">严禁非确认直接下发 · 幂等键防重保护</span>
            </div>

            <div class="space-y-3">
              <div>
                <label class="text-xs font-medium text-slate-400 block mb-1">建议处置方案 (可修改):</label>
                <textarea 
                  v-model="proposalBuffer" 
                  rows="2"
                  class="w-full bg-slate-950/80 border border-blue-900/50 rounded-xl p-3 text-sm text-slate-200 focus:outline-none focus:border-blue-500"
                ></textarea>
              </div>

              <div class="flex items-center justify-between pt-2">
                <div class="text-xs text-slate-400">
                  审核坐席: <span class="text-slate-200 font-medium">Agent-001 (当前工号)</span>
                </div>
                <button 
                  @click="confirmWorkOrder" 
                  :disabled="isConfirming || currentWorkOrder?.status === 'CONFIRMED'"
                  class="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-semibold text-sm rounded-xl shadow-lg shadow-emerald-600/30 transition flex items-center space-x-2"
                >
                  <span>{{ currentWorkOrder?.status === 'CONFIRMED' ? '✓ 工单已确认下发' : '确认建单并触发 n8n 通知' }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Step 5: Confirmed Work Order & n8n Automation Log Card -->
          <div v-if="currentWorkOrder" class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <div class="flex items-center space-x-2">
                <span class="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold flex items-center justify-center">5</span>
                <h3 class="font-semibold text-slate-200 text-sm">工单详情与 n8n 工作流状态</h3>
              </div>
              <span class="text-xs px-2 py-0.5 rounded font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                {{ currentWorkOrder.ticket_number }}
              </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div class="bg-slate-950/50 p-3 rounded-xl border border-slate-800">
                <span class="text-slate-400">工单状态:</span>
                <p class="text-emerald-400 font-bold mt-1 text-sm">{{ currentWorkOrder.status }}</p>
              </div>
              <div class="bg-slate-950/50 p-3 rounded-xl border border-slate-800">
                <span class="text-slate-400">关联订单:</span>
                <p class="text-slate-200 font-medium mt-1 font-mono">{{ currentWorkOrder.order_id || '无' }}</p>
              </div>
              <div class="bg-slate-950/50 p-3 rounded-xl border border-slate-800">
                <span class="text-slate-400">幂等键:</span>
                <p class="text-slate-400 font-mono truncate mt-1">{{ currentWorkOrder.idempotency_key }}</p>
              </div>
            </div>
          </div>

          <!-- Step 6: Audit Trail & Traces Explorer -->
          <div v-if="traces.length > 0" class="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <h3 class="font-semibold text-slate-200 text-sm flex items-center space-x-2">
                <span>🛡️</span>
                <span>全链路审计追溯日志 (Audit Trail & Agent Traces)</span>
              </h3>
              <span class="text-xs text-slate-500">{{ traces.length }} 个节点</span>
            </div>

            <div class="space-y-2">
              <div 
                v-for="t in traces" 
                :key="t.id"
                class="bg-slate-950/50 border border-slate-800/80 rounded-xl p-3 text-xs space-y-1.5"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span class="w-5 h-5 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center font-mono font-bold text-[10px]">
                      {{ t.step_index }}
                    </span>
                    <span class="font-semibold text-slate-300">{{ t.action_type }}</span>
                  </div>
                  <span class="text-slate-500 font-mono">{{ t.latency_ms }} ms</span>
                </div>
                <div class="grid grid-cols-2 gap-2 text-[11px] font-mono bg-slate-900/40 p-2 rounded-lg">
                  <div>
                    <span class="text-slate-500">输入 (脱敏):</span>
                    <p class="text-slate-300 truncate">{{ JSON.stringify(t.input_payload) }}</p>
                  </div>
                  <div>
                    <span class="text-slate-500">输出:</span>
                    <p class="text-slate-300 truncate">{{ JSON.stringify(t.output_payload) }}</p>
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
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = '/api/v1'

const sessions = ref<any[]>([])
const currentSession = ref<any>(null)
const audioFiles = ref<any[]>([])
const transcriptions = ref<any[]>([])
const agentResult = ref<any>(null)
const currentWorkOrder = ref<any>(null)
const traces = ref<any[]>([])

const isTranscribing = ref(false)
const isAnalyzing = ref(false)
const isConfirming = ref(false)
const isEditingText = ref(false)
const editBuffer = ref('')
const proposalBuffer = ref('')

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
      channel: "web_upload"
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
    alert(e.response?.data?.detail || "转写失败")
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
    alert(e.response?.data?.detail || "分析失败")
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
      confirmed_by: "Agent-001"
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
