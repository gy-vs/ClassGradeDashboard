<template>
  <div class="container">
    <div class="page-header">
      <h1>成绩分析看板</h1>
      <p class="page-desc">全面展示班级成绩数据，多维度分析学生学习情况</p>
    </div>

    <div class="overview-cards">
      <div class="overview-card card-blue">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <div class="card-content">
          <p class="card-label">总人数</p>
          <p class="card-value">{{ overview.总人数 || 0 }}</p>
          <p class="card-desc">学生总数</p>
        </div>
      </div>
      <div class="overview-card card-orange">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <div class="card-content">
          <p class="card-label">总平均分</p>
          <p class="card-value">{{ overview.总平均分 || 0 }}<span class="unit">分</span></p>
          <p class="card-desc">所有科目平均</p>
        </div>
      </div>
      <div class="overview-card card-green">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
        </div>
        <div class="card-content">
          <p class="card-label">及格率</p>
          <p class="card-value">{{ overview.总及格率 || 0 }}<span class="unit">%</span></p>
          <p class="card-desc">≥ 60分</p>
        </div>
      </div>
      <div class="overview-card card-purple">
        <div class="card-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        </div>
        <div class="card-content">
          <p class="card-label">优秀率</p>
          <p class="card-value">{{ overview.总优秀率 || 0 }}<span class="unit">%</span></p>
          <p class="card-desc">≥ 90分</p>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="card chart-card">
        <h2 class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="12" width="6" height="9" rx="1"/>
            <rect x="12" y="8" width="6" height="13" rx="1"/>
            <rect x="21" y="4" width="6" height="17" rx="1"/>
          </svg>
          各科目成绩对比
        </h2>
        <div ref="barChartRef" class="chart-container"></div>
      </div>

      <div class="card chart-card">
        <h2 class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
          整体分数段分布
        </h2>
        <div ref="pieChartRef" class="chart-container"></div>
      </div>

      <div class="card chart-card">
        <h2 class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
            <line x1="12" y1="22.08" x2="12" y2="12"/>
          </svg>
          学生成绩雷达图
        </h2>
        <div style="margin-bottom: 12px;">
          <select class="form-input" style="width: 200px;" v-model="selectedStudent" @change="updateRadarChart">
            <option v-for="s in ranking" :key="s.姓名" :value="s.姓名">{{ s.姓名 }}</option>
          </select>
        </div>
        <div ref="radarChartRef" class="chart-container"></div>
      </div>

      <div class="card chart-card">
        <h2 class="card-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 20V10"/>
            <path d="M12 20V4"/>
            <path d="M6 20v-6"/>
          </svg>
          成绩分布直方图
        </h2>
        <div ref="histogramRef" class="chart-container"></div>
      </div>
    </div>

    <div class="card">
      <h2 class="card-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 19l-7-7 7-7"/>
          <path d="M15 5l7 7-7 7"/>
        </svg>
        学生成绩排名
      </h2>
      <div class="table-toolbar">
        <input
          v-model="searchKeyword"
          type="text"
          class="form-input"
          placeholder="搜索学生姓名..."
          style="width: 240px;"
        >
        <select class="form-input" style="width: 160px;" v-model="sortSubject">
          <option value="总分">按总分排序</option>
          <option v-for="s in subjects" :key="s" :value="s">按{{ s }}排序</option>
        </select>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th>排名</th>
            <th>姓名</th>
            <th v-for="s in subjects" :key="s">{{ s }}</th>
            <th>总分</th>
            <th>平均分</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in filteredRanking" :key="item.姓名" :class="getRankClass(index + 1)">
            <td>
              <span class="badge" :class="getBadgeClass(index + 1)">
                {{ getRankBadge(index + 1) }}
              </span>
            </td>
            <td><strong>{{ item.姓名 }}</strong></td>
            <td v-for="s in subjects" :key="s">{{ item[s] }}</td>
            <td><strong>{{ item.总分 }}</strong></td>
            <td>{{ item.平均分 }}</td>
          </tr>
          <tr v-if="filteredRanking.length === 0">
            <td :colspan="subjects.length + 4" style="text-align: center; padding: 40px; color: #9ca3af;">
              暂无数据，请先导入成绩
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { getOverview, getSubjectStats, getRanking, getDistribution } from '../api'

const subjects = ['语文', '数学', '英语', '物理', '化学']
const colors = ['#667eea', '#764ba2', '#11998e', '#38ef7d', '#f093fb']

const overview = ref({})
const subjectStats = ref({})
const ranking = ref([])
const distribution = ref({})
const selectedStudent = ref('')
const searchKeyword = ref('')
const sortSubject = ref('总分')

const barChartRef = ref(null)
const pieChartRef = ref(null)
const radarChartRef = ref(null)
const histogramRef = ref(null)

let barChart = null
let pieChart = null
let radarChart = null
let histogramChart = null

const filteredRanking = ref([])

const loadData = async () => {
  try {
    const [ovRes, statsRes, rankRes, distRes] = await Promise.all([
      getOverview(),
      getSubjectStats(),
      getRanking(),
      getDistribution()
    ])
    overview.value = ovRes.data
    subjectStats.value = statsRes.data
    ranking.value = rankRes.data
    distribution.value = distRes.data

    if (ranking.value.length > 0) {
      selectedStudent.value = ranking.value[0].姓名
    }

    updateCharts()
  } catch (err) {
    console.error(err)
  }
}

const updateFilteredRanking = () => {
  let result = [...ranking.value]
  
  if (searchKeyword.value) {
    result = result.filter(r => r.姓名.includes(searchKeyword.value))
  }
  
  result.sort((a, b) => b[sortSubject.value] - a[sortSubject.value])
  
  filteredRanking.value = result
}

watch([searchKeyword, sortSubject, ranking], () => {
  updateFilteredRanking()
}, { deep: true })

const getRankClass = (rank) => {
  if (rank === 1) return 'rank-1'
  if (rank === 2) return 'rank-2'
  if (rank === 3) return 'rank-3'
  return ''
}

const getBadgeClass = (rank) => {
  if (rank === 1) return 'badge-gold'
  if (rank === 2) return 'badge-silver'
  if (rank === 3) return 'badge-bronze'
  return 'badge-default'
}

const getRankBadge = (rank) => {
  if (rank === 1) return '🥇'
  if (rank === 2) return '🥈'
  if (rank === 3) return '🥉'
  return rank
}

const updateCharts = () => {
  initBarChart()
  initPieChart()
  initRadarChart()
  initHistogram()
}

const initBarChart = () => {
  if (!barChartRef.value) return
  if (barChart) barChart.dispose()
  barChart = echarts.init(barChartRef.value)

  const avgData = subjects.map(s => subjectStats.value[s]?.平均分 || 0)
  
  barChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['平均分', '最高分', '最低分'], bottom: 0 },
    xAxis: { type: 'category', data: subjects, axisLabel: { color: '#6b7280' } },
    yAxis: { type: 'value', min: 0, max: 100, axisLabel: { color: '#6b7280' } },
    series: [
      {
        name: '平均分',
        type: 'bar',
        data: avgData,
        itemStyle: {
          borderRadius: [8, 8, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#667eea' },
            { offset: 1, color: '#764ba2' }
          ])
        },
        barWidth: 40
      },
      {
        name: '最高分',
        type: 'bar',
        data: subjects.map(s => subjectStats.value[s]?.最高分 || 0),
        itemStyle: {
          borderRadius: [8, 8, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#11998e' },
            { offset: 1, color: '#38ef7d' }
          ])
        },
        barWidth: 40
      },
      {
        name: '最低分',
        type: 'bar',
        data: subjects.map(s => subjectStats.value[s]?.最低分 || 0),
        itemStyle: {
          borderRadius: [8, 8, 0, 0],
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#f093fb' },
            { offset: 1, color: '#f5576c' }
          ])
        },
        barWidth: 40
      }
    ]
  })
}

const initPieChart = () => {
  if (!pieChartRef.value) return
  if (pieChart) pieChart.dispose()
  pieChart = echarts.init(pieChartRef.value)

  const dist = distribution.value['整体'] || {}
  const pieColors = ['#f87171', '#fb923c', '#fbbf24', '#34d399', '#60a5fa']

  pieChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 0 },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, formatter: '{b}\n{d}%', fontSize: 12, fontWeight: 600 },
      emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
      data: Object.keys(dist).map((key, i) => ({
        value: dist[key],
        name: key + '分',
        itemStyle: { color: pieColors[i] }
      }))
    }]
  })
}

const initRadarChart = () => {
  if (!radarChartRef.value) return
  if (radarChart) radarChart.dispose()
  radarChart = echarts.init(radarChartRef.value)
  updateRadarChart()
}

const updateRadarChart = () => {
  if (!radarChart || !selectedStudent.value) return
  const student = ranking.value.find(s => s.姓名 === selectedStudent.value)
  if (!student) return

  radarChart.setOption({
    tooltip: {},
    radar: {
      indicator: subjects.map(s => ({ name: s, max: 100 })),
      shape: 'polygon',
      splitNumber: 5,
      axisName: { color: '#4b5563', fontWeight: 600 },
      splitArea: { areaStyle: { color: ['rgba(102, 126, 234, 0.05)'] } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: subjects.map(s => student[s]),
        name: student.姓名,
        areaStyle: { color: 'rgba(102, 126, 234, 0.3)' },
        lineStyle: { color: '#667eea', width: 2 },
        itemStyle: { color: '#667eea' }
      }]
    }]
  })
}

const initHistogram = () => {
  if (!histogramRef.value) return
  if (histogramChart) histogramChart.dispose()
  histogramChart = echarts.init(histogramRef.value)

  const dist = distribution.value['整体'] || {}
  const histColors = ['#f87171', '#fb923c', '#fbbf24', '#34d399', '#60a5fa']

  histogramChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: Object.keys(dist), axisLabel: { color: '#6b7280' } },
    yAxis: { type: 'value', axisLabel: { color: '#6b7280' } },
    series: [{
      type: 'bar',
      data: Object.keys(dist).map((key, i) => ({
        value: dist[key],
        itemStyle: {
          borderRadius: [8, 8, 0, 0],
          color: histColors[i]
        }
      })),
      barWidth: '60%'
    }]
  })
}

onMounted(() => {
  loadData()
  updateFilteredRanking()
  window.addEventListener('resize', () => {
    barChart?.resize()
    pieChart?.resize()
    radarChart?.resize()
    histogramChart?.resize()
  })
})
</script>

<style scoped>
.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.page-desc {
  color: #6b7280;
  font-size: 14px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.overview-card {
  padding: 24px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 20px;
  color: #fff;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
}

.overview-card:hover {
  transform: translateY(-4px);
}

.card-blue {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-orange {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-green {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.card-purple {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
}

.card-icon {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon svg {
  width: 28px;
  height: 28px;
}

.card-label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 4px;
}

.card-value {
  font-size: 36px;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 4px;
}

.card-value .unit {
  font-size: 18px;
  margin-left: 4px;
  font-weight: 600;
}

.card-desc {
  font-size: 12px;
  opacity: 0.8;
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  min-height: 400px;
}

.chart-container {
  width: 100%;
  height: 320px;
}

.table-toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}
</style>
