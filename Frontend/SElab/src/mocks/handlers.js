import { http, HttpResponse } from 'msw'

export const handlers = [
    // login handler
    //  POST方法，发送json如下：
    // {
    //     "user_id": "用户账号" number类型,
    //     "password": "密码" string类型
    // }
    // 返回的json格式：
    // {
    //     "success": "登录结果" boolean类型,
    //     "message": "提示信息" string类型
    // }
    http.post('/api/login', async ({ request }) => {
        console.log('Mocked login request received')
        const { user_id, password } = await request.json()
        // 验证user_id是否为数字类型
        if (typeof user_id !== 'number') {
            return HttpResponse.json({ 
                success: false, 
                message: '用户账号必须是数字类型' 
            })
        }
        if ((user_id === 123456 || user_id === 350234) && password === 'password') {
            return HttpResponse.json({ 
                success: true, 
                message: '登录成功' 
            })
        }
        console.log('failed login attempt')
        return HttpResponse.json({ 
            success: false, 
            message: '用户账号或密码错误' 
        })
    }),

]