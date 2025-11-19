import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { initMocks } from './mocks/initMocks';
import App from './App.vue'
import router from './router'

// 初始化模拟服务工作者（MSW）
initMocks().then(() => {
const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
});