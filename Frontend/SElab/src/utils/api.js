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
      
      if (!response.ok) {
        // 尝试解析错误信息，如果失败则使用默认错误
        let errorData
        try {
          errorData = await response.json()
        } catch {
          errorData = { message: `HTTP错误: ${response.status}` }
        }
        throw new Error(errorData.message || '请求失败')
      }
      
      const data = await response.json()
      return data
    } catch (error) {
      console.error('API请求错误:', error)
      throw error
      // return error message
      const errorMessage = {
        success: false,
        message: error.message || '请求失败',
        error: error,
      }
      throw errorMessage
      // return JSON.stringify(errorMessage)
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