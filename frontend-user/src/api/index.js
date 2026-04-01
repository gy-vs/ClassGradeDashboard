import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const getGrades = () => request.get('/grades')
export const addGrade = (data) => request.post('/grades', data)
export const getStatistics = () => request.get('/statistics')
export const getRankings = () => request.get('/rankings')
export const getDistribution = () => request.get('/distribution')
export const importExcel = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
export const downloadTemplate = () => {
  window.open('/api/template')
}

export default request
