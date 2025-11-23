class ApiService {
  constructor() {
    this.baseURL = import.meta.env.VITE_APP_API_BASE_URL
    this.useMock = import.meta.env.VITE_APP_MSW_ENABLED === 'true'
  }

  async request(url, options = {}) {
    const fullUrl = this.useMock ? url : `${this.baseURL}${url}`
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body)
    }

    try {
      const response = await fetch(fullUrl, config)
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || '请求失败')
      }
      
      return data
    } catch (error) {
      console.error('API请求错误:', error)
      throw error
      // return error message
      const errorMessage = {
        success: false,
        message: error.message || '请求失败',
      }
      return JSON.stringify(errorMessage)
    }
  }

  async post(url, data) {
    return this.request(url, {
      method: 'POST',
      body: data,
    })
  }

  async get(url) {
    return this.request(url, {
      method: 'GET',
    })
  }
}

export const apiService = new ApiService()