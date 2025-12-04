<template>
  <div class="dashboard-container">
    <!-- 导航栏 -->
    <nav class="dashboard-nav">
      <div class="nav-content">
        <h1 class="nav-logo">电影推荐系统</h1>
        <span class="user-info">欢迎，用户 {{ userInfo.user_id }}</span>
        <div class="nav-actions">
          <div class="dropdown">
            <button class="user-menu-btn" @click="showUserMenu = !showUserMenu">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6"/>
              </svg>
            </button>
            
            <!-- 下拉菜单 -->
            <div class="dropdown-menu" v-if="showUserMenu">
              <button class="dropdown-item" @click="showPreferenceModal = true; showUserMenu = false">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="3"></circle>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              偏好设置
              </button>
              
              <button class="dropdown-item" @click="showChangePasswordModal = true; showUserMenu = false">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
                修改密码
              </button>
              
              <div class="dropdown-divider"></div>
              
              <button class="dropdown-item logout" @click="handleLogout">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16,17 21,12 16,7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                退出登录
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main class="dashboard-main">
      <div class="dashboard-header">
        <h2 class="dashboard-title">为您推荐</h2>
        <button 
          class="refresh-btn"
          @click="fetchMovies"
          :disabled="isLoading"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M23 4v6h-6"></path>
            <path d="M1 20v-6h6"></path>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10"></path>
            <path d="M20.49 15a9 9 0 0 1-14.85 3.36L1 14"></path>
          </svg>
          刷新推荐
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M16 12a4 4 0 0 1-4 4"></path>
          </svg>
        </div>
        <p>正在加载推荐电影...</p>
      </div>

      <!-- 错误提示 -->
      <div v-if="fetchError" class="error-container">
        <div class="error-message">
          {{ fetchError }}
        </div>
        <button class="retry-btn" @click="fetchMovies">重试</button>
      </div>

      <!-- 电影卡片网格 -->
      <div v-if="!isLoading && !fetchError" class="movies-grid">
        <div 
          v-for="(movie, index) in movies" 
          :key="index" 
          class="movie-card"
          @click="showMovieDetails(movie)"
        >
          <div class="movie-poster">
            <div class="poster-placeholder">
              <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21,15 16,10 5,21"></polyline>
              </svg>
            </div>
          </div>
          <div class="movie-info">
            <h3 class="movie-title">{{ movie.movie_name }}</h3>
            <div class="movie-meta">
              <span class="movie-year">年份: {{ movie.release_year }}</span>
              <span class="movie-rating-info">评分: {{ movie.avg_rating }}/5 ({{ movie.vote_count }}票)</span>
            </div>
          </div>
        </div>
      </div>
    </main>
    <!-- 偏好设置模态框 -->
    <div v-if="showPreferenceModal" class="modal-overlay" @click="handlePreferenceModalClose">
      <div class="modal-content preference-modal" @click.stop>
        <button class="modal-close" @click="showPreferenceModal = false">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <div class="modal-header">
          <h2>偏好设置</h2>
          <p class="preference-subtitle">选择您喜欢的电影类型</p>
        </div>
        <div class="modal-body">
          <div class="preference-grid">
            <button
              v-for="category in movieCategories"
              :key="category"
              class="preference-btn"
              :class="{ active: userPreferences.includes(category) }"
              @click="togglePreference(category)"
            >
              {{ category }}
            </button>
          </div>
        </div>
        <div class="modal-footer">
          <button class="save-btn" @click="savePreferences" :disabled="isSavingPreferences">
            {{ isSavingPreferences ? '保存中...' : '保存偏好' }}
          </button>
          <button class="cancel-btn" @click="showPreferenceModal = false">取消</button>
        </div>
      </div>
    </div>

    <!-- 电影详情模态框 -->
    <div v-if="selectedMovie" class="modal-overlay" @click="selectedMovie = null">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="selectedMovie = null">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        <div class="modal-header">
          <h2>{{ selectedMovie.movie_name }}</h2>
          <span class="movie-type-badge">{{ selectedMovie.movie_type }}</span>
        </div>
        <div class="modal-body">
          <div class="movie-short-comment" v-if="selectedMovie.short_comment">
            <h3>电影简介</h3>
            <p>{{ selectedMovie.short_comment }}</p>
          </div>
          <div class="movie-stats">
            <div class="stat-item">
              <span class="stat-label">上映年份:</span>
              <span class="stat-value">{{ selectedMovie.release_year }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">平均评分:</span>
              <span class="stat-value">{{ selectedMovie.avg_rating }}/5</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">投票数:</span>
              <span class="stat-value">{{ selectedMovie.vote_count }}</span>
            </div>
          </div>
        </div>
        <div class="modal-rating">
            <div class="rating-controls">
              <span class="rating-label">您的评分:</span>
              <select 
                class="rating-select"
                :value="userRatings[selectedMovie.movie_id] || ''"
                @change="handleRatingSelect(selectedMovie, $event)"
              >
                <option value="" disabled>请选择</option>
                <option v-for="rating in ratingOptions" :key="rating" :value="rating">
                  {{ rating }}
                </option>
              </select>
            </div>
            <span class="rating-text">
              {{ userRatings[selectedMovie.movie_id] ? `已评分: ${userRatings[selectedMovie.movie_id]}/5` : '点击选择评分' }}
            </span>
        </div>
      </div>
    </div>
    <!-- 在模态框部分添加修改密码模态框 -->
    <div v-if="showChangePasswordModal" class="modal-overlay" @click="handleChangePasswordModalClose">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="showChangePasswordModal = false">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
        
        <div class="modal-header">
          <h2>修改密码</h2>
          <p class="password-subtitle">请设置新的登录密码</p>
        </div>
        
        <div class="modal-body">
          <form class="password-form" @submit.prevent="handleChangePassword">
            <div class="form-group">
              <label for="newPassword" class="form-label">新密码</label>
              <input
                id="newPassword"
                v-model="newPassword"
                type="password"
                class="form-input"
                placeholder="请输入新密码"
                required
                minlength="6"
              />
            </div>
            
            <div class="form-group">
              <label for="confirmPassword" class="form-label">确认新密码</label>
              <input
                id="confirmPassword"
                v-model="confirmPassword"
                type="password"
                class="form-input"
                placeholder="请再次输入新密码"
                required
                minlength="6"
              />
            </div>
            
            <div v-if="passwordError" class="password-error">
              {{ passwordError }}
            </div>
            
            <div class="password-requirements">
              <p>密码要求：</p>
              <ul>
                <li :class="{ 'met': newPassword.length >= 6 }">至少6个字符</li>
                <li :class="{ 'met': hasUpperCase && hasLowerCase }">包含大小写字母</li>
                <li :class="{ 'met': hasNumber }">包含数字</li>
              </ul>
            </div>
          </form>
        </div>
        
        <div class="modal-footer">
          <button 
            class="save-btn" 
            @click="handleChangePassword"
            :disabled="isChangingPassword || !isPasswordValid"
          >
            {{ isChangingPassword ? '修改中...' : '确认修改' }}
          </button>
          <button class="cancel-btn" @click="showChangePasswordModal = false">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { apiService } from '../utils/api.js';
import { computed } from 'vue';

// 路由实例
const router = useRouter();

// 用户信息
const userInfo = ref({
  user_id: null
});

// 状态管理
const isLoading = ref(false);
const fetchError = ref('');
const movies = ref([]);
const selectedMovie = ref(null);
const userRatings = ref({});

// 新增：偏好设置相关状态
const showPreferenceModal = ref(false);
const userPreferences = ref([]);
const isSavingPreferences = ref(false);
// 电影类别列表
const movieCategories = ref([
  'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
  'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
  'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
  'Thriller', 'War', 'Western'
]);
// 新增：推荐次数记录
const recordTimes = ref(0);
// 新增：标记是否有评分操作
const hasRated = ref(false);

// 在原有的响应式变量中添加
const showUserMenu = ref(false);
const showChangePasswordModal = ref(false);
const newPassword = ref('');
const confirmPassword = ref('');
const passwordError = ref('');
const isChangingPassword = ref(false);

// ================== 密码修改相关逻辑 ==================

// 计算属性：密码验证
const hasUpperCase = computed(() => /[A-Z]/.test(newPassword.value));
const hasLowerCase = computed(() => /[a-z]/.test(newPassword.value));
const hasNumber = computed(() => /[0-9]/.test(newPassword.value));
const isPasswordValid = computed(() => {
  // return newPassword.value.length >= 6 && 
  //        newPassword.value === confirmPassword.value &&
  //        hasUpperCase.value && 
  //        hasLowerCase.value && 
  //        hasNumber.value;
  return newPassword.value.length >= 6 && 
         newPassword.value === confirmPassword.value;
});
// 点击外部关闭下拉菜单
const handleClickOutside = (event) => {
  if (!event.target.closest('.dropdown')) {
    showUserMenu.value = false;
  }
};

// 修改密码处理
const handleChangePassword = async () => {
  if (!isPasswordValid.value) {
    passwordError.value = '请确保密码符合要求且两次输入一致';
    return;
  }
  
  try {
    isChangingPassword.value = true;
    passwordError.value = '';
    
    const response = await apiService.post('/api/change_password', {
      user_id: Number(userInfo.value.user_id),
      new_password: newPassword.value
    });
    
    if (response.success) {
      console.log('密码修改成功');
      showChangePasswordModal.value = false;
      // 清空表单
      newPassword.value = '';
      confirmPassword.value = '';
      // 可以添加成功提示
      alert('密码修改成功！');
    } else {
      passwordError.value = response.message || '密码修改失败，请重试';
    }
  } catch (error) {
    console.error('修改密码请求失败:', error);
    passwordError.value = '修改密码失败，请检查网络连接';
  } finally {
    isChangingPassword.value = false;
  }
};

// 处理修改密码模态框关闭
const handleChangePasswordModalClose = () => {
  showChangePasswordModal.value = false;
  // 清空表单和错误信息
  newPassword.value = '';
  confirmPassword.value = '';
  passwordError.value = '';
};


/**
 * 切换偏好选择
 */
const togglePreference = (category) => {
  const index = userPreferences.value.indexOf(category);
  if (index > -1) {
    userPreferences.value.splice(index, 1);
  } else {
    userPreferences.value.push(category);
  }
};

/**
 * 保存用户偏好
 */
const savePreferences = async () => {
  if (!userInfo.value.user_id) return;
  
  try {
    isSavingPreferences.value = true;
    
    const response = await apiService.post('/api/like', {
      user_id: Number(userInfo.value.user_id),
      like: userPreferences.value
    });
    
    if (response.success) {
      console.log('保存偏好成功');
      showPreferenceModal.value = false;
      
      // 刷新电影推荐
      if (userPreferences.value.length > 0) {
        await fetchMovies();
      }
    } else {
      console.error('保存偏好失败:', response.message);
      fetchError.value = '保存偏好失败，请重试';
    }
  } catch (error) {
    console.error('保存偏好请求失败:', error);
    fetchError.value = '保存偏好失败，请检查网络连接';
  } finally {
    isSavingPreferences.value = false;
  }
};

/**
 * 处理偏好模态框关闭
 */
const handlePreferenceModalClose = () => {
  showPreferenceModal.value = false;
};


// ================= 电影推荐相关逻辑 ==================

// 评分选项 (0.5-5分，粒度为0.5)
const ratingOptions = computed(() => {
  const options = [];
  for (let i = 0.5; i <= 5; i += 0.5) {
    options.push(i.toFixed(1));
  }
  return options;
});

/**
 * 获取用户偏好
 */
const fetchUserPreferences = async () => {
  if (!userInfo.value.user_id) return;
  
  try {
    const response = await apiService.post('/api/like_query', {
      user_id: Number(userInfo.value.user_id)
    });
    
    if (response.success) {
      userPreferences.value = response.like || [];
      console.log('获取用户偏好成功:', userPreferences.value);
      
      // 如果用户偏好为空，自动打开偏好设置模态框
      if (userPreferences.value.length === 0) {
        showPreferenceModal.value = true;
      }
    } else {
      console.error('获取用户偏好失败:', response.message);
    }
  } catch (error) {
    console.error('获取用户偏好请求失败:', error);
  }
};
/**
 * 获取用户信息
 */
const getUserInfo = async () => {
  // 优先从sessionStorage获取（当前会话）
  let storedInfo = sessionStorage.getItem('userInfo');
  
  // 如果sessionStorage中没有，尝试从localStorage获取（持久化存储）
  if (!storedInfo) {
    storedInfo = localStorage.getItem('userInfo');
  }
  
  if (storedInfo) {
    userInfo.value = JSON.parse(storedInfo);
    console.log('获取用户信息成功:', userInfo.value);
    // 获取用户偏好
    await fetchUserPreferences();
  } else {
    // 如果没有用户信息，跳转到登录页
    console.log('未找到用户信息，跳转到登录页');
    router.push('/login');
  }
};

/**
 * 获取电影推荐
 */
const fetchMovies = async () => {
  if (!userInfo.value.user_id) return;
  
  try {
    isLoading.value = true;
    fetchError.value = '';
    
    // 发送请求获取推荐电影
    const response = await apiService.post('/api/recommend', {
      user_id: Number(userInfo.value.user_id),
      record_times: recordTimes.value
    });
    
    // 解析响应
    const result = response;
    
    if (result.success) {
      movies.value = result.recommend_movies || [];
      if (movies.value.length === 0) {
        fetchError.value = '暂无推荐电影';
      }
      if (hasRated.value) {
        recordTimes.value = 0;
        hasRated.value = false; // 重置标记
      } else {
        recordTimes.value += 1;
      }
    } else {
      fetchError.value = result.message || '获取推荐失败';
    }
  } catch (error) {
    console.error('获取电影推荐失败:', error);
    fetchError.value = '获取推荐失败，请稍后重试';
  } finally {
    isLoading.value = false;
  }
};

/**
 * 截断电影内容简介
 */
// const truncateContent = (content) => {
//   if (!content) return '';
//   return content.length > 100 ? content.substring(0, 100) + '...' : content;
// };

// ================= 电影详情和评分相关逻辑 ==================

/**
 * 显示电影详情
 */
const showMovieDetails = (movie) => {
  console.log('显示电影详情:', movie);
  selectedMovie.value = movie;
};

/**
 * 对电影进行评分
 */
const handleRatingSelect = async (movie, event) => {
  const rating = event.target.value;
  
  if (!rating) return;
  
  // 更新本地评分状态
  userRatings.value[movie.movie_id] = rating;
  
  try {
    // 更新API路径和参数格式
    const response = await apiService.post('/api/judge', {
      user_id: Number(userInfo.value.user_id),
      movie_id: Number(movie.movie_id),
      rating: parseFloat(rating)
    });
    
    if (response.success) {
      console.log('评分成功');
      hasRated.value = true; // 标记已进行评分操作
      // 刷新电影列表以更新平均评分
      // await fetchMovies();
    } else {
      console.error('评分失败:', response.message);
      delete userRatings.value[movie.movie_id];
    }
  } catch (error) {
    console.error('评分请求失败:', error);
    delete userRatings.value[movie.movie_id];
  }
};

// const rateMovie = (movie, rating) => {
//   // 更新本地评分状态
//   userRatings.value[movie.movie_name] = rating;
  
//   // 在实际应用中，这里应该发送评分到后端
//   console.log(`用户 ${userInfo.value.user_id} 对电影 "${movie.movie_name}" 评分: ${rating}`);
  
//   // 模拟发送评分到后端
//   // apiService.post('/api/movies/rate', {
//   //   user_id: userInfo.value.user_id,
//   //   movie_name: movie.movie_name,
//   //   rating: rating
//   // });
// };


/**
 * 退出登录
 */
const handleLogout = () => {
  // 清除存储的用户信息
  localStorage.removeItem('userInfo');
  sessionStorage.removeItem('userInfo');
  
  // 跳转到登录页
  router.push('/login');
};

// 组件挂载时获取用户信息和电影推荐
onMounted(() => {
  getUserInfo();
  fetchMovies();
  document.addEventListener('click', handleClickOutside);
});

// 组件卸载时移除事件监听
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

</script>

<style scoped>
/* 全局容器 */
.dashboard-container {
  min-height: 100vh;
  background: #f8fafc;
  width: 100%;
  max-width: none;
  padding: 30px 20px;
}

/* 导航栏 */
.dashboard-nav {
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  max-width: none; /* 移除导航栏宽度限制 */
  padding: 0 20px;
  top: 0;
  z-index: 100;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.nav-logo {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  font-size: 14px;
  color: #64748b;
}

.logout-btn {
  padding: 8px 16px;
  background: #ef4444;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.logout-btn:hover {
  background: #dc2626;
}

/* 主要内容区域 */
.dashboard-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: #556cd6;
}

.refresh-btn:disabled {
  background: #a5b4fc;
  cursor: not-allowed;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #64748b;
}

.loading-spinner svg {
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 错误提示 */
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  text-align: center;
}

.error-message {
  padding: 16px 20px;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #dc2626;
  font-size: 16px;
  margin-bottom: 20px;
}

.retry-btn {
  padding: 10px 20px;
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.retry-btn:hover {
  background: #556cd6;
}

/* 电影卡片网格 */
.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.movie-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.movie-poster {
  height: 180px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.poster-placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.movie-info {
  padding: 20px;
}

.movie-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.movie-type {
  font-size: 14px;
  color: #667eea;
  margin: 0 0 12px 0;
  font-weight: 500;
}

.movie-content {
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
  margin: 0;
}

.movie-rating {
  padding: 0 20px 20px;
  border-top: 1px solid #f1f5f9;
  margin-top: 16px;
  padding-top: 16px;
}

.rating-stars {
  display: flex;
  margin-bottom: 8px;
}

.rating-stars.large {
  margin-bottom: 12px;
}

.star {
  font-size: 20px;
  color: #e2e8f0;
  cursor: pointer;
  transition: color 0.2s ease;
  margin-right: 4px;
}

.rating-stars.large .star {
  font-size: 28px;
  margin-right: 6px;
}

.star:hover,
.star.active {
  color: #fbbf24;
}

.rating-text {
  font-size: 13px;
  color: #94a3b8;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #fff;
  border-radius: 12px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
}

.modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #64748b;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.3s ease;
}

.modal-close:hover {
  background: #f1f5f9;
}

.modal-header {
  padding: 30px 30px 20px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h2 {
  margin: 0;
  font-size: 24px;
  color: #1e293b;
}

.movie-type-badge {
  background: #667eea;
  color: #fff;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.modal-body {
  padding: 20px 30px;
}

.modal-body p {
  font-size: 16px;
  line-height: 1.6;
  color: #475569;
  margin: 0;
}

.modal-rating {
  padding: 20px 30px 30px;
  border-top: 1px solid #f1f5f9;
}

.modal-rating h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: #1e293b;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .nav-content {
    padding: 0 16px;
  }
  
  .dashboard-main {
    padding: 20px 16px;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .movies-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    margin: 0 16px;
  }
  
  .modal-header {
    padding: 24px 24px 16px;
  }
  
  .modal-body {
    padding: 16px 24px;
  }
  
  .modal-rating {
    padding: 16px 24px 24px;
  }
}
/* 新增样式 */
.movie-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 12px;
}

.movie-card::after {
  content: "点击查看详情和评分";
  display: block;
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
  padding: 10px 20px 20px;
  border-top: 1px solid #f1f5f9;
  margin-top: 16px;
}
.movie-year, .movie-rating-info {
  font-size: 14px;
  color: #64748b;
}

.rating-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.rating-label {
  font-size: 13px;
  color: #64748b;
}

.rating-select {
  padding: 4px 8px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  font-size: 13px;
}

.movie-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-weight: 500;
  color: #374151;
}

.stat-value {
  color: #6b7280;
}
/* 新增偏好设置按钮样式 */
.preference-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: #0ea06f;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.preference-btn:hover {
  background: #059669;
}

/* 偏好设置模态框样式 */
.preference-modal {
  max-width: 800px;
}

.preference-subtitle {
  margin: 8px 0 0 0;
  color: #64748b;
  font-size: 14px;
}

.preference-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.preference-grid .preference-btn {
  padding: 12px 16px;
  background: #f8fafc;
  color: #475569;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-align: center;
  justify-content: center;
}

.preference-grid .preference-btn:hover {
  border-color: #667eea;
  background: #f0f4ff;
}

.preference-grid .preference-btn.active {
  background: #667eea;
  color: #fff;
  border-color: #667eea;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding: 20px 30px 30px;
  border-top: 1px solid #f1f5f9;
}

.save-btn {
  padding: 10px 20px;
  background: #667eea;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.save-btn:hover:not(:disabled) {
  background: #556cd6;
}

.save-btn:disabled {
  background: #a5b4fc;
  cursor: not-allowed;
}

.cancel-btn {
  padding: 10px 20px;
  background: #f1f5f9;
  color: #64748b;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.cancel-btn:hover {
  background: #e2e8f0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .preference-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 8px;
  }
  
  .preference-grid .preference-btn {
    padding: 10px 12px;
    font-size: 13px;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}

/* 新增下拉菜单样式 */
.dropdown {
  position: relative;
  display: inline-block;
}

.user-menu-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #64748b;
}

.user-menu-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  min-width: 180px;
  z-index: 1000;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 12px 16px;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  font-size: 14px;
  color: #475569;
  transition: background 0.3s ease;
}

.dropdown-item:hover {
  background: #f8fafc;
}

.dropdown-item.logout {
  color: #ef4444;
}

.dropdown-item.logout:hover {
  background: #fef2f2;
}

.dropdown-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 4px 0;
}

/* 修改密码表单样式 */
.password-form {
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
  font-weight: 500;
  color: #374151;
  font-size: 14px;
}

.form-input {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.password-error {
  padding: 12px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  color: #dc2626;
  font-size: 14px;
}

.password-requirements {
  padding: 16px;
  background: #f8fafc;
  border-radius: 6px;
  font-size: 13px;
}

.password-requirements p {
  margin: 0 0 8px 0;
  font-weight: 500;
  color: #64748b;
}

.password-requirements ul {
  margin: 0;
  padding-left: 16px;
  color: #94a3b8;
}

.password-requirements li.met {
  color: #10b981;
  text-decoration: line-through;
}

.password-subtitle {
  margin: 8px 0 0 0;
  color: #64748b;
  font-size: 14px;
}

/* 移除原有的偏好设置按钮和退出登录按钮样式 */
.nav-actions .preference-btn,
.nav-actions .logout-btn {
  display: none;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .dropdown-menu {
    right: -10px;
    min-width: 160px;
  }
  
  .user-menu-btn {
    padding: 6px 10px;
    font-size: 13px;
  }
}
</style>