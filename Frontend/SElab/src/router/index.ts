import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue';
import Dashboard from '../views/Dashboard.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: () => {
        // 检查用户是否已登录
        const userInfo = sessionStorage.getItem('userInfo') || localStorage.getItem('userInfo');
        if (userInfo) {
          return { name: 'dashboard' };
        } else {
          return { name: 'login' };
        }
      }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { requiresGuest: true }
    },
  ],
})

// 添加路由守卫
router.beforeEach((to, from, next) => {
  // 检查用户是否已登录
  const userInfo = sessionStorage.getItem('userInfo') || localStorage.getItem('userInfo');
  const isAuthenticated = !!userInfo;

  if (to.meta.requiresAuth && !isAuthenticated) {
    // 如果需要认证但用户未登录，跳转到登录页
    next({ name: 'login' });
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // 如果要求访客但用户已登录，跳转到仪表板
    next({ name: 'dashboard' });
  } else {
    // 其他情况正常放行
    next();
  }
})

export default router
