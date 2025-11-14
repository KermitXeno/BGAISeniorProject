import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'

// Medical AI API Base URL - Update this to match your Flask server
const AI_API_BASE_URL = 'http://localhost:5001'

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
  predicted_class: string
  max_confidence: string
  interpretation: Record<string, string>
  impairment_labels: string[]
  raw_predictions: number[]
  status: string
  // Add compatibility fields for existing frontend code
  prediction: string
  confidence: number
  all_scores: Record<string, number>
}

export interface BiomarkerAnalysisResult {
  // Updated to match your Flask API response
  predicted_class: string
  max_confidence: string
  interpretation: Record<string, string>
  cdr_labels: string[]
  raw_predictions: number[]
  input_data: number[]
  status: string
  // Add compatibility fields for existing frontend code
  prediction: string
  confidence: number
  all_scores: Record<string, number>
}

export interface BiomarkerData {
  gender: number      // 0 for male, 1 for female (M/F)
  age: number         // Age in years
  education: number   // Years of education (EDUC)
  ses: number         // Socioeconomic status (SES)
  mmse: number        // Mini-Mental State Examination score (MMSE)
  etiv: number        // Estimated Total Intracranial Volume (eTIV)
  nwbv: number        // Normalized Whole Brain Volume (nWBV)
  asf: number         // Atlas Scaling Factor (ASF)
}

// Medical AI API Functions
export const medicalAPI = {
  // Analyze MRI scan
  analyzeMRI: async (file: File): Promise<MRIAnalysisResult> => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await aiApi.post<any>('/amri', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    // Transform the response to match our interface
    const apiResponse = response.data;
    
    // Convert max_confidence string to number (remove % and divide by 100)
    const confidenceValue = parseFloat(apiResponse.max_confidence.replace('%', '')) / 100;
    
    // Create all_scores from interpretation (convert percentages to decimals)
    const all_scores: Record<string, number> = {};
    Object.entries(apiResponse.interpretation).forEach(([key, value]) => {
      all_scores[key] = parseFloat((value as string).replace('%', '')) / 100;
    });

    const transformedResponse: MRIAnalysisResult = {
      // Original Flask API fields
      predicted_class: apiResponse.predicted_class,
      max_confidence: apiResponse.max_confidence,
      interpretation: apiResponse.interpretation,
      impairment_labels: apiResponse.impairment_labels,
      raw_predictions: apiResponse.raw_predictions,
      status: apiResponse.status,
      // Compatibility fields for existing frontend code
      prediction: apiResponse.predicted_class,
      confidence: confidenceValue,
      all_scores: all_scores
    };
    
    return transformedResponse;
  },

  // Analyze biomarker data
  analyzeBiomarkers: async (data: BiomarkerData): Promise<BiomarkerAnalysisResult> => {
    // Format data according to your model's expected input order:
    // [M/F, Age, EDUC, SES, MMSE, eTIV, nWBV, ASF]
    const biomarkerArray = [
      data.gender,    // M/F (0 or 1)
      data.age,       // Age
      data.education, // EDUC
      data.ses,       // SES
      data.mmse,      // MMSE
      data.etiv,      // eTIV
      data.nwbv,      // nWBV
      data.asf        // ASF
    ]
    
    const response = await aiApi.post<any>('/biofm', {
      features: biomarkerArray
    })

    // Transform the response to match our interface
    const apiResponse = response.data;
    
    // Convert max_confidence string to number (remove % and divide by 100)
    const confidenceValue = parseFloat(apiResponse.max_confidence.replace('%', '')) / 100;
    
    // Create all_scores from interpretation (convert percentages to decimals)
    const all_scores: Record<string, number> = {};
    Object.entries(apiResponse.interpretation).forEach(([key, value]) => {
      all_scores[key] = parseFloat((value as string).replace('%', '')) / 100;
    });

    const transformedResponse: BiomarkerAnalysisResult = {
      // Original Flask API fields
      predicted_class: apiResponse.predicted_class,
      max_confidence: apiResponse.max_confidence,
      interpretation: apiResponse.interpretation,
      cdr_labels: apiResponse.cdr_labels,
      raw_predictions: apiResponse.raw_predictions,
      input_data: apiResponse.input_data,
      status: apiResponse.status,
      // Compatibility fields for existing frontend code
      prediction: apiResponse.predicted_class,
      confidence: confidenceValue,
      all_scores: all_scores
    };
    
    return transformedResponse;
  },

  // Health check for AI API
  healthCheck: async (): Promise<{ status: string; models_loaded: boolean }> => {
    const response = await aiApi.get('/health')
    return response.data
  }
}

// Helper functions
export const formatConfidence = (confidence: number | string): string => {
  if (typeof confidence === 'string') {
    return confidence; // Already formatted (e.g., "85.2%")
  }
  return `${(confidence * 100).toFixed(1)}%`
}

export const getConfidenceColor = (confidence: number | string): string => {
  let confidenceValue: number;
  
  if (typeof confidence === 'string') {
    confidenceValue = parseFloat(confidence.replace('%', '')) / 100;
  } else {
    confidenceValue = confidence;
  }
  
  if (confidenceValue >= 0.8) return 'text-green-600'
  if (confidenceValue >= 0.6) return 'text-yellow-600'
  return 'text-red-600'
}

export const getSeverityLevel = (prediction: string): 'low' | 'medium' | 'high' => {
  const lower = prediction.toLowerCase();
  
  // For BIO model (CDR levels)
  if (lower.includes('cdr 0') || lower.includes('no dementia')) {
    return 'low';
  }
  if (lower.includes('cdr 0.5') || lower.includes('very mild dementia')) {
    return 'low';
  }
  if (lower.includes('cdr 1') || lower.includes('mild dementia')) {
    return 'medium';
  }
  if (lower.includes('cdr 2') || lower.includes('moderate dementia')) {
    return 'high';
  }
  
  // For MRI model (Impairment levels)
  if (lower.includes('no impairment')) {
    return 'low';
  }
  if (lower.includes('very mild impairment')) {
    return 'low';
  }
  if (lower.includes('mild impairment')) {
    return 'medium';
  }
  if (lower.includes('moderate impairment') || lower.includes('severe impairment')) {
    return 'high';
  }
  
  return 'medium'; // Default fallback
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