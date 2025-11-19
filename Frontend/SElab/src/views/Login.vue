<template>
  <div class="login-container">
    <!-- 登录卡片 -->
    <div class="login-card">
      <div class="login-header">
        <h2 class="login-title">系统登录</h2>
        <p class="login-desc">请输入账号密码登录</p>
      </div>

      <!-- 登录表单 -->
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- 用户名输入框 -->
        <div class="form-group">
          <label class="form-label" for="username">用户名</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <input
              id="username"
              v-model.trim="form.username"
              type="text"
              class="form-input"
              placeholder="请输入用户名"
              :disabled="isLoading"
              @blur="validateField('username')"
            />
          </div>
          <p v-if="formErrors.username" class="error-message">{{ formErrors.username }}</p>
        </div>

        <!-- 密码输入框 -->
        <div class="form-group">
          <label class="form-label" for="password">密码</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <input
              id="password"
              v-model.trim="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请输入密码"
              :disabled="isLoading"
              @blur="validateField('password')"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showPassword = !showPassword"
              :disabled="isLoading"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path v-if="!showPassword" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle v-if="!showPassword" cx="12" cy="12" r="3"></circle>
                <path v-if="showPassword" d="M23 12l-2.44-2.78.34-3.68-3.61-.82-1.89-3.18L12 3 8.6 1.54 6.71 4.72l-3.61.81.34 3.68L1 12l2.44 2.78-.34 3.69 3.61.82 1.89 3.18L12 21l3.4 1.46 1.89-3.18 3.61-.82-.34-3.68L23 12z"></path>
                <line v-if="showPassword" x1="1" y1="12" x2="23" y2="12"></line>
              </svg>
            </button>
          </div>
          <p v-if="formErrors.password" class="error-message">{{ formErrors.password }}</p>
        </div>

        <!-- 记住密码和忘记密码 -->
        <div class="form-actions">
          <label class="remember-checkbox">
            <input
              type="checkbox"
              v-model="form.remember"
              :disabled="isLoading"
            />
            <span class="checkbox-text">记住我</span>
          </label>
          <a href="#" class="forgot-password" :disabled="isLoading">忘记密码?</a>
        </div>

        <!-- 登录按钮 -->
        <button
          type="submit"
          class="login-btn"
          :disabled="isLoading"
        >
          <span v-if="!isLoading">登录</span>
          <span v-if="isLoading" class="loading-spinner">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M16 12a4 4 0 0 1-4 4"></path>
            </svg>
          </span>
        </button>
      </form>

      <!-- 注册链接 -->
      <div class="register-link">
        还没有账号? <a href="#">立即注册</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../utils/api.js';
// 路由实例
const router = useRouter();

// 表单数据
const form = ref({
  username: '',
  password: '',
  remember: false
});

// 状态管理
const showPassword = ref(false);
const isLoading = ref(false);
const formErrors = ref({});

/**
 * 验证单个字段
 * @param {string} field - 字段名
 */
const validateField = (field) => {
  formErrors.value[field] = '';
  
  switch (field) {
    case 'username':
      if (!form.value.username) {
        formErrors.value.username = '用户名不能为空';
      }
      break;
    case 'password':
      if (!form.value.password) {
        formErrors.value.password = '密码不能为空';
      } else if (form.value.password.length < 6) {
        formErrors.value.password = '密码长度不能少于6位';
      }
      break;
  }
};

/**
 * 表单整体验证
 * @returns {boolean} 是否验证通过
 */
const validateForm = () => {
  const errors = {};
  
  // 验证用户名
  if (!form.value.username) {
    errors.username = '用户名不能为空';
  }
  
  // 验证密码
  if (!form.value.password) {
    errors.password = '密码不能为空';
  } else if (form.value.password.length < 6) {
    errors.password = '密码长度不能少于6位';
  }
  
  formErrors.value = errors;
  return Object.keys(errors).length === 0;
};

/**
 * 登录处理函数（框架）
 */
const handleLogin = async () => {
  // 表单验证
  if (!validateForm()) return;
  
  try {
    // 登录中状态
    isLoading.value = true;
    
    // 发送登录请求
    const response = await apiService.post('/api/login', {
      username: form.value.username,
      password: form.value.password
    });
    
    // 解析响应
    // const result = await response.json();
    const result = response;
    
    if (result.success) {
      // 登录成功处理
      if (form.value.remember) {
        localStorage.setItem('userInfo', JSON.stringify({ username: form.value.username }));
      } else {
        sessionStorage.setItem('userInfo', JSON.stringify({ username: form.value.username }));
      }
      
      // 跳转到首页
      console.log('登录成功，跳转到首页');
      // 实际项目中取消注释下面的路由跳转
      // router.push('/');
      } else {
      // 登录失败处理
      console.error('登录失败');
      // 可以在这里添加错误提示，例如：
      // ElMessage.error('登录失败，请检查账号密码是否正确');
    }
  } catch (error) {
    // 错误处理
    console.error('登录失败:', error);
    // 可以在这里添加全局错误提示，例如使用 ElMessage
    // ElMessage.error('登录失败，请检查账号密码是否正确');
  } finally {
    // 恢复状态
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 全局容器 */
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

/* 登录卡片 */
.login-card {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
  padding: 40px 30px;
  backdrop-filter: blur(4px);
}

/* 登录头部 */
.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.login-desc {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

/* 表单样式 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #334155;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.form-input {
  width: 100%;
  padding: 14px 16px 14px 44px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  color: #1e293b;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  background-color: #f8fafc;
  cursor: not-allowed;
}

.input-icon {
  position: absolute;
  left: 16px;
  color: #94a3b8;
}

.toggle-password {
  position: absolute;
  right: 16px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 4px;
  transition: color 0.3s ease;
}

.toggle-password:hover {
  color: #667eea;
}

/* 错误提示 */
.error-message {
  margin: 0;
  font-size: 12px;
  color: #ef4444;
}

/* 表单操作区 */
.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.remember-checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #64748b;
  cursor: pointer;
}

.remember-checkbox input {
  width: 14px;
  height: 14px;
  accent-color: #667eea;
}

.forgot-password {
  font-size: 13px;
  color: #667eea;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #556cd6;
  text-decoration: underline;
}

.forgot-password:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  padding: 14px;
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-btn:hover {
  background: #556cd6;
}

.login-btn:disabled {
  background: #a5b4fc;
  cursor: not-allowed;
}

.loading-spinner svg {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 注册链接 */
.register-link {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: #64748b;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.register-link a:hover {
  color: #556cd6;
  text-decoration: underline;
}

/* 响应式调整 */
@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .login-title {
    font-size: 22px;
  }
  
  .form-input {
    padding: 12px 14px 12px 40px;
  }
  
  .login-btn {
    padding: 12px;
    font-size: 14px;
  }
}
</style>