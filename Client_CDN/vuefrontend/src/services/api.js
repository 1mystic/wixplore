import axios from 'axios'
export default axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://your-backend-url/api',
  withCredentials: true,
})
