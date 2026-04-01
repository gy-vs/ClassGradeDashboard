<template>
  <div class="data-import-card">
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="upload-area"
             :class="{ 'is-dragover': isDragover }"
             @dragover.prevent="handleDragOver"
             @dragleave.prevent="handleDragLeave"
             @drop.prevent="handleDrop"
             @click="triggerFileInput">
          <input ref="fileInput" type="file" accept=".xlsx,.xls" @change="handleFileChange" style="display: none;">
          <el-icon :size="48" color="#409EFF"><Upload /></el-icon>
          <div class="upload-text">点击或拖拽 Excel 文件到此处上传</div>
          <div class="upload-hint">支持 .xlsx, .xls 格式</div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="manual-input">
          <el-form :model="form" label-width="60px" size="small">
            <el-form-item label="姓名">
              <el-input v-model="form.name" placeholder="请输入学生姓名" />
            </el-form-item>
            <el-row :gutter="10">
              <el-col :span="12">
                <el-form-item label="语文">
                  <el-input-number v-model="form.chinese" :min="0" :max="100" :step="1" style="width: 100%;" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="数学">
                  <el-input-number v-model="form.math" :min="0" :max="100" :step="1" style="width: 100%;" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="10">
              <el-col :span="12">
                <el-form-item label="英语">
                  <el-input-number v-model="form.english" :min="0" :max="100" :step="1" style="width: 100%;" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="物理">
                  <el-input-number v-model="form.physics" :min="0" :max="100" :step="1" style="width: 100%;" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="化学">
              <el-input-number v-model="form.chemistry" :min="0" :max="100" :step="1" style="width: 100%;" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleAddStudent" style="width: 100%;">
                <el-icon><Plus /></el-icon> 添加学生
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-col>
    </el-row>
    <div class="action-buttons">
      <el-button @click="downloadTemplate">
        <el-icon><Download /></el-icon> 下载模板
      </el-button>
      <el-button type="danger" @click="handleClearData">
        <el-icon><Delete /></el-icon> 清空数据
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const emit = defineEmits(['data-imported'])

const fileInput = ref(null)
const isDragover = ref(false)

const form = ref({
  name: '',
  chinese: 0,
  math: 0,
  english: 0,
  physics: 0,
  chemistry: 0
})

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleDragOver = () => {
  isDragover.value = true
}

const handleDragLeave = () => {
  isDragover.value = false
}

const handleDrop = (e) => {
  isDragover.value = false
  const files = e.dataTransfer.files
  if (files.length > 0) {
    uploadFile(files[0])
  }
}

const handleFileChange = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    uploadFile(files[0])
  }
  e.target.value = ''
}

const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await axios.post('/api/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    ElMessage.success(res.data.message)
    emit('data-imported')
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '导入失败')
  }
}

const handleAddStudent = async () => {
  if (!form.value.name) {
    ElMessage.warning('请输入学生姓名')
    return
  }

  try {
    const data = {
      '姓名': form.value.name,
      '语文': form.value.chinese,
      '数学': form.value.math,
      '英语': form.value.english,
      '物理': form.value.physics,
      '化学': form.value.chemistry
    }
    await axios.post('/api/students', data)
    ElMessage.success('添加成功')
    form.value = { name: '', chinese: 0, math: 0, english: 0, physics: 0, chemistry: 0 }
    emit('data-imported')
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '添加失败')
  }
}

const downloadTemplate = () => {
  window.location.href = '/api/template'
}

const handleClearData = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有数据吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await axios.post('/api/clear')
    ElMessage.success('数据已清空')
    emit('data-imported')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('清空失败')
    }
  }
}
</script>

<style scoped>
.data-import-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 12px;
  padding: 60px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.upload-area:hover,
.upload-area.is-dragover {
  border-color: #409EFF;
  background-color: #f0f7ff;
}

.upload-text {
  margin-top: 16px;
  font-size: 16px;
  color: #606266;
}

.upload-hint {
  margin-top: 8px;
  font-size: 14px;
  color: #909399;
}

.manual-input {
  padding: 10px 0;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
</style>
