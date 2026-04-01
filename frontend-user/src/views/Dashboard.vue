<template>
  <div class="dashboard">
    <h1 class="page-title">统计看板</h1>
    
    <div class="overview-cards">
      <div class="stat-card blue">
        <div class="stat-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">总人数</p>
          <p class="stat-value">{{ overview.total_students }}</p>
        </div>
      </div>
      <div class="stat-card purple">
        <div class="stat-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">平均分</p>
          <p class="stat-value">{{ overview.average }}</p>
        </div>
      </div>
      <div class="stat-card green">
        <div class="stat-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">及格率</p>
          <p class="stat-value">{{ overview.pass_rate }}%</p>
        </div>
      </div>
      <div class="stat-card orange">
        <div class="stat-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
        </div>
        <div class="stat-content">
          <p class="stat-label">优秀率</p>
          <p class="stat-value">{{ overview.excellent_rate }}%</p>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card">
        <h2 class="card-title">各科成绩对比</h2>
        <div ref="barChartRef" class="chart"></div>
      </div>
      <div class="card chart-card">
        <h2 class="card-title">分数段分布</h2>
        <div ref="pieChartRef" class="chart"></div>
      </div>
    </div>

    <div class="card">
      <div class="table-header">
        <h2 class="card-title">学生成绩排名</h2>
        <input v-model="searchKeyword" type="text" placeholder="搜索学生姓名..." class="search-input" />
      </div>
      <div class="table-wrapper">
        <table class="rank-table">
          <thead>
            <tr>
              <th @click="sortBy('rank')" class="sortable">排名</th>
              <th @click="sortBy('姓名')" class="sortable">姓名</th>
              <th v-for="s in subjects" :key="s" @click="sortBy(s)" class="sortable">{{ s }}</th>
              <th @click="sortBy('总分')" class="sortable">总分</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in sortedRankings" :key="idx" :class="{ even: idx % 2 === 1, medal: idx < 3 }">
              <td class="rank">
                <span v-if="idx === 0" class="medal gold">🥇</span>
                <span v-else-if="idx === 1" class="medal silver">🥈</span>
                <span v-else-if="idx === 2" class="medal bronze">🥉</span>
                <span v-else>{{ idx + 1 }}</span>
              </td>
              <td>{{ row.姓名 }}</td>
              <td v-for="s in subjects" :key="s">{{ row[s] || '-' }}</td>
              <td class="total">{{ row.总分 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import * as echarts from 'echarts'
import { getStatistics, getRankings, getDistribution } from '@/api'

const subjects = ['语文', '数学', '英语', '物理', '化学']
const overview = ref({
  total_students: 0,
  average: 0,
  pass_rate: 0,
  excellent_rate: 0
})
const rankings = ref([])
const distribution = ref(null)
const barChartRef = ref(null)
const pieChartRef = ref(null)
const searchKeyword = ref('')
const sortField = ref('总分')
const sortOrder = ref('desc')

const colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']

const sortedRankings = computed(() => {
  let result = [...rankings.value]
  if (searchKeyword.value) {
    result = result.filter(r => r.姓名.includes(searchKeyword.value))
  }
  result.sort((a, b) => {
    const aVal = a[sortField.value] || 0
    const bVal = b[sortField.value] || 0
    return sortOrder.value === 'asc' ? aVal - bVal : bVal - aVal
  })
  return result
})

const sortBy = (field) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'desc'
  }
}

const initBarChart = () => {
  if (!barChartRef.value || !overview.value) return
  const chart = echarts.init(barChartRef.value)
  const data = subjects.map(s => overview.value.subjects[s]?.平均分 || 0)
  
  chart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { top: 0, data: ['平均分'] },
    grid: { top: 50, left: 50, right: 30, bottom: 30 },
    xAxis: { type: 'category', data: subjects },
    yAxis: { type: 'value', min: 0, max: 100 },
    series: [{
      name: '平均分',
      type: 'bar',
      data: data,
      itemStyle: {
        borderRadius: [8, 8, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#667eea' },
          { offset: 1, color: '#764ba2' }
        ])
      },
      barWidth: 50
    }]
  })
}

const initPieChart = () => {
  if (!pieChartRef.value || !distribution.value) return
  const chart = echarts.init(pieChartRef.value)
  const ranges = ['0-59', '60-69', '70-79', '80-89', '90-100']
  const total = {}
  ranges.forEach(r => total[r] = 0)
  
  subjects.forEach(s => {
    ranges.forEach(r => {
      total[r] += distribution.value[s]?.[r] || 0
    })
  })
  
  const data = ranges.map(r => ({ name: r, value: total[r] }))
  
  chart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { orient: 'vertical', left: 10, top: 'center' },
    grid: { top: 30, left: 100, right: 30, bottom: 30 },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['60%', '50%'],
      data: data,
      color: colors,
      label: { formatter: '{b}: {d}%' }
    }]
  })
}

const loadData = async () => {
  const [statsRes, rankingsRes, distRes] = await Promise.all([
    getStatistics(),
    getRankings(),
    getDistribution()
  ])
  if (statsRes.data.overview) {
    overview.value = {
      total_students: statsRes.data.overview.total_students,
      average: statsRes.data.overview.average,
      pass_rate: statsRes.data.overview.pass_rate,
      excellent_rate: statsRes.data.overview.excellent_rate
    }
  }
  rankings.value = rankingsRes.data.data
  distribution.value = distRes.data
  
  setTimeout(() => {
    initBarChart()
    initPieChart()
  }, 100)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 24px;
  color: #1a202c;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.stat-card {
  padding: 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  color: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stat-card.blue {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-card.purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card.green {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.stat-card.orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
  margin-top: 4px;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.chart-card {
  min-height: 400px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #2d3748;
}

.chart {
  width: 100%;
  height: 320px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.search-input {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  width: 200px;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.table-wrapper {
  overflow-x: auto;
}

.rank-table {
  width: 100%;
  border-collapse: collapse;
}

.rank-table th {
  text-align: left;
  padding: 12px 16px;
  background: #f7fafc;
  font-weight: 600;
  color: #2d3748;
  border-bottom: 2px solid #e2e8f0;
  cursor: pointer;
  user-select: none;
}

.rank-table th.sortable:hover {
  background: #edf2f7;
}

.rank-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.rank-table tr.even {
  background: #f7fafc;
}

.rank-table tr.medal {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.05) 0%, transparent 100%);
  font-weight: 500;
}

.rank {
  font-weight: 600;
  width: 60px;
}

.medal {
  font-size: 20px;
}

.total {
  font-weight: 600;
  color: #667eea;
}
</style>
