import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'

// Create axios instance with default configuration
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API methods
export const apiClient = {
  get: <T>(url: string): Promise<AxiosResponse<T>> => api.get(url),
  post: <T>(url: string, data?: any): Promise<AxiosResponse<T>> => api.post(url, data),
  put: <T>(url: string, data?: any): Promise<AxiosResponse<T>> => api.put(url, data),
  delete: <T>(url: string): Promise<AxiosResponse<T>> => api.delete(url),
}

export default api