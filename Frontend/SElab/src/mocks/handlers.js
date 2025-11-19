import { http, HttpResponse } from 'msw'

export const handlers = [
    // login handler
    //  POST方法，发送json如下：
    // {
    //     "username": "***",
    //     "password": "***"
    // }
    // 返回的json格式：
    // {
    //     // bool 类型
    //     "success": true
    // }
    http.post('/api/login', async ({ request }) => {
        console.log('Mocked login request received')
        const { username, password } = await request.json()
        if (username === 'admin' && password === 'password') {
            return HttpResponse.json({ success: true })
        } else if (username === 'user' && password === 'password') {
            return HttpResponse.json({ success: true })
        }
        console.log('failed login attempt')
        return HttpResponse.json({ success: false })
    }),

]