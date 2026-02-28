<template>
  <div class="min-h-screen bg-bg">
    <!-- Loading state -->
    <div v-if="loading" class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <div class="animate-spin w-8 h-8 border-2 border-white/20 border-t-white rounded-full mx-auto mb-4"></div>
        <p class="text-gray-500 text-sm">命运正在揭晓...</p>
      </div>
    </div>

    <!-- Result content -->
    <div v-else-if="result" class="max-w-lg mx-auto px-4 py-12">

      <!-- ====== HERO: City & Score ====== -->
      <Transition name="fade-up" appear>
        <div class="text-center mb-6">
          <p class="text-gray-500 text-xs tracking-[0.3em] uppercase mb-4">Your Destiny City</p>
          <h1 class="text-4xl md:text-5xl font-bold text-white mb-2 tracking-wider">
            {{ result.city.name }}
          </h1>
          <p class="text-gray-500 text-sm">{{ result.city.country }}</p>
        </div>
      </Transition>

      <!-- Score -->
      <Transition name="fade-up" appear>
        <div class="text-center mb-10" style="transition-delay: 0.15s">
          <div class="inline-flex items-baseline gap-1">
            <span class="text-5xl md:text-6xl font-bold text-white font-mono">
              {{ displayScore }}
            </span>
            <span class="text-2xl text-gray-500 font-light">%</span>
          </div>
          <p class="text-gray-600 text-xs mt-1 tracking-wider">灵魂共振指数</p>
        </div>
      </Transition>

      <!-- ====== ATTRIBUTE TAGS ====== -->
      <Transition name="fade-up" appear>
        <div class="flex flex-wrap justify-center gap-2 mb-10" style="transition-delay: 0.25s">
          <span class="px-3 py-1.5 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-100">
            {{ result.city.wuxing }}行 · {{ result.city.element }}
          </span>
          <span class="px-3 py-1.5 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-100">
            ♈ {{ result.city.zodiac }}
          </span>
          <span class="px-3 py-1.5 rounded-full text-xs font-medium bg-teal-50 text-teal-700 border border-teal-100">
            🃏 {{ result.city.tarot }}
          </span>
          <span class="px-3 py-1.5 rounded-full text-xs font-medium bg-pink-50 text-pink-700 border border-pink-100">
            ⚡ {{ result.city.energy_type }}
          </span>
        </div>
      </Transition>

      <!-- ====== REPORT SECTIONS (when report exists) ====== -->
      <template v-if="report">

        <!-- Section 1: Destiny Summary -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.3s">
            <div class="bg-white rounded-2xl shadow-card p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">✦</span>
                <h2 class="text-gray-900 font-bold text-base">命运总览</h2>
              </div>
              <p class="text-gray-600 text-sm leading-[1.9]">{{ report.destiny_summary }}</p>
            </div>
          </section>
        </Transition>

        <!-- Section 2: Energy Profile (Radar-like display) -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.35s">
            <div class="bg-white rounded-2xl shadow-card p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">◉</span>
                <h2 class="text-gray-900 font-bold text-base">灵魂能量画像</h2>
              </div>
              <p class="text-gray-400 text-xs mb-5">你的10维能量频率分布</p>
              <!-- Top 3 Highlights -->
              <div class="grid grid-cols-3 gap-3 mb-6">
                <div
                  v-for="(dim, idx) in report.top_dimensions"
                  :key="dim.dimension"
                  class="text-center p-3 rounded-xl"
                  :class="idx === 0 ? 'bg-gray-900 text-white' : 'bg-gray-50'"
                >
                  <div class="text-xl mb-1">{{ dim.icon }}</div>
                  <div class="font-bold text-lg" :class="idx === 0 ? 'text-white' : 'text-gray-900'">{{ dim.value }}%</div>
                  <div class="text-xs mt-0.5" :class="idx === 0 ? 'text-gray-300' : 'text-gray-500'">{{ dim.label }}</div>
                </div>
              </div>
              <!-- Full Profile Bars -->
              <div class="space-y-3">
                <div v-for="dim in report.energy_profile" :key="dim.dimension" class="flex items-center gap-3">
                  <span class="w-5 text-center text-sm flex-shrink-0">{{ dim.icon }}</span>
                  <span class="text-xs text-gray-500 w-16 flex-shrink-0">{{ dim.label }}</span>
                  <div class="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all duration-1000 ease-out"
                      :class="dim.value > 60 ? 'bg-gray-900' : dim.value > 30 ? 'bg-gray-500' : 'bg-gray-300'"
                      :style="{ width: dim.value + '%' }"
                    ></div>
                  </div>
                  <span class="text-xs text-gray-400 w-8 text-right font-mono">{{ dim.value }}</span>
                </div>
              </div>
            </div>
          </section>
        </Transition>

        <!-- Section 3: Element Analysis -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.4s">
            <div class="bg-white rounded-2xl shadow-card overflow-hidden">
              <div class="p-6">
                <div class="flex items-center gap-2 mb-1">
                  <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">{{ elementIcon }}</span>
                  <h2 class="text-gray-900 font-bold text-base">元素属性解析</h2>
                </div>
                <p class="text-amber-600 text-sm font-medium mb-4 ml-8">{{ report.element_analysis.title }}</p>
                <div class="space-y-4">
                  <div>
                    <p class="text-gray-400 text-xs tracking-wider mb-1.5">核心特质</p>
                    <p class="text-gray-600 text-sm leading-[1.8]">{{ report.element_analysis.core }}</p>
                  </div>
                  <div>
                    <p class="text-gray-400 text-xs tracking-wider mb-1.5">✦ 你的光面</p>
                    <p class="text-gray-600 text-sm leading-[1.8]">{{ report.element_analysis.strengths }}</p>
                  </div>
                  <div>
                    <p class="text-gray-400 text-xs tracking-wider mb-1.5">✧ 你的暗面</p>
                    <p class="text-gray-600 text-sm leading-[1.8]">{{ report.element_analysis.shadow }}</p>
                  </div>
                  <div class="pt-3 border-t border-gray-100">
                    <p class="text-gray-400 text-xs tracking-wider mb-1.5">↳ 城市连接</p>
                    <p class="text-gray-600 text-sm leading-[1.8]">{{ report.element_analysis.city_connection }}</p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </Transition>

        <!-- Section 4: Zodiac Analysis -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.45s">
            <div class="bg-white rounded-2xl shadow-card p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">☽</span>
                <h2 class="text-gray-900 font-bold text-base">星座能量解析</h2>
              </div>
              <div class="flex flex-wrap gap-2 mb-4">
                <span class="px-2.5 py-1 rounded-lg text-xs bg-purple-50 text-purple-700 border border-purple-100">
                  {{ report.zodiac_analysis.zodiac }}
                </span>
                <span class="px-2.5 py-1 rounded-lg text-xs bg-gray-50 text-gray-600 border border-gray-100">
                  守护星: {{ report.zodiac_analysis.ruling_planet }}
                </span>
                <span class="px-2.5 py-1 rounded-lg text-xs bg-gray-50 text-gray-600 border border-gray-100">
                  {{ report.zodiac_analysis.quality }}宫
                </span>
                <span class="px-2.5 py-1 rounded-lg text-xs bg-amber-50 text-amber-700 border border-amber-100">
                  关键词: {{ report.zodiac_analysis.keyword }}
                </span>
              </div>
              <p class="text-gray-600 text-sm leading-[1.8]">{{ report.zodiac_analysis.analysis }}</p>
            </div>
          </section>
        </Transition>

        <!-- Section 5: Tarot Reading -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.5s">
            <div class="bg-white rounded-2xl shadow-card p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">🃏</span>
                <h2 class="text-gray-900 font-bold text-base">塔罗牌解读</h2>
              </div>
              <!-- Tarot card visual -->
              <div class="bg-gray-50 rounded-xl p-5 mb-4 text-center border border-gray-100">
                <p class="text-gray-400 text-xs tracking-widest mb-2">ARCANA {{ report.tarot_reading.number }}</p>
                <p class="text-2xl font-bold text-gray-900 mb-1">「{{ report.tarot_reading.card }}」</p>
                <p class="text-sm text-amber-600 font-medium mb-2">{{ report.tarot_reading.keyword }}</p>
                <p class="text-xs text-gray-500">{{ report.tarot_reading.upright }}</p>
              </div>
              <p class="text-gray-600 text-sm leading-[1.8]">{{ report.tarot_reading.analysis }}</p>
            </div>
          </section>
        </Transition>

        <!-- Section 6: Wuxing Analysis -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.55s">
            <div class="bg-white rounded-2xl shadow-card p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">☯</span>
                <h2 class="text-gray-900 font-bold text-base">五行命理解析</h2>
              </div>
              <div class="flex flex-wrap gap-2 mb-4">
                <span class="px-2.5 py-1 rounded-lg text-xs bg-amber-50 text-amber-700 border border-amber-100">
                  五行属{{ report.wuxing_analysis.wuxing }}
                </span>
                <span class="px-2.5 py-1 rounded-lg text-xs bg-gray-50 text-gray-600 border border-gray-100">
                  方位: {{ report.wuxing_analysis.direction }}
                </span>
                <span class="px-2.5 py-1 rounded-lg text-xs bg-gray-50 text-gray-600 border border-gray-100">
                  时令: {{ report.wuxing_analysis.season }}
                </span>
              </div>
              <div class="space-y-4">
                <div>
                  <p class="text-gray-400 text-xs tracking-wider mb-1.5">五行本质</p>
                  <p class="text-gray-600 text-sm leading-[1.8]">{{ report.wuxing_analysis.nature }}</p>
                </div>
                <div>
                  <p class="text-gray-400 text-xs tracking-wider mb-1.5">性格深析</p>
                  <p class="text-gray-600 text-sm leading-[1.8]">{{ report.wuxing_analysis.personality }}</p>
                </div>
                <div class="pt-3 border-t border-gray-100">
                  <p class="text-gray-400 text-xs tracking-wider mb-1.5">↳ 城市五行匹配</p>
                  <p class="text-gray-600 text-sm leading-[1.8]">{{ report.wuxing_analysis.city_match }}</p>
                </div>
              </div>
            </div>
          </section>
        </Transition>

        <!-- Section 7: Energy Type Reading -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.6s">
            <div class="bg-white rounded-2xl shadow-card p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">⚡</span>
                <h2 class="text-gray-900 font-bold text-base">能量频率解读</h2>
              </div>
              <div class="bg-gray-50 rounded-xl p-4 mb-4 border border-gray-100 text-center">
                <p class="text-gray-400 text-xs tracking-widest mb-1">YOUR FREQUENCY</p>
                <p class="text-lg font-bold text-gray-900">{{ report.energy_reading.type }}</p>
              </div>
              <p class="text-gray-600 text-sm leading-[1.8]">{{ report.energy_reading.analysis }}</p>
            </div>
          </section>
        </Transition>

        <!-- Section 8: Career Advice -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.65s">
            <div class="bg-white rounded-2xl shadow-card p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">◈</span>
                <h2 class="text-gray-900 font-bold text-base">职业发展指引</h2>
              </div>
              <div class="flex flex-wrap gap-2 mb-4">
                <span
                  v-for="tag in report.career_advice.tags"
                  :key="tag"
                  class="px-2.5 py-1 rounded-lg text-xs bg-teal-50 text-teal-700 border border-teal-100"
                >
                  {{ tag }}
                </span>
              </div>
              <p class="text-gray-600 text-sm leading-[1.8]">{{ report.career_advice.summary }}</p>
            </div>
          </section>
        </Transition>

        <!-- Section 9: City Description -->
        <Transition name="fade-up" appear>
          <section class="mb-6" style="transition-delay: 0.7s">
            <div class="bg-white rounded-2xl shadow-card p-6">
              <div class="flex items-center gap-2 mb-4">
                <span class="w-6 h-6 flex items-center justify-center rounded-full bg-gray-900 text-white text-xs">⌂</span>
                <h2 class="text-gray-900 font-bold text-base">城市灵魂档案</h2>
              </div>
              <p class="text-gray-400 text-xs tracking-wider mb-1">城市气质</p>
              <p class="text-gray-700 text-sm font-medium mb-3">{{ result.city.vibe }}</p>
              <p class="text-gray-600 text-sm leading-[1.8]">{{ report.city_description }}</p>
            </div>
          </section>
        </Transition>

      </template>

      <!-- ====== FALLBACK: old interpretation only ====== -->
      <template v-else>
        <Transition name="fade-up" appear>
          <div class="bg-white rounded-2xl shadow-card overflow-hidden mb-6" style="transition-delay: 0.3s">
            <div class="px-6 pt-6 pb-4">
              <p class="text-gray-400 text-xs tracking-wider mb-1">城市气质</p>
              <p class="text-gray-700 text-sm">{{ result.city.vibe }}</p>
            </div>
            <div class="px-6"><div class="w-full h-px bg-gray-100"></div></div>
            <div class="px-6 py-5">
              <p class="text-gray-400 text-xs tracking-wider mb-3">✦ 命运解读</p>
              <p class="text-gray-600 text-sm leading-[1.8]">{{ result.interpretation }}</p>
            </div>
          </div>
        </Transition>
      </template>

      <!-- ====== RUNNER-UPS ====== -->
      <Transition name="fade-up" appear>
        <div v-if="result.runner_ups.length" class="mb-8" style="transition-delay: 0.75s">
          <p class="text-gray-500 text-xs tracking-wider mb-3 px-1">其他缘分城市</p>
          <div class="space-y-2">
            <div
              v-for="ru in result.runner_ups"
              :key="ru.city.id"
              class="bg-white/5 border border-white/10 rounded-xl p-4 flex items-center justify-between"
            >
              <div>
                <span class="text-white text-sm font-medium">{{ ru.city.name }}</span>
                <span class="text-gray-600 text-xs ml-2">{{ ru.city.country }}</span>
              </div>
              <span class="text-gray-400 text-sm font-mono">{{ ru.score.toFixed(1) }}%</span>
            </div>
          </div>
        </div>
      </Transition>

      <!-- ====== SHARE PROGRESS ====== -->
      <Transition name="fade-up" appear>
        <div class="mb-6" style="transition-delay: 0.8s">
          <div class="bg-white/5 border border-white/10 rounded-2xl p-6">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-white text-sm font-medium">分享获取新邀请码</span>
              <span class="text-gray-500 text-xs">（{{ shareProgress.visitor_count }}/{{ shareProgress.required }}）</span>
            </div>
            <p class="text-gray-500 text-xs mb-4">分享链接给好友，集齐 {{ shareProgress.required }} 人点击即可获得新邀请码</p>

            <!-- Progress bar -->
            <div class="w-full h-2 bg-gray-800 rounded-full overflow-hidden mb-3">
              <div
                class="h-full rounded-full transition-all duration-700 ease-out"
                :class="shareProgress.completed ? 'bg-green-400' : 'bg-white'"
                :style="{ width: (shareProgress.visitor_count / shareProgress.required * 100) + '%' }"
              ></div>
            </div>

            <!-- Progress dots -->
            <div class="flex justify-between mb-4">
              <div
                v-for="i in shareProgress.required"
                :key="i"
                class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-mono transition-all duration-300"
                :class="i <= shareProgress.visitor_count
                  ? 'bg-white text-gray-900'
                  : 'bg-gray-800 text-gray-600 border border-gray-700'"
              >
                {{ i <= shareProgress.visitor_count ? '✓' : i }}
              </div>
            </div>

            <!-- Reward code -->
            <Transition name="fade">
              <div v-if="shareProgress.completed && shareProgress.reward_code" class="rounded-xl p-4 text-center" :class="shareProgress.reward_code_used ? 'bg-gray-500/10 border border-gray-500/30' : 'bg-green-500/10 border border-green-500/30'">
                <template v-if="shareProgress.reward_code_used">
                  <p class="text-gray-400 text-xs mb-2">该邀请码已被使用</p>
                  <p class="text-gray-500 text-lg font-mono tracking-[0.2em] font-bold line-through">{{ shareProgress.reward_code }}</p>
                  <p class="text-gray-600 text-xs mt-2">继续分享可以让更多朋友看到你的测试结果</p>
                </template>
                <template v-else>
                  <p class="text-green-400 text-xs mb-2">恭喜！已获得新邀请码</p>
                  <p class="text-white text-lg font-mono tracking-[0.2em] font-bold">{{ shareProgress.reward_code }}</p>
                  <button
                    @click="copyRewardCode"
                    class="mt-2 px-4 py-1.5 bg-green-500/20 border border-green-500/30 rounded-lg text-green-300 text-xs hover:bg-green-500/30 transition-colors"
                  >
                    {{ rewardCopied ? '✓ 已复制' : '复制邀请码' }}
                  </button>
                </template>
              </div>
            </Transition>
          </div>
        </div>
      </Transition>

      <!-- ====== ACTIONS ====== -->
      <Transition name="fade-up" appear>
        <div class="space-y-3" style="transition-delay: 0.85s">
          <button
            @click="copyShareLink"
            class="w-full py-3.5 bg-white text-gray-900 rounded-xl font-medium text-sm tracking-wider transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
          >
            {{ copied ? '✓ 已复制' : '复制分享链接' }}
          </button>
          <button
            @click="$router.push('/')"
            class="w-full py-3.5 bg-transparent border border-gray-700 text-gray-400 rounded-xl text-sm tracking-wider transition-all duration-200 hover:border-gray-500 hover:text-gray-300"
          >
            新的测试
          </button>
        </div>
      </Transition>

      <!-- Footer -->
      <div class="mt-12 text-center">
        <div class="w-12 h-px bg-gray-800 mx-auto mb-3"></div>
        <p class="text-gray-700 text-xs tracking-wider">✦ 你的天选城市 ✦</p>
      </div>
    </div>

    <!-- Error state -->
    <div v-else class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <p class="text-gray-500 mb-4">未找到测试结果</p>
        <button
          @click="$router.push('/')"
          class="px-6 py-2.5 bg-white text-gray-900 rounded-xl text-sm font-medium"
        >
          返回首页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getResult, getShareProgress } from '../api'
import type { MatchResult, FullReport } from '../types'

const route = useRoute()
const result = ref<MatchResult | null>(null)
const loading = ref(true)
const copied = ref(false)
const rewardCopied = ref(false)
const displayScore = ref(0)

const shareProgress = reactive({
  visitor_count: 0,
  required: 3,
  completed: false,
  reward_code: null as string | null,
  reward_code_used: false,
})

const report = computed<FullReport | undefined>(() => result.value?.report ?? undefined)

const elementIcon = computed(() => {
  const map: Record<string, string> = { '火': '🔥', '水': '💧', '风': '🌬', '土': '⛰', '木': '🌿' }
  return map[report.value?.element_analysis.element ?? ''] ?? '✦'
})

onMounted(async () => {
  const shareId = route.params.shareId as string

  const cached = sessionStorage.getItem('destiny_result')
  if (cached) {
    try {
      const parsed = JSON.parse(cached)
      if (parsed.share_id === shareId) {
        result.value = parsed
        sessionStorage.removeItem('destiny_result')
        loading.value = false
        animateScore(parsed.score)
        loadShareProgress(shareId)
        return
      }
    } catch {}
  }

  try {
    result.value = await getResult(shareId)
    animateScore(result.value.score)
    loadShareProgress(shareId)
  } catch {
    result.value = null
  } finally {
    loading.value = false
  }
})

async function loadShareProgress(shareId: string) {
  try {
    const progress = await getShareProgress(shareId)
    shareProgress.visitor_count = progress.visitor_count
    shareProgress.required = progress.required
    shareProgress.completed = progress.completed
    shareProgress.reward_code = progress.reward_code
    shareProgress.reward_code_used = progress.reward_code_used ?? false
  } catch {}
}

function animateScore(target: number) {
  const duration = 1500
  const start = performance.now()
  function update(now: number) {
    const elapsed = now - start
    const progress = Math.min(elapsed / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    displayScore.value = Math.round(eased * target)
    if (progress < 1) requestAnimationFrame(update)
  }
  requestAnimationFrame(update)
}

async function copyShareLink() {
  const url = `${window.location.origin}/share/${route.params.shareId}`
  try {
    await navigator.clipboard.writeText(url)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  } catch {
    const input = document.createElement('input')
    input.value = url
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  }
}

async function copyRewardCode() {
  if (!shareProgress.reward_code) return
  try {
    await navigator.clipboard.writeText(shareProgress.reward_code)
    rewardCopied.value = true
    setTimeout(() => (rewardCopied.value = false), 2000)
  } catch {
    const input = document.createElement('input')
    input.value = shareProgress.reward_code
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    rewardCopied.value = true
    setTimeout(() => (rewardCopied.value = false), 2000)
  }
}
</script>
