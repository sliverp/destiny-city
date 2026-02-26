import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'welcome',
      component: () => import('../views/WelcomePage.vue'),
    },
    {
      path: '/quiz',
      name: 'quiz',
      component: () => import('../views/QuizPage.vue'),
    },
    {
      path: '/result/:shareId',
      name: 'result',
      component: () => import('../views/ResultPage.vue'),
    },
    {
      path: '/share/:shareId',
      name: 'share',
      component: () => import('../views/SharePage.vue'),
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminPage.vue'),
    },
  ],
})

export default router
