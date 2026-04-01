<template>
  <div class="app-container">
    <header class="header">
      <div class="header-content">
        <div class="logo">
          <el-icon :size="32" color="#409EFF"><School /></el-icon>
          <h1>班级成绩分析看板</h1>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="section">
        <div class="section-title">数据导入</div>
        <DataImport @data-imported="loadData" />
      </div>

      <div class="section">
        <div class="section-title">班级概览</div>
        <OverviewCards :overview="overview" />
      </div>

      <div class="section">
        <div class="section-title">成绩统计图表</div>
        <ChartsView :statistics="statistics" :students="students" />
      </div>

      <div class="section">
        <div class="section-title">学生成绩排名</div>
        <StudentTable :students="students" @refresh="loadData" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import DataImport from './components/DataImport.vue'
import OverviewCards from './components/OverviewCards.vue'
import ChartsView from './components/ChartsView.vue'
import StudentTable from './components/StudentTable.vue'

const overview = ref({})
const statistics = ref({})
const students = ref([])

const loadData = async () => {
  try {
    const [statsRes, studentsRes] = await Promise.all([
      axios.get('/api/statistics'),
      axios.get('/api/students')
    ])
    overview.value = statsRes.data.overview
    statistics.value = statsRes.data
    students.value = studentsRes.data
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 40px;
  height: 70px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo h1 {
  font-size: 24px;
  font-weight: 600;
}

.main-content {
  flex: 1;
  padding: 24px 40px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

.section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
  padding-left: 12px;
  border-left: 4px solid #409EFF;
}
</style>
