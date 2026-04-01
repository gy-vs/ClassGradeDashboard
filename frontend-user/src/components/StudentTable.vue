<template>
  <div class="student-table-card">
    <div class="table-header">
      <el-input
        v-model="searchText"
        placeholder="搜索学生姓名"
        prefix-icon="Search"
        style="width: 300px;"
        clearable
      />
    </div>
    <el-table
      :data="filteredStudents"
      stripe
      style="width: 100%;"
      :row-class-name="tableRowClassName"
      :default-sort="{ prop: '总分', order: 'descending' }"
    >
      <el-table-column prop="排名" label="排名" width="80" sortable>
        <template #default="{ row }">
          <div class="rank-cell">
            <span v-if="row.排名 === 1" class="medal gold">🥇</span>
            <span v-else-if="row.排名 === 2" class="medal silver">🥈</span>
            <span v-else-if="row.排名 === 3" class="medal bronze">🥉</span>
            <span v-else class="rank-number">{{ row.排名 }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="姓名" label="姓名" width="120" sortable />
      <el-table-column prop="语文" label="语文" width="90" sortable>
        <template #default="{ row }">
          <el-tag :type="getScoreType(row.语文)" size="small">{{ row.语文 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="数学" label="数学" width="90" sortable>
        <template #default="{ row }">
          <el-tag :type="getScoreType(row.数学)" size="small">{{ row.数学 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="英语" label="英语" width="90" sortable>
        <template #default="{ row }">
          <el-tag :type="getScoreType(row.英语)" size="small">{{ row.英语 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="物理" label="物理" width="90" sortable>
        <template #default="{ row }">
          <el-tag :type="getScoreType(row.物理)" size="small">{{ row.物理 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="化学" label="化学" width="90" sortable>
        <template #default="{ row }">
          <el-tag :type="getScoreType(row.化学)" size="small">{{ row.化学 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="总分" label="总分" width="100" sortable>
        <template #default="{ row }">
          <span class="total-score">{{ row.总分 }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ $index }">
          <el-button type="danger" size="small" link @click="handleDelete($index)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const props = defineProps(['students'])
const emit = defineEmits(['refresh'])

const searchText = ref('')

const filteredStudents = computed(() => {
  if (!searchText.value) return props.students
  return props.students.filter(student => 
    student.姓名.includes(searchText.value)
  )
})

const getScoreType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return ''
  if (score >= 60) return 'warning'
  return 'danger'
}

const tableRowClassName = ({ rowIndex }) => {
  if (rowIndex === 0) return 'gold-row'
  if (rowIndex === 1) return 'silver-row'
  if (rowIndex === 2) return 'bronze-row'
  return ''
}

const handleDelete = async (index) => {
  try {
    await ElMessageBox.confirm('确定要删除这名学生的成绩吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await axios.delete(`/api/students/${index}`)
    ElMessage.success('删除成功')
    emit('refresh')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
</script>

<style scoped>
.student-table-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.table-header {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rank-cell {
  display: flex;
  align-items: center;
  justify-content: center;
}

.medal {
  font-size: 24px;
}

.rank-number {
  font-weight: 500;
  color: #606266;
}

.total-score {
  font-weight: 700;
  color: #409EFF;
  font-size: 16px;
}

:deep(.gold-row) {
  background-color: #fff7e6 !important;
}

:deep(.silver-row) {
  background-color: #f5f7fa !important;
}

:deep(.bronze-row) {
  background-color: #fef3e2 !important;
}

:deep(.gold-row:hover),
:deep(.silver-row:hover),
:deep(.bronze-row:hover) {
  background-color: #ecf5ff !important;
}
</style>
