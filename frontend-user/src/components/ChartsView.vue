<template>
  <div class="charts-view">
    <el-row :gutter="20">
      <el-col :span="16">
        <div class="chart-card">
          <div class="chart-title">各科目平均分对比</div>
          <div ref="barChartRef" class="chart-container"></div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="chart-card">
          <div class="chart-title">分数段分布</div>
          <div ref="pieChartRef" class="chart-container"></div>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <div class="chart-card">
          <div class="chart-title">科目统计详情</div>
          <el-table :data="subjectStatsData" stripe style="width: 100%;">
            <el-table-column prop="subject" label="科目" width="100" />
            <el-table-column prop="average" label="平均分" width="100" />
            <el-table-column prop="max" label="最高分" width="100" />
            <el-table-column prop="min" label="最低分" width="100" />
            <el-table-column prop="pass_rate" label="及格率">
              <template #default="{ row }">
                <el-tag type="success" v-if="row.pass_rate >= 80">{{ row.pass_rate }}%</el-tag>
                <el-tag type="warning" v-else-if="row.pass_rate >= 60">{{ row.pass_rate }}%</el-tag>
                <el-tag type="danger" v-else>{{ row.pass_rate }}%</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="excellent_rate" label="优秀率">
              <template #default="{ row }">
                <el-tag type="success" v-if="row.excellent_rate >= 30">{{ row.excellent_rate }}%</el-tag>
                <el-tag type="info" v-else>{{ row.excellent_rate }}%</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps(['statistics', 'students'])

const barChartRef = ref(null)
const pieChartRef = ref(null)
let barChart = null
let pieChart = null

const subjectStatsData = ref([])

const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de']
const subjects = ['语文', '数学', '英语', '物理', '化学']

const initBarChart = () => {
  if (!barChartRef.value) return
  
  barChart = echarts.init(barChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['平均分'],
      top: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: subjects,
      axisLabel: {
        fontSize: 14
      }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 100
    },
    series: [{
      name: '平均分',
      type: 'bar',
      barWidth: '50%',
      data: [],
      itemStyle: {
        borderRadius: [8, 8, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#667eea' },
          { offset: 1, color: '#764ba2' }
        ])
      }
    }]
  }
  
  barChart.setOption(option)
  
  window.addEventListener('resize', () => barChart.resize())
}

const initPieChart = () => {
  if (!pieChartRef.value) return
  
  pieChart = echarts.init(pieChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '10%',
      top: 'center'
    },
    series: [{
      name: '分数段',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['35%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}\n{d}%'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: []
    }]
  }
  
  pieChart.setOption(option)
  
  window.addEventListener('resize', () => pieChart.resize())
}

const updateCharts = () => {
  if (!props.statistics) return
  
  if (barChart && props.statistics.subject_stats) {
    const averages = subjects.map(subject => 
      props.statistics.subject_stats[subject]?.average || 0
    )
    
    barChart.setOption({
      series: [{
        data: averages
      }]
    })
  }
  
  if (pieChart && props.statistics.distribution) {
    const dist = props.statistics.distribution
    const pieData = [
      { value: dist['0-59'] || 0, name: '0-59', itemStyle: { color: '#ee6666' } },
      { value: dist['60-69'] || 0, name: '60-69', itemStyle: { color: '#fac858' } },
      { value: dist['70-79'] || 0, name: '70-79', itemStyle: { color: '#91cc75' } },
      { value: dist['80-89'] || 0, name: '80-89', itemStyle: { color: '#73c0de' } },
      { value: dist['90-100'] || 0, name: '90-100', itemStyle: { color: '#5470c6' } }
    ].filter(item => item.value > 0)
    
    pieChart.setOption({
      series: [{
        data: pieData
      }]
    })
  }
  
  if (props.statistics.subject_stats) {
    subjectStatsData.value = subjects.map(subject => ({
      subject,
      ...props.statistics.subject_stats[subject]
    }))
  }
}

onMounted(() => {
  nextTick(() => {
    initBarChart()
    initPieChart()
    updateCharts()
  })
})

watch(() => props.statistics, () => {
  updateCharts()
}, { deep: true })
</script>

<style scoped>
.charts-view {
  width: 100%;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.chart-container {
  height: 350px;
  width: 100%;
}
</style>
