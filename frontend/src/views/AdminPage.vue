<template>
  <div class="min-h-screen bg-bg">
    <!-- Top bar -->
    <div class="border-b border-white/5 px-6 py-4">
      <div class="max-w-2xl mx-auto flex items-center justify-between">
        <h1 class="text-white font-medium tracking-wider">管理后台</h1>
        <button
          v-if="authenticated"
          @click="logout"
          class="text-gray-500 text-xs hover:text-gray-300 transition-colors"
        >
          退出
        </button>
      </div>
    </div>

    <div class="max-w-2xl mx-auto px-4 py-8">
      <!-- Auth gate -->
      <div v-if="!authenticated" class="max-w-sm mx-auto mt-20">
        <div class="bg-white rounded-2xl shadow-card p-8">
          <h2 class="text-gray-900 text-lg font-medium mb-6 text-center">管理员认证</h2>
          <div class="mb-4">
            <label class="block text-xs text-gray-400 uppercase tracking-wider mb-2">API Key</label>
            <input
              v-model="adminKey"
              type="password"
              placeholder="请输入管理员密钥"
              class="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl text-gray-900 text-sm placeholder:text-gray-300 focus:outline-none focus:border-gray-900 transition-colors"
              @keyup.enter="authenticate"
            />
          </div>
          <button
            @click="authenticate"
            class="w-full py-3 bg-gray-900 text-white rounded-xl text-sm font-medium tracking-wider hover:-translate-y-0.5 hover:shadow-lg transition-all duration-200"
          >
            验证
          </button>
          <p v-if="authError" class="text-red-500 text-xs mt-3 text-center">{{ authError }}</p>
        </div>
      </div>

      <!-- Admin content -->
      <div v-else class="space-y-6">
        <!-- Generate card -->
        <div class="bg-white rounded-2xl shadow-card p-6">
          <h2 class="text-gray-900 font-medium mb-4">批量生成邀请码</h2>
          <div class="flex gap-3">
            <div class="flex-1">
              <input
                v-model.number="generateCount"
                type="number"
                min="1"
                max="100"
                placeholder="数量"
                class="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-gray-900 text-sm focus:outline-none focus:border-gray-900 transition-colors"
              />
            </div>
            <button
              @click="generate"
              :disabled="generating"
              class="px-6 py-2.5 bg-gray-900 text-white rounded-xl text-sm font-medium tracking-wider hover:-translate-y-0.5 hover:shadow-lg transition-all duration-200 disabled:opacity-50"
            >
              {{ generating ? '生成中...' : '生成' }}
            </button>
          </div>

          <!-- Generated codes -->
          <Transition name="fade-up">
            <div v-if="newCodes.length" class="mt-4 p-4 bg-gray-50 rounded-xl">
              <div class="flex items-center justify-between mb-2">
                <p class="text-xs text-gray-500">新生成的邀请码</p>
                <button @click="copyAllCodes" class="text-xs text-gray-500 hover:text-gray-900 transition-colors">
                  {{ copiedAll ? '✓ 已复制' : '复制全部' }}
                </button>
              </div>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="code in newCodes"
                  :key="code"
                  class="px-3 py-1 bg-white border border-gray-200 rounded-lg text-sm font-mono text-gray-900 cursor-pointer hover:border-gray-400 transition-colors"
                  @click="copySingle(code)"
                  title="点击复制"
                >
                  {{ code }}
                </span>
              </div>
            </div>
          </Transition>
        </div>

        <!-- Stats -->
        <div class="grid grid-cols-3 gap-3">
          <div class="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
            <p class="text-2xl font-bold text-white font-mono">{{ totalCodes }}</p>
            <p class="text-gray-500 text-xs mt-1">总计</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
            <p class="text-2xl font-bold text-green-400 font-mono">{{ availableCodes }}</p>
            <p class="text-gray-500 text-xs mt-1">可用</p>
          </div>
          <div class="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
            <p class="text-2xl font-bold text-gray-500 font-mono">{{ usedCodes }}</p>
            <p class="text-gray-500 text-xs mt-1">已使用</p>
          </div>
        </div>

        <!-- Filter -->
        <div class="flex gap-2">
          <button
            v-for="f in filters"
            :key="f.value"
            @click="currentFilter = f.value"
            class="px-4 py-1.5 rounded-lg text-xs transition-all duration-200"
            :class="currentFilter === f.value
              ? 'bg-white text-gray-900'
              : 'bg-white/5 text-gray-500 hover:text-white'"
          >
            {{ f.label }}
          </button>
        </div>

        <!-- Codes list -->
        <div class="bg-white rounded-2xl shadow-card overflow-hidden">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-50 text-xs text-gray-400 uppercase tracking-wider">
                <th class="text-left px-6 py-3">邀请码</th>
                <th class="text-left px-6 py-3">状态</th>
                <th class="text-left px-6 py-3 hidden sm:table-cell">使用者</th>
                <th class="text-left px-6 py-3 hidden sm:table-cell">时间</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="inv in filteredCodes"
                :key="inv.id"
                class="border-t border-gray-50 hover:bg-gray-50/50 transition-colors"
              >
                <td class="px-6 py-3 font-mono text-sm text-gray-900">{{ inv.code }}</td>
                <td class="px-6 py-3">
                  <span
                    class="px-2 py-0.5 rounded-full text-xs font-medium"
                    :class="inv.is_used
                      ? 'bg-gray-100 text-gray-500'
                      : 'bg-green-50 text-green-600 border border-green-100'"
                  >
                    {{ inv.is_used ? '已使用' : '可用' }}
                  </span>
                </td>
                <td class="px-6 py-3 text-xs text-gray-400 hidden sm:table-cell">
                  {{ inv.used_by || '—' }}
                </td>
                <td class="px-6 py-3 text-xs text-gray-400 hidden sm:table-cell">
                  {{ inv.used_at ? new Date(inv.used_at).toLocaleString('zh-CN') : '—' }}
                </td>
              </tr>
              <tr v-if="!filteredCodes.length">
                <td colspan="4" class="px-6 py-8 text-center text-gray-400 text-sm">暂无数据</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { generateInviteCodes, getInviteCodes } from '../api'
import type { InviteCode } from '../types'

const adminKey = ref('')
const authenticated = ref(false)
const authError = ref('')
const generateCount = ref(10)
const generating = ref(false)
const newCodes = ref<string[]>([])
const copiedAll = ref(false)
const allCodes = ref<InviteCode[]>([])
const currentFilter = ref('all')

const filters = [
  { label: '全部', value: 'all' },
  { label: '可用', value: 'available' },
  { label: '已使用', value: 'used' },
]

const totalCodes = computed(() => allCodes.value.length)
const availableCodes = computed(() => allCodes.value.filter(c => !c.is_used).length)
const usedCodes = computed(() => allCodes.value.filter(c => c.is_used).length)

const filteredCodes = computed(() => {
  if (currentFilter.value === 'available') return allCodes.value.filter(c => !c.is_used)
  if (currentFilter.value === 'used') return allCodes.value.filter(c => c.is_used)
  return allCodes.value
})

async function authenticate() {
  authError.value = ''
  try {
    await getInviteCodes(adminKey.value)
    authenticated.value = true
    loadCodes()
  } catch {
    authError.value = '密钥错误'
  }
}

function logout() {
  authenticated.value = false
  adminKey.value = ''
  allCodes.value = []
}

async function loadCodes() {
  try {
    allCodes.value = await getInviteCodes(adminKey.value)
  } catch {}
}

async function generate() {
  generating.value = true
  try {
    const res = await generateInviteCodes(adminKey.value, generateCount.value)
    newCodes.value = res.codes
    await loadCodes()
  } catch (e: any) {
    alert(e?.response?.data?.detail || '生成失败')
  } finally {
    generating.value = false
  }
}

async function copyAllCodes() {
  try {
    await navigator.clipboard.writeText(newCodes.value.join('\n'))
    copiedAll.value = true
    setTimeout(() => (copiedAll.value = false), 2000)
  } catch {}
}

async function copySingle(code: string) {
  try {
    await navigator.clipboard.writeText(code)
  } catch {}
}
</script>
