<template>
  <div class="min-h-screen bg-bg flex flex-col items-center justify-center px-4 relative overflow-hidden">
    <!-- Subtle background decoration -->
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-white/[0.02] blur-3xl"></div>
      <div class="absolute bottom-1/3 right-1/4 w-96 h-96 rounded-full bg-white/[0.01] blur-3xl"></div>
    </div>

    <!-- Title area -->
    <div class="text-center mb-10 relative z-10">
      <h1 class="text-4xl md:text-5xl font-bold text-white tracking-wider mb-4">
        你的天选城市
      </h1>
      <p class="text-gray-500 text-sm md:text-base tracking-widest font-light">
        宇宙已为你标记了一座城市...
      </p>
    </div>

    <!-- Main card -->
    <div class="w-full max-w-md relative z-10">
      <div class="bg-white rounded-2xl shadow-card p-8 md:p-10 transition-shadow duration-300 hover:shadow-card-hover">
        <!-- Error message -->
        <Transition name="fade">
          <div v-if="errorMsg" class="mb-5 p-3 rounded-lg bg-red-50 border border-red-100">
            <p class="text-red-500 text-sm text-center">{{ errorMsg }}</p>
          </div>
        </Transition>

        <!-- Invite code input -->
        <div class="mb-6">
          <label class="block text-xs text-gray-400 uppercase tracking-wider mb-2 font-medium">
            邀请码
          </label>
          <input
            v-model="inviteCode"
            type="text"
            placeholder="请输入 12 位邀请码（区分大小写）"
            maxlength="12"
            class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-gray-900 text-center text-lg tracking-[0.2em] font-mono placeholder:text-gray-300 placeholder:tracking-normal placeholder:text-sm placeholder:font-sans focus:outline-none focus:border-gray-900 transition-colors duration-200"
            :disabled="loading"
            @keyup.enter="handleVerify"
          />
        </div>

        <!-- Submit button -->
        <button
          @click="handleVerify"
          :disabled="loading || inviteCode.length < 1"
          class="w-full py-3.5 bg-gray-900 text-white rounded-xl font-medium text-sm tracking-wider transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:translate-y-0"
        >
          <span v-if="!loading">开启命运之旅</span>
          <span v-else class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            正在验证...
          </span>
        </button>

        <!-- 购买邀请码链接 -->
        <div class="mt-4 text-center">
          <a
            :href="buyLink"
            target="_blank"
            rel="noopener noreferrer"
            class="text-gray-400 text-xs hover:text-gray-600 transition-colors underline underline-offset-4"
          >
            还没有邀请码？点击获取
          </a>
        </div>
      </div>

      <!-- Helper links -->
      <div class="mt-8 text-center space-y-3">
        <p class="text-gray-600 text-xs">
          查看好友的测试结果？
          <button @click="showShareInput = !showShareInput" class="text-white underline underline-offset-4 hover:no-underline transition-all ml-1">
            输入分享链接
          </button>
        </p>

        <Transition name="fade-up">
          <div v-if="showShareInput" class="mt-3">
            <div class="flex gap-2 max-w-xs mx-auto">
              <input
                v-model="shareId"
                type="text"
                placeholder="输入分享 ID"
                class="flex-1 px-3 py-2 bg-white/5 border border-gray-700 rounded-lg text-white text-sm placeholder:text-gray-600 focus:outline-none focus:border-gray-500 transition-colors"
              />
              <button
                @click="goToShare"
                class="px-4 py-2 bg-white/10 border border-gray-700 rounded-lg text-white text-sm hover:bg-white/20 transition-colors"
              >
                查看
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Footer -->
    <div class="absolute bottom-6 text-center">
      <div class="w-16 h-px bg-gray-800 mx-auto mb-3"></div>
      <p class="text-gray-700 text-xs tracking-wider">✦ 星辰指引你的归属之地 ✦</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { verifyInviteCode } from '../api'

const router = useRouter()
const inviteCode = ref('')
const loading = ref(false)
const errorMsg = ref('')
const showShareInput = ref(false)
const shareId = ref('')

// 发货平台链接（待替换为实际链接）
const buyLink = ref('https://p.goofish.com/p/CcrqpKfu')

async function handleVerify() {
  if (!inviteCode.value.trim()) return
  loading.value = true
  errorMsg.value = ''

  try {
    const res = await verifyInviteCode(inviteCode.value.trim())
    if (res.valid) {
      if (res.share_id) {
        // 已使用的邀请码，跳转到报告页
        router.push(`/result/${res.share_id}`)
      } else {
        // 新邀请码，进入测试
        sessionStorage.setItem('destiny_token', res.token)
        router.push('/quiz')
      }
    } else {
      errorMsg.value = res.message || '邀请码无效'
    }
  } catch (e: any) {
    errorMsg.value = e?.response?.data?.detail || '验证失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

function goToShare() {
  if (shareId.value.trim()) {
    router.push(`/share/${shareId.value.trim()}`)
  }
}
</script>
