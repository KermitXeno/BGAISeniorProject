import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'

// Medical AI API Base URL - Update this to match your Flask server
const AI_API_BASE_URL = 'http://localhost:5000'

// Create axios instance for AI API
const aiApi: AxiosInstance = axios.create({
  baseURL: AI_API_BASE_URL,
  timeout: 30000, // Longer timeout for AI processing
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for AI API
aiApi.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError) => {
    console.error('AI API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// Type definitions for AI API responses
export interface MRIAnalysisResult {
  prediction: string
  confidence: number
  all_scores: Record<string, number>
  status: string
}

export interface BiomarkerAnalysisResult {
  prediction: string
  confidence: number
  all_scores: Record<string, number>
  input_data: number[]
  status: string
}

export interface BiomarkerData {
  gender: number      // 0 for male, 1 for female
  age: number         // Age in years
  education: number   // Years of education
  ses: number         // Socioeconomic status
  mmse: number        // Mini-Mental State Examination score
  cdr: number         // Clinical Dementia Rating
  etiv: number        // Estimated Total Intracranial Volume
  nwbv: number        // Normalized Whole Brain Volume
}

// Medical AI API Functions
export const medicalAPI = {
  // Analyze MRI scan
  analyzeMRI: async (file: File): Promise<MRIAnalysisResult> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await aiApi.post<MRIAnalysisResult>('/predictMRI', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    return response.data
  },

  // Analyze biomarker data
  analyzeBiomarkers: async (data: BiomarkerData): Promise<BiomarkerAnalysisResult> => {
    const biomarkerArray = [
      data.gender,
      data.age,
      data.education,
      data.ses,
      data.mmse,
      data.cdr,
      data.etiv,
      data.nwbv
    ]
    
    const response = await aiApi.post<BiomarkerAnalysisResult>('/predictBIO', {
      data: biomarkerArray
    })
    
    return response.data
  },

  // Health check for AI API
  healthCheck: async (): Promise<{ status: string; models_loaded: boolean }> => {
    const response = await aiApi.get('/health')
    return response.data
  }
}

// Helper functions
export const formatConfidence = (confidence: number): string => {
  return `${(confidence * 100).toFixed(1)}%`
}

export const getConfidenceColor = (confidence: number): string => {
  if (confidence >= 0.8) return 'text-green-600'
  if (confidence >= 0.6) return 'text-yellow-600'
  return 'text-red-600'
}

export const getSeverityLevel = (prediction: string): 'low' | 'medium' | 'high' => {
  switch (prediction.toLowerCase()) {
    case 'no impairment':
      return 'low'
    case 'very mild impairment':
      return 'low'
    case 'mild impairment':
      return 'medium'
    case 'moderate impairment':
    case 'severe impairment':
      return 'high'
    default:
      return 'medium'
  }
}

// Create axios instance with default configuration (for other API calls)
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

// General API methods
export const apiClient = {
  get: <T>(url: string): Promise<AxiosResponse<T>> => api.get(url),
  post: <T>(url: string, data?: any): Promise<AxiosResponse<T>> => api.post(url, data),
  put: <T>(url: string, data?: any): Promise<AxiosResponse<T>> => api.put(url, data),
  delete: <T>(url: string): Promise<AxiosResponse<T>> => api.delete(url),
}

export default api