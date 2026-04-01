<template>
  <div class="overview-cards">
    <el-row :gutter="20">
      <el-col :xs="24" :sm="12" :md="6">
        <div class="card blue-card">
          <div class="card-icon">
            <el-icon :size="40"><User /></el-icon>
          </div>
          <div class="card-content">
            <div class="card-value">{{ overview.total_students || 0 }}</div>
            <div class="card-label">总人数</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="card purple-card">
          <div class="card-icon">
            <el-icon :size="40"><Trophy /></el-icon>
          </div>
          <div class="card-content">
            <div class="card-value">{{ overview.overall_average || 0 }}</div>
            <div class="card-label">平均分</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="card green-card">
          <div class="card-icon">
            <el-icon :size="40"><CircleCheck /></el-icon>
          </div>
          <div class="card-content">
            <div class="card-value">{{ overview.overall_pass_rate || 0 }}%</div>
            <div class="card-label">及格率</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <div class="card orange-card">
          <div class="card-icon">
            <el-icon :size="40"><Star /></el-icon>
          </div>
          <div class="card-content">
            <div class="card-value">{{ overview.overall_excellent_rate || 0 }}%</div>
            <div class="card-label">优秀率</div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
defineProps(['overview'])
</script>

<style scoped>
.overview-cards {
  width: 100%;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card-icon {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.blue-card .card-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.purple-card .card-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.green-card .card-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.orange-card .card-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.card-content {
  flex: 1;
}

.card-value {
  font-size: 36px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
}

.card-label {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}
</style>
