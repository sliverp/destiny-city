<template>
  <div class="min-h-screen bg-bg flex flex-col">
    <!-- Top bar -->
    <div class="sticky top-0 z-20 bg-bg/95 backdrop-blur-sm border-b border-white/5 px-6 py-4">
      <div class="max-w-lg mx-auto">
        <div class="flex items-center justify-between mb-3">
          <span class="text-white font-mono text-sm">
            {{ displayIndex }} / {{ displayTotal }}
          </span>
          <span class="text-gray-500 text-xs tracking-wider">
            {{ currentStepCategory }}
          </span>
        </div>
        <!-- Progress bar -->
        <div class="w-full h-0.5 bg-gray-800 rounded-full overflow-hidden">
          <div
            class="h-full bg-white rounded-full transition-all duration-500 ease-out"
            :style="{ width: progressPercent + '%' }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Content area -->
    <div class="flex-1 flex items-center justify-center px-4 py-8">
      <div class="w-full max-w-lg" v-if="!loadingQuestions">

        <!-- Step 0: City Scope Selection -->
        <Transition :name="transitionName" mode="out-in">
          <div v-if="currentIndex === -1" key="scope" class="space-y-6">
            <div class="bg-white rounded-2xl shadow-card p-6 md:p-8">
              <div class="mb-5">
                <span class="inline-block px-3 py-1 bg-gray-100 text-gray-500 text-xs rounded-full tracking-wider">
                  ✦ 城市范围
                </span>
              </div>
              <h2 class="text-gray-900 text-lg md:text-xl font-medium leading-relaxed">
                你希望探索哪个范围的天选城市？
              </h2>
              <p class="text-gray-400 text-sm mt-2">这将影响最终的匹配结果</p>
            </div>

            <div class="space-y-3">
              <button
                v-for="option in scopeOptions"
                :key="option.value"
                @click="selectScope(option.value)"
                class="w-full text-left p-4 rounded-xl border transition-all duration-200 group"
                :class="
                  cityScope === option.value
                    ? 'bg-gray-50 border-gray-900 shadow-sm'
                    : 'bg-white border-gray-200 hover:border-gray-400 hover:shadow-sm'
                "
              >
                <div class="flex items-start gap-3">
                  <div
                    class="mt-0.5 w-5 h-5 rounded-full border-2 flex-shrink-0 flex items-center justify-center transition-all duration-200"
                    :class="
                      cityScope === option.value
                        ? 'border-gray-900 bg-gray-900'
                        : 'border-gray-300 group-hover:border-gray-400'
                    "
                  >
                    <svg
                      v-if="cityScope === option.value"
                      class="w-3 h-3 text-white"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="3"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  </div>
                  <div>
                    <span
                      class="text-sm md:text-base leading-relaxed transition-colors duration-200 block"
                      :class="
                        cityScope === option.value
                          ? 'text-gray-900 font-medium'
                          : 'text-gray-600 group-hover:text-gray-800'
                      "
                    >
                      {{ option.label }}
                    </span>
                    <span class="text-gray-400 text-xs mt-0.5 block">{{ option.desc }}</span>
                  </div>
                </div>
              </button>
            </div>
          </div>

          <!-- Regular questions -->
          <div v-else :key="currentIndex" class="space-y-6">
            <div class="bg-white rounded-2xl shadow-card p-6 md:p-8">
              <div class="mb-5">
                <span class="inline-block px-3 py-1 bg-gray-100 text-gray-500 text-xs rounded-full tracking-wider">
                  ✦ {{ currentQuestion?.category }}
                </span>
              </div>
              <h2 class="text-gray-900 text-lg md:text-xl font-medium leading-relaxed">
                {{ currentQuestion?.content }}
              </h2>
            </div>

            <div class="space-y-3">
              <button
                v-for="option in currentQuestion?.options"
                :key="option.id"
                @click="selectOption(option.id)"
                class="w-full text-left p-4 rounded-xl border transition-all duration-200 group"
                :class="
                  selectedOption === option.id
                    ? 'bg-gray-50 border-gray-900 shadow-sm'
                    : 'bg-white border-gray-200 hover:border-gray-400 hover:shadow-sm'
                "
              >
                <div class="flex items-start gap-3">
                  <div
                    class="mt-0.5 w-5 h-5 rounded-full border-2 flex-shrink-0 flex items-center justify-center transition-all duration-200"
                    :class="
                      selectedOption === option.id
                        ? 'border-gray-900 bg-gray-900'
                        : 'border-gray-300 group-hover:border-gray-400'
                    "
                  >
                    <svg
                      v-if="selectedOption === option.id"
                      class="w-3 h-3 text-white"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="3"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  </div>
                  <span
                    class="text-sm md:text-base leading-relaxed transition-colors duration-200"
                    :class="
                      selectedOption === option.id
                        ? 'text-gray-900 font-medium'
                        : 'text-gray-600 group-hover:text-gray-800'
                    "
                  >
                    {{ option.content }}
                  </span>
                </div>
              </button>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Loading state -->
      <div v-else class="text-center">
        <div class="animate-spin w-8 h-8 border-2 border-white/20 border-t-white rounded-full mx-auto mb-4"></div>
        <p class="text-gray-500 text-sm">正在召唤命运之题...</p>
      </div>
    </div>

    <!-- Bottom navigation -->
    <div class="sticky bottom-0 bg-bg/95 backdrop-blur-sm border-t border-white/5 px-6 py-4">
      <div class="max-w-lg mx-auto flex items-center justify-between">
        <button
          v-if="currentIndex > -1"
          @click="prevQuestion"
          class="px-4 py-2 text-gray-500 text-sm hover:text-white transition-colors"
        >
          ← {{ currentIndex === 0 ? '返回范围选择' : '上一题' }}
        </button>
        <div v-else></div>

        <!-- Scope step: next button -->
        <button
          v-if="currentIndex === -1"
          @click="nextFromScope"
          :disabled="!cityScope"
          class="px-6 py-2.5 bg-white text-gray-900 rounded-xl text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:translate-y-0"
        >
          开始答题 →
        </button>
        <!-- Regular question: next -->
        <button
          v-else-if="currentIndex < questions.length - 1"
          @click="nextQuestion"
          :disabled="!selectedOption"
          class="px-6 py-2.5 bg-white text-gray-900 rounded-xl text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:translate-y-0"
        >
          下一题 →
        </button>
        <!-- Last question: submit -->
        <button
          v-else
          @click="submitAnswers"
          :disabled="!selectedOption || submitting"
          class="px-6 py-2.5 bg-white text-gray-900 rounded-xl text-sm font-medium transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:translate-y-0"
        >
          <span v-if="!submitting">查看命运 ✦</span>
          <span v-else class="flex items-center gap-2">
            <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            命运推算中...
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getQuestions, submitAnswers as submitApi, saveTestProgress, getTestProgress } from '../api'
import type { Question } from '../types'

const router = useRouter()
const questions = ref<Question[]>([])
const currentIndex = ref(-1) // -1 = scope selection step
const answers = ref<Record<number, string>>({})
const selectedOption = ref<string | null>(null)
const loadingQuestions = ref(true)
const submitting = ref(false)
const transitionName = ref('slide-left')
const cityScope = ref<string>('')

const scopeOptions = [
  { value: 'domestic', label: '国内城市', desc: '探索中国境内的天选城市，贴近生活、更有共鸣' },
  { value: 'overseas', label: '国外城市', desc: '放眼全球，寻找远方的灵魂归属地' },
  { value: 'any', label: '不限范围', desc: '让命运在全世界为你寻找最佳匹配' },
]

const currentQuestion = computed(() => questions.value[currentIndex.value])

// 显示的序号：scope 页显示 1，问题从 2 开始
const displayIndex = computed(() => {
  if (currentIndex.value === -1) return '01'
  return String(currentIndex.value + 2).padStart(2, '0')
})
const displayTotal = computed(() => String(questions.value.length + 1).padStart(2, '0'))

const currentStepCategory = computed(() => {
  if (currentIndex.value === -1) return '城市范围'
  return currentQuestion.value?.category ?? ''
})

const progressPercent = computed(() => {
  const total = questions.value.length + 1 // +1 for scope step
  if (currentIndex.value === -1) return (1 / total) * 100
  return ((currentIndex.value + 2) / total) * 100
})

let saveTimer: ReturnType<typeof setTimeout> | null = null

function debouncedSave() {
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(() => {
    const token = sessionStorage.getItem('destiny_token')
    if (token) {
      saveTestProgress(token, answers.value, currentIndex.value, cityScope.value).catch(() => {})
    }
  }, 500)
}

onMounted(async () => {
  const token = sessionStorage.getItem('destiny_token')
  if (!token) {
    router.push('/')
    return
  }
  try {
    questions.value = await getQuestions(token)

    // 恢复进度
    const progress = await getTestProgress(token)
    if (progress.answers && Object.keys(progress.answers).length > 0) {
      answers.value = progress.answers
      cityScope.value = progress.city_scope || 'any'
      currentIndex.value = progress.current_index
      // 恢复当前题的已选选项
      if (currentIndex.value >= 0 && questions.value[currentIndex.value]) {
        selectedOption.value = answers.value[questions.value[currentIndex.value].id] || null
      }
    }
  } catch {
    router.push('/')
  } finally {
    loadingQuestions.value = false
  }
})

function selectScope(value: string) {
  cityScope.value = value
  setTimeout(() => nextFromScope(), 400)
}

function nextFromScope() {
  if (!cityScope.value) return
  transitionName.value = 'slide-left'
  currentIndex.value = 0
  selectedOption.value = answers.value[questions.value[0]?.id] || null
  debouncedSave()
}

function selectOption(optionId: string) {
  selectedOption.value = optionId
  if (currentQuestion.value) {
    answers.value[currentQuestion.value.id] = optionId
  }
  debouncedSave()
  if (currentIndex.value < questions.value.length - 1) {
    setTimeout(() => nextQuestion(), 400)
  }
}

function nextQuestion() {
  if (!selectedOption.value) return
  transitionName.value = 'slide-left'
  currentIndex.value++
  selectedOption.value = answers.value[questions.value[currentIndex.value]?.id] || null
  debouncedSave()
}

function prevQuestion() {
  transitionName.value = 'slide-right'
  if (currentIndex.value === 0) {
    currentIndex.value = -1
    selectedOption.value = null
  } else {
    currentIndex.value--
    selectedOption.value = answers.value[questions.value[currentIndex.value]?.id] || null
  }
}

async function submitAnswers() {
  if (!selectedOption.value || submitting.value) return
  submitting.value = true
  const token = sessionStorage.getItem('destiny_token')!
  try {
    const result = await submitApi(token, answers.value)
    sessionStorage.setItem('destiny_result', JSON.stringify(result))
    router.push(`/result/${result.share_id}`)
  } catch (e: any) {
    alert(e?.response?.data?.detail || '提交失败')
  } finally {
    submitting.value = false
  }
}
</script>
