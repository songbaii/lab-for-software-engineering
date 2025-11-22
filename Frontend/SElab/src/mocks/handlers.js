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
    // register handler
    // 注册部分

    // ```
    // 对应路由: '/api/register', methods=['POST']
    // 接收JSON格式: {"user_name": "用户账号" s't'r类型, "password": "密码" string类型}
    // 返回的JSON: {"success": "登录结果" boolean类型, "message": "提示信息" string类型, "user_id": "分配的用户账号" number类型}
    // ```
    http.post('/api/register', async ({ request }) => {
        console.log('Mocked register request received')
        const { user_name, password } = await request.json()
        if (typeof user_name !== 'string' || typeof password !== 'string') {
            return HttpResponse.json({ 
                success: false, 
                message: '用户名和密码必须是字符串类型',
                user_id: null
            })
        } else if (user_name.length === 0 || password.length === 0) {
            return HttpResponse.json({ 
                success: false,
                message: '用户名和密码不能为空',
                user_id: null
            })
        } else {
            // 模拟分配一个用户ID
            const user_id = Math.floor(Math.random() * 900000) + 100000; // 生成一个6位数的用户ID
            console.log(`Registered new user: ${user_name} with ID: ${user_id}`)
            return HttpResponse.json({
                success: true,
                message: '注册成功',
                user_id: user_id
            })
        }
    }),
]