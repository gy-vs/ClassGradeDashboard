<template>
  <div class="container">
    <div class="page-header">
      <h1>数据管理</h1>
      <p class="page-desc">管理学生成绩数据，支持手动录入和 Excel 批量导入</p>
    </div>

    <div class="grid-row">
      <div class="col-left">
        <div class="card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            手动录入成绩
          </h2>
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label class="form-label">学生姓名</label>
              <input v-model="formData.姓名" type="text" class="form-input" placeholder="请输入学生姓名" required>
            </div>
            <div class="form-row">
              <div class="form-group" v-for="subject in subjects" :key="subject">
                <label class="form-label">{{ subject }}</label>
                <input v-model.number="formData[subject]" type="number" min="0" max="100" class="form-input" placeholder="0-100" required>
              </div>
            </div>
            <button type="submit" class="btn btn-primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              保存成绩
            </button>
          </form>
        </div>

        <div class="card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            Excel 批量导入
          </h2>
          <div
            class="upload-area"
            :class="{ 'upload-active': isDragOver }"
            @dragover.prevent="isDragOver = true"
            @dragleave="isDragOver = false"
            @drop.prevent="handleDrop"
          >
            <input
              ref="fileInput"
              type="file"
              accept=".xlsx,.xls"
              @change="handleFileChange"
              style="display: none"
            >
            <div class="upload-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10 9 9 9 8 9"/>
              </svg>
            </div>
            <p class="upload-text">拖拽 Excel 文件到此处</p>
            <p class="upload-hint">或 <span class="upload-link" @click="$refs.fileInput.click()">点击选择文件</span></p>
            <p class="upload-format">支持格式：.xlsx, .xls</p>
          </div>
          <div v-if="uploadedFile" class="file-info">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            <span>{{ uploadedFile.name }}</span>
            <button class="btn btn-success" @click="handleImport" :disabled="importing">
              {{ importing ? '导入中...' : '开始导入' }}
            </button>
          </div>
          <div class="action-buttons">
            <button class="btn btn-warning" @click="handleDownloadTemplate">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              下载模板
            </button>
            <button class="btn btn-danger" @click="handleClear">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              </svg>
              清空数据
            </button>
          </div>
        </div>
      </div>

      <div class="col-right">
        <div class="card">
          <h2 class="card-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="8" y1="6" x2="21" y2="6"/>
              <line x1="8" y1="12" x2="21" y2="12"/>
              <line x1="8" y1="18" x2="21" y2="18"/>
              <line x1="3" y1="6" x2="3.01" y2="6"/>
              <line x1="3" y1="12" x2="3.01" y2="12"/>
              <line x1="3" y1="18" x2="3.01" y2="18"/>
            </svg>
            数据列表
          </h2>
          <div class="table-wrapper">
            <table class="table">
              <thead>
                <tr>
                  <th>姓名</th>
                  <th v-for="subject in subjects" :key="subject">{{ subject }}</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in gradeList" :key="item.姓名">
                  <td><strong>{{ item.姓名 }}</strong></td>
                  <td v-for="subject in subjects" :key="subject">{{ item[subject] }}</td>
                  <td>
                    <button class="btn btn-danger" style="padding: 6px 12px; font-size: 12px;" @click="handleDelete(item.姓名)">
                      删除
                    </button>
                  </td>
                </tr>
                <tr v-if="gradeList.length === 0">
                  <td :colspan="subjects.length + 2" style="text-align: center; padding: 40px; color: #9ca3af;">
                    暂无数据
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getGrades, addGrade, deleteGrade, importExcel, downloadTemplate, clearData } from '../api'

const subjects = ['语文', '数学', '英语', '物理', '化学']

const formData = ref({
  姓名: '',
  语文: 0,
  数学: 0,
  英语: 0,
  物理: 0,
  化学: 0
})

const gradeList = ref([])
const isDragOver = ref(false)
const uploadedFile = ref(null)
const importing = ref(false)

const loadData = async () => {
  try {
    const res = await getGrades()
    gradeList.value = res.data
  } catch (err) {
    console.error(err)
  }
}

const handleSubmit = async () => {
  try {
    await addGrade(formData.value)
    alert('保存成功！')
    formData.value = { 姓名: '', 语文: 0, 数学: 0, 英语: 0, 物理: 0, 化学: 0 }
    loadData()
  } catch (err) {
    alert('保存失败：' + err.message)
  }
}

const handleDrop = (e) => {
  isDragOver.value = false
  const files = e.dataTransfer.files
  if (files.length > 0 && (files[0].name.endsWith('.xlsx') || files[0].name.endsWith('.xls'))) {
    uploadedFile.value = files[0]
  } else {
    alert('请上传 Excel 文件！')
  }
}

const handleFileChange = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    uploadedFile.value = files[0]
  }
}

const handleImport = async () => {
  if (!uploadedFile.value) return
  importing.value = true
  try {
    const res = await importExcel(uploadedFile.value)
    alert(res.data.message)
    uploadedFile.value = null
    loadData()
  } catch (err) {
    alert('导入失败：' + (err.response?.data?.error || err.message))
  } finally {
    importing.value = false
  }
}

const handleDownloadTemplate = async () => {
  try {
    const res = await downloadTemplate()
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.download = '成绩导入模板.xlsx'
    link.click()
    window.URL.revokeObjectURL(url)
  } catch (err) {
    alert('下载失败：' + err.message)
  }
}

const handleDelete = async (name) => {
  if (confirm(`确定要删除 ${name} 的成绩吗？`)) {
    try {
      await deleteGrade(name)
      alert('删除成功！')
      loadData()
    } catch (err) {
      alert('删除失败：' + err.message)
    }
  }
}

const handleClear = async () => {
  if (confirm('确定要清空所有数据吗？此操作不可恢复！')) {
    try {
      await clearData()
      alert('数据已清空！')
      loadData()
    } catch (err) {
      alert('清空失败：' + err.message)
    }
  }
}

onMounted(() => {
  loadData()
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

.grid-row {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 20px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
}

.upload-area:hover,
.upload-active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.upload-icon {
  color: #9ca3af;
  margin-bottom: 16px;
}

.upload-icon svg {
  width: 48px;
  height: 48px;
  margin: 0 auto;
}

.upload-text {
  font-size: 16px;
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 8px;
}

.upload-hint {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 8px;
}

.upload-link {
  color: #667eea;
  font-weight: 500;
  text-decoration: underline;
  cursor: pointer;
}

.upload-format {
  color: #9ca3af;
  font-size: 12px;
}

.file-info {
  margin-top: 16px;
  padding: 12px 16px;
  background: #f0fdf4;
  border: 1px solid #86efac;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.file-info svg {
  width: 24px;
  height: 24px;
  color: #16a34a;
}

.action-buttons {
  margin-top: 16px;
  display: flex;
  gap: 12px;
  justify-content: flex-start;
}

.table-wrapper {
  overflow-x: auto;
}
</style>
