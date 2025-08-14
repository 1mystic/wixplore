import axios from 'axios'

// Determine the base URL based on environment
const getBaseURL = () => {
  // For local development
  if (import.meta.env.DEV) {
    return 'http://localhost:5000/api'
  }
  
  // For production (Vercel deployment)
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // Default to relative path for serverless deployment
  return '/api'
}

export default axios.create({
  baseURL: getBaseURL(),
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})
