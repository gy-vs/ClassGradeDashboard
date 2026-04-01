import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/data',
    name: 'Data',
    component: () => import('@/views/Data.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
