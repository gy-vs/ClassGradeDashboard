import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5001/api',
  timeout: 10000
})

export const getGrades = () => api.get('/grades')
export const addGrade = (data) => api.post('/grades', data)
export const deleteGrade = (name) => api.delete(`/grades/${name}`)
export const importExcel = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}
export const downloadTemplate = () => api.get('/template', { responseType: 'blob' })
export const getSubjectStats = () => api.get('/statistics/subjects')
export const getOverview = () => api.get('/statistics/overview')
export const getRanking = () => api.get('/statistics/ranking')
export const getDistribution = () => api.get('/statistics/distribution')
export const clearData = () => api.post('/clear')

export default api
