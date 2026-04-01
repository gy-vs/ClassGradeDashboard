<template>
  <div class="data-page">
    <h1 class="page-title">数据管理</h1>
    
    <div class="grid">
      <div class="card">
        <h2 class="card-title">手动录入成绩</h2>
        <form @submit.prevent="handleAdd" class="form">
          <div class="form-row">
            <div class="form-group">
              <label>学生姓名</label>
              <input v-model="form.name" type="text" placeholder="请输入学生姓名" />
            </div>
            <div class="form-group">
              <label>科目</label>
              <select v-model="form.subject">
                <option value="">请选择科目</option>
                <option v-for="s in subjects" :key="s" :value="s">{{ s }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>分数</label>
              <input v-model="form.score" type="number" min="0" max="100" placeholder="0-100" />
            </div>
            <button type="submit" class="btn btn-primary">添加</button>
          </div>
        </form>
      </div>

      <div class="card">
        <h2 class="card-title">Excel 批量导入</h2>
        <div
          class="upload-area"
          :class="{ 'dragover': isDragover }"
          @dragover.prevent="isDragover = true"
          @dragleave.prevent="isDragover = false"
          @drop.prevent="handleDrop"
          @click="$refs.fileInput.click()"
        >
          <input ref="fileInput" type="file" accept=".xlsx,.xls" @change="handleFile" style="display: none" />
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
          </svg>
          <p class="upload-text">拖拽文件到此处，或点击上传</p>
          <p class="upload-hint">支持 .xlsx, .xls 格式</p>
        </div>
        <button @click="downloadTemplate" class="btn btn-outline">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          下载导入模板
        </button>
      </div>
    </div>

    <div class="card">
      <h2 class="card-title">成绩列表</h2>
      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>姓名</th>
              <th v-for="s in subjects" :key="s">{{ s }}</th>
              <th>总分</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, idx) in grades" :key="idx" :class="{ even: idx % 2 === 1 }">
              <td>{{ row.姓名 }}</td>
              <td v-for="s in subjects" :key="s">{{ row[s] || '-' }}</td>
              <td class="total">{{ getTotal(row) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getGrades, addGrade, importExcel, downloadTemplate } from '@/api'

const subjects = ['语文', '数学', '英语', '物理', '化学']
const grades = ref([])
const isDragover = ref(false)
const form = ref({
  name: '',
  subject: '',
  score: ''
})

const loadGrades = async () => {
  const res = await getGrades()
  grades.value = res.data.data
}

const handleAdd = async () => {
  if (!form.value.name || !form.value.subject || form.value.score === '') {
    alert('请填写完整信息')
    return
  }
  try {
    await addGrade(form.value)
    form.value = { name: '', subject: '', score: '' }
    await loadGrades()
    alert('添加成功！')
  } catch (e) {
    alert('添加失败：' + (e.response?.data?.error || e.message))
  }
}

const handleDrop = (e) => {
  isDragover.value = false
  const file = e.dataTransfer.files[0]
  handleImport(file)
}

const handleFile = (e) => {
  const file = e.target.files[0]
  handleImport(file)
}

const handleImport = async (file) => {
  if (!file) return
  try {
    await importExcel(file)
    await loadGrades()
    alert('导入成功！')
  } catch (e) {
    alert('导入失败：' + (e.response?.data?.error || e.message))
  }
}

const getTotal = (row) => {
  return subjects.reduce((sum, s) => sum + (row[s] || 0), 0)
}

onMounted(() => {
  loadGrades()
})
</script>

<style scoped>
.page-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 24px;
  color: #1a202c;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #2d3748;
}

.form-row {
  display: flex;
  gap: 16px;
  align-items: end;
}

.form-group {
  flex: 1;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #4a5568;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.btn {
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-outline {
  background: white;
  color: #667eea;
  border: 1px solid #667eea;
  margin-top: 16px;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

.upload-area {
  border: 2px dashed #cbd5e0;
  border-radius: 12px;
  padding: 40px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.upload-area.dragover,
.upload-area:hover {
  border-color: #667eea;
  background: #f8f7ff;
}

.upload-text {
  margin-top: 12px;
  font-weight: 500;
  color: #4a5568;
}

.upload-hint {
  margin-top: 4px;
  font-size: 13px;
  color: #9ca3af;
}

.table-wrapper {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  text-align: left;
  padding: 12px 16px;
  background: #f7fafc;
  font-weight: 600;
  color: #2d3748;
  border-bottom: 2px solid #e2e8f0;
}

.table td {
  padding: 12px 16px;
  border-bottom: 1px solid #e2e8f0;
}

.table tr.even {
  background: #f7fafc;
}

.total {
  font-weight: 600;
  color: #667eea;
}
</style>
