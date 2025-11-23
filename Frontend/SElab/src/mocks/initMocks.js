import { worker } from './browser'

export async function initMocks() {
  if (import.meta.env.VITE_APP_MSW_ENABLED === 'true') {
    await worker.start({
      onUnhandledRequest: 'bypass',
      serviceWorker: {
        url: '/mockServiceWorker.js',
      },
    })
    console.log('MSW已启动 - 使用模拟后端')
  } else {
    console.log('MSW未启动 - 使用真实后端')
  }
}