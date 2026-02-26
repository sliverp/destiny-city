<template>
  <div class="min-h-screen bg-bg">
    <!-- Loading -->
    <div v-if="loading" class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <div class="animate-spin w-8 h-8 border-2 border-white/20 border-t-white rounded-full mx-auto mb-4"></div>
        <p class="text-gray-500 text-sm">加载中...</p>
      </div>
    </div>

    <!-- Share content -->
    <div v-else-if="result" class="max-w-lg mx-auto px-4 py-12">
      <!-- Header -->
      <div class="text-center mb-3">
        <p class="text-gray-600 text-xs tracking-wider">✦ 你的天选城市 ✦</p>
      </div>
      <div class="text-center mb-8">
        <p class="text-gray-500 text-xs tracking-wider mb-2">来自好友的分享</p>
        <div class="w-8 h-px bg-gray-700 mx-auto"></div>
      </div>

      <!-- City title -->
      <div class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-white mb-1">{{ result.city.name }}</h1>
        <p class="text-gray-500 text-sm">{{ result.city.country }}</p>
        <p class="text-white text-2xl font-mono mt-3">{{ result.score.toFixed(1) }}%</p>
        <p class="text-gray-600 text-xs mt-0.5">灵魂共振指数</p>
      </div>

      <!-- Tags -->
      <div class="flex flex-wrap justify-center gap-2 mb-8">
        <span class="px-3 py-1 rounded-full text-xs font-medium bg-amber-50 text-amber-700 border border-amber-100">
          {{ result.city.wuxing }}行 · {{ result.city.element }}
        </span>
        <span class="px-3 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700 border border-purple-100">
          ♈ {{ result.city.zodiac }}
        </span>
        <span class="px-3 py-1 rounded-full text-xs font-medium bg-teal-50 text-teal-700 border border-teal-100">
          🃏 {{ result.city.tarot }}
        </span>
        <span class="px-3 py-1 rounded-full text-xs font-medium bg-pink-50 text-pink-700 border border-pink-100">
          ⚡ {{ result.city.energy_type }}
        </span>
      </div>

      <!-- Full Report (when available) -->
      <template v-if="report">
        <!-- Destiny Summary -->
        <div class="bg-white rounded-2xl shadow-card p-6 mb-5">
          <div class="flex items-center gap-2 mb-3">
            <span class="w-5 h-5 flex items-center justify-center rounded-full bg-gray-900 text-white text-[10px]">✦</span>
            <h2 class="text-gray-900 font-bold text-sm">命运总览</h2>
          </div>
          <p class="text-gray-600 text-sm leading-[1.8]">{{ report.destiny_summary }}</p>
        </div>

        <!-- Energy Profile -->
        <div class="bg-white rounded-2xl shadow-card p-6 mb-5">
          <div class="flex items-center gap-2 mb-3">
            <span class="w-5 h-5 flex items-center justify-center rounded-full bg-gray-900 text-white text-[10px]">◉</span>
            <h2 class="text-gray-900 font-bold text-sm">灵魂能量画像</h2>
          </div>
          <div class="grid grid-cols-3 gap-2 mb-5">
            <div
              v-for="(dim, idx) in report.top_dimensions"
              :key="dim.dimension"
              class="text-center p-2.5 rounded-xl"
              :class="idx === 0 ? 'bg-gray-900 text-white' : 'bg-gray-50'"
            >
              <div class="text-lg mb-0.5">{{ dim.icon }}</div>
              <div class="font-bold text-base" :class="idx === 0 ? 'text-white' : 'text-gray-900'">{{ dim.value }}%</div>
              <div class="text-[10px] mt-0.5" :class="idx === 0 ? 'text-gray-300' : 'text-gray-500'">{{ dim.label }}</div>
            </div>
          </div>
          <div class="space-y-2.5">
            <div v-for="dim in report.energy_profile" :key="dim.dimension" class="flex items-center gap-2">
              <span class="w-4 text-center text-xs flex-shrink-0">{{ dim.icon }}</span>
              <span class="text-[10px] text-gray-500 w-14 flex-shrink-0">{{ dim.label }}</span>
              <div class="flex-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full"
                  :class="dim.value > 60 ? 'bg-gray-900' : dim.value > 30 ? 'bg-gray-500' : 'bg-gray-300'"
                  :style="{ width: dim.value + '%' }"
                ></div>
              </div>
              <span class="text-[10px] text-gray-400 w-6 text-right font-mono">{{ dim.value }}</span>
            </div>
          </div>
        </div>

        <!-- Element Analysis (compact) -->
        <div class="bg-white rounded-2xl shadow-card p-6 mb-5">
          <div class="flex items-center gap-2 mb-1">
            <span class="w-5 h-5 flex items-center justify-center rounded-full bg-gray-900 text-white text-[10px]">{{ elementIcon }}</span>
            <h2 class="text-gray-900 font-bold text-sm">元素属性解析</h2>
          </div>
          <p class="text-amber-600 text-xs font-medium mb-3 ml-7">{{ report.element_analysis.title }}</p>
          <p class="text-gray-600 text-sm leading-[1.8] mb-3">{{ report.element_analysis.core }}</p>
          <div class="pt-3 border-t border-gray-100">
            <p class="text-gray-400 text-[10px] tracking-wider mb-1">↳ 城市连接</p>
            <p class="text-gray-600 text-sm leading-[1.8]">{{ report.element_analysis.city_connection }}</p>
          </div>
        </div>

        <!-- Tarot Reading (compact) -->
        <div class="bg-white rounded-2xl shadow-card p-6 mb-5">
          <div class="flex items-center gap-2 mb-3">
            <span class="w-5 h-5 flex items-center justify-center rounded-full bg-gray-900 text-white text-[10px]">🃏</span>
            <h2 class="text-gray-900 font-bold text-sm">塔罗牌解读</h2>
          </div>
          <div class="bg-gray-50 rounded-xl p-4 mb-3 text-center border border-gray-100">
            <p class="text-gray-400 text-[10px] tracking-widest mb-1">ARCANA {{ report.tarot_reading.number }}</p>
            <p class="text-xl font-bold text-gray-900 mb-0.5">「{{ report.tarot_reading.card }}」</p>
            <p class="text-xs text-amber-600 font-medium">{{ report.tarot_reading.keyword }}</p>
          </div>
          <p class="text-gray-600 text-sm leading-[1.8]">{{ report.tarot_reading.analysis }}</p>
        </div>

        <!-- Wuxing (compact) -->
        <div class="bg-white rounded-2xl shadow-card p-6 mb-5">
          <div class="flex items-center gap-2 mb-3">
            <span class="w-5 h-5 flex items-center justify-center rounded-full bg-gray-900 text-white text-[10px]">☯</span>
            <h2 class="text-gray-900 font-bold text-sm">五行命理解析</h2>
          </div>
          <div class="flex flex-wrap gap-1.5 mb-3">
            <span class="px-2 py-0.5 rounded text-[10px] bg-amber-50 text-amber-700">五行属{{ report.wuxing_analysis.wuxing }}</span>
            <span class="px-2 py-0.5 rounded text-[10px] bg-gray-50 text-gray-600">{{ report.wuxing_analysis.direction }}方</span>
            <span class="px-2 py-0.5 rounded text-[10px] bg-gray-50 text-gray-600">{{ report.wuxing_analysis.season }}</span>
          </div>
          <p class="text-gray-600 text-sm leading-[1.8] mb-3">{{ report.wuxing_analysis.personality }}</p>
          <div class="pt-3 border-t border-gray-100">
            <p class="text-gray-400 text-[10px] tracking-wider mb-1">↳ 城市五行匹配</p>
            <p class="text-gray-600 text-sm leading-[1.8]">{{ report.wuxing_analysis.city_match }}</p>
          </div>
        </div>

        <!-- Energy Reading (compact) -->
        <div class="bg-white rounded-2xl shadow-card p-6 mb-5">
          <div class="flex items-center gap-2 mb-3">
            <span class="w-5 h-5 flex items-center justify-center rounded-full bg-gray-900 text-white text-[10px]">⚡</span>
            <h2 class="text-gray-900 font-bold text-sm">能量频率</h2>
          </div>
          <p class="text-gray-900 text-sm font-bold mb-2">{{ report.energy_reading.type }}</p>
          <p class="text-gray-600 text-sm leading-[1.8]">{{ report.energy_reading.analysis }}</p>
        </div>

        <!-- Career Advice (compact) -->
        <div class="bg-white rounded-2xl shadow-card p-6 mb-5">
          <div class="flex items-center gap-2 mb-3">
            <span class="w-5 h-5 flex items-center justify-center rounded-full bg-gray-900 text-white text-[10px]">◈</span>
            <h2 class="text-gray-900 font-bold text-sm">职业发展指引</h2>
          </div>
          <div class="flex flex-wrap gap-1.5 mb-3">
            <span v-for="tag in report.career_advice.tags" :key="tag" class="px-2 py-0.5 rounded text-[10px] bg-teal-50 text-teal-700">
              {{ tag }}
            </span>
          </div>
          <p class="text-gray-600 text-sm leading-[1.8]">{{ report.career_advice.summary }}</p>
        </div>
      </template>

      <!-- Fallback: old-style interpretation -->
      <template v-else>
        <div class="bg-white rounded-2xl shadow-card overflow-hidden mb-6">
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
      </template>

      <!-- CTA -->
      <div class="bg-white/5 border border-white/10 rounded-2xl p-6 text-center mb-6">
        <p class="text-white text-base font-medium mb-2">也想知道你的天选城市？</p>
        <p class="text-gray-500 text-xs mb-5">获取邀请码，开启属于你的命运测试</p>
        <button
          @click="$router.push('/')"
          class="px-8 py-3 bg-white text-gray-900 rounded-xl font-medium text-sm tracking-wider transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg"
        >
          开始测试
        </button>
      </div>

      <!-- Footer -->
      <div class="mt-8 text-center">
        <div class="w-12 h-px bg-gray-800 mx-auto mb-3"></div>
        <p class="text-gray-700 text-xs tracking-wider">✦ 星辰指引你的归属之地 ✦</p>
      </div>
    </div>

    <!-- Not found -->
    <div v-else class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <p class="text-gray-500 mb-4">未找到该分享结果</p>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getResult, recordShareVisit } from '../api'
import type { MatchResult, FullReport } from '../types'

const route = useRoute()
const result = ref<MatchResult | null>(null)
const loading = ref(true)

const report = computed<FullReport | undefined>(() => result.value?.report ?? undefined)

const elementIcon = computed(() => {
  const map: Record<string, string> = { '火': '🔥', '水': '💧', '风': '🌬', '土': '⛰', '木': '🌿' }
  return map[report.value?.element_analysis.element ?? ''] ?? '✦'
})

function ensureVisitorCookie() {
  if (!document.cookie.includes('visitor_id=')) {
    const id = crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2) + Date.now().toString(36)
    document.cookie = `visitor_id=${id}; path=/; max-age=${10 * 365 * 24 * 3600}; samesite=lax`
  }
}

onMounted(async () => {
  const shareId = route.params.shareId as string
  ensureVisitorCookie()

  try {
    result.value = await getResult(shareId)
    // 记录访问（后端会自动去重）
    await recordShareVisit(shareId).catch(() => {})
  } catch {
    result.value = null
  } finally {
    loading.value = false
  }
})
</script>
