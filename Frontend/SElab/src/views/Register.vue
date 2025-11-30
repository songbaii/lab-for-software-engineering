<template>
  <div class="register-container">
    <!-- 注册卡片 -->
    <div class="register-card">
      <div class="register-header">
        <h2 class="register-title">用户注册</h2>
        <p class="register-desc">请输入账号信息完成注册</p>
      </div>

      <!-- 注册表单 -->
      <form @submit.prevent="handleRegister" class="register-form">
        <!-- 用户名输入框 -->
        <div class="form-group">
          <label class="form-label" for="user_name">用户名</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            <input
              id="user_name"
              v-model.trim="form.user_name"
              type="text"
              class="form-input"
              placeholder="请输入用户名"
              :disabled="isLoading"
              @blur="validateField('user_name')"
            />
          </div>
          <p v-if="formErrors.user_name" class="error-message">{{ formErrors.user_name }}</p>
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

        <!-- 确认密码输入框 -->
        <div class="form-group">
          <label class="form-label" for="confirmPassword">确认密码</label>
          <div class="input-wrapper">
            <svg class="input-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <input
              id="confirmPassword"
              v-model.trim="form.confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              class="form-input"
              placeholder="请再次输入密码"
              :disabled="isLoading"
              @blur="validateField('confirmPassword')"
            />
            <button
              type="button"
              class="toggle-password"
              @click="showConfirmPassword = !showConfirmPassword"
              :disabled="isLoading"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path v-if="!showConfirmPassword" d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle v-if="!showConfirmPassword" cx="12" cy="12" r="3"></circle>
                <path v-if="showConfirmPassword" d="M23 12l-2.44-2.78.34-3.68-3.61-.82-1.89-3.18L12 3 8.6 1.54 6.71 4.72l-3.61.81.34 3.68L1 12l2.44 2.78-.34 3.69 3.61.82 1.89 3.18L12 21l3.4 1.46 1.89-3.18 3.61-.82-.34-3.68L23 12z"></path>
                <line v-if="showConfirmPassword" x1="1" y1="12" x2="23" y2="12"></line>
              </svg>
            </button>
          </div>
          <p v-if="formErrors.confirmPassword" class="error-message">{{ formErrors.confirmPassword }}</p>
        </div>

        <!-- 注册错误提示 -->
        <div v-if="registerError" class="register-error-message">
          {{ registerError }}
        </div>

        <!-- 注册成功提示 -->
        <div v-if="registerSuccess" class="register-success-message">
          <p>注册成功！</p>
          <p>您的用户ID是：<strong>{{ assignedUserId }}</strong></p>
          <p>请牢记您的用户ID，用于登录系统。</p>
        </div>

        <!-- 注册按钮 -->
        <button
          type="submit"
          class="register-btn"
          :disabled="isLoading || registerSuccess"
        >
          <span v-if="!isLoading">注册</span>
          <span v-if="isLoading" class="loading-spinner">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M16 12a4 4 0 0 1-4 4"></path>
            </svg>
          </span>
        </button>
      </form>

      <!-- 登录链接 -->
      <div class="login-link">
        已有账号? <router-link to="/login">立即登录</router-link>
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
  user_name: '',
  password: '',
  confirmPassword: ''
});

// 状态管理
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const isLoading = ref(false);
const formErrors = ref({});
const registerError = ref('');
const registerSuccess = ref(false);
const assignedUserId = ref(null);

/**
 * 验证单个字段
 * @param {string} field - 字段名
 */
const validateField = (field) => {
  formErrors.value[field] = '';
  
  switch (field) {
    case 'user_name':
      if (!form.value.user_name.trim()) {
        formErrors.value.user_name = '用户名不能为空';
      } else if (form.value.user_name.length < 3) {
        formErrors.value.user_name = '用户名长度不能少于3位';
      }
      break;
    case 'password':
      if (!form.value.password) {
        formErrors.value.password = '密码不能为空';
      } else if (form.value.password.length < 6) {
        formErrors.value.password = '密码长度不能少于6位';
      }
      break;
    case 'confirmPassword':
      if (!form.value.confirmPassword) {
        formErrors.value.confirmPassword = '请确认密码';
      } else if (form.value.password !== form.value.confirmPassword) {
        formErrors.value.confirmPassword = '两次输入的密码不一致';
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
  if (!form.value.user_name.trim()) {
    errors.user_name = '用户名不能为空';
  } else if (form.value.user_name.length < 3) {
    errors.user_name = '用户名长度不能少于3位';
  }
  
  // 验证密码
  if (!form.value.password) {
    errors.password = '密码不能为空';
  } else if (form.value.password.length < 6) {
    errors.password = '密码长度不能少于6位';
  }
  
  // 验证确认密码
  if (!form.value.confirmPassword) {
    errors.confirmPassword = '请确认密码';
  } else if (form.value.password !== form.value.confirmPassword) {
    errors.confirmPassword = '两次输入的密码不一致';
  }
  
  formErrors.value = errors;
  return Object.keys(errors).length === 0;
};

/**
 * 注册处理函数
 */
const handleRegister = async () => {
  // 清除之前的错误信息
  registerError.value = '';
  registerSuccess.value = false;
  assignedUserId.value = null;
  
  // 表单验证
  if (!validateForm()) return;
  
  try {
    // 注册中状态
    isLoading.value = true;
    
    // 发送注册请求
    const response = await apiService.post('/api/register', {
      user_name: form.value.user_name,
      password: form.value.password
    });
    
    // 解析响应
    const result = response;
    
    if (result.success) {
      // 注册成功处理
      registerSuccess.value = true;
      assignedUserId.value = result.user_id;
      
      // 清空表单
      form.value = {
        user_name: '',
        password: '',
        confirmPassword: ''
      };
      
      console.log('注册成功,分配的用户ID=', result.user_id);
    } else {
      // 注册失败处理
      console.error('注册失败');
      registerError.value = result.message || '注册失败，请稍后重试';
    }
  } catch (error) {
    // 错误处理
    console.error('注册失败:', error);
    registerError.value = '注册请求失败，请稍后重试';
  } finally {
    // 恢复状态
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 全局容器 */
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  width: 100%;
  max-width: none; /* 移除最大宽度限制 */
  padding: 20px;
}

/* 注册卡片 */
.register-card {
  width: 100%;
  max-width: 420px;
  margin: 0 auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.2);
  padding: 40px 30px;
  backdrop-filter: blur(4px);
}

/* 注册头部 */
.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 8px;
}

.register-desc {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

/* 表单样式 */
.register-form {
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

.register-error-message {
  padding: 12px 16px;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #dc2626;
  font-size: 14px;
  text-align: center;
  margin-bottom: 16px;
  animation: slideDown 0.3s ease;
}

.register-success-message {
  padding: 16px;
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  color: #166534;
  font-size: 14px;
  text-align: center;
  margin-bottom: 16px;
  animation: slideDown 0.3s ease;
}

.register-success-message strong {
  font-size: 18px;
  color: #059669;
}

/* 注册按钮 */
.register-btn {
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

.register-btn:hover {
  background: #556cd6;
}

.register-btn:disabled {
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

/* 登录链接 */
.login-link {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: #64748b;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.login-link a:hover {
  color: #556cd6;
  text-decoration: underline;
}

/* 响应式调整 */
@media (max-width: 480px) {
  .register-card {
    padding: 30px 20px;
  }
  
  .register-title {
    font-size: 22px;
  }
  
  .form-input {
    padding: 12px 14px 12px 40px;
  }
  
  .register-btn {
    padding: 12px;
    font-size: 14px;
  }
}
</style>