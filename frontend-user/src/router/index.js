import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import DataManager from '../views/DataManager.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/data',
    name: 'DataManager',
    component: DataManager
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
