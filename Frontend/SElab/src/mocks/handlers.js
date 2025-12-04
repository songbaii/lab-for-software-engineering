import { http, HttpResponse } from 'msw'
// 模拟用户偏好数据存储
const userPreferences = new Map()

// 初始化一些测试用户的偏好数据
userPreferences.set(123456, ['Action', 'Drama', 'Sci-Fi'])
userPreferences.set(350234, ['Comedy', 'Romance'])
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
    // 推荐电影接口 handler
    // POST /api/recommend
    // 请求体: { user_id: number }
    // 响应: { success: boolean, message?: string, movies?: array }
    http.post('/api/recommend', async ({ request }) => {
        console.log('Mocked recommend request received')
        const { user_id } = await request.json()
        
        // 验证用户ID
        if (typeof user_id !== 'number') {
            return HttpResponse.json({ 
                success: false, 
                message: '用户ID必须是数字类型',
                movies: []
            })
        }

        // 模拟推荐电影数据
        const mockMovies = [
            {
                movie_id: 1,
                movie_name: "肖申克的救赎",
                release_year: 1994,
                avg_rating: 4.3,
                vote_count: 2500000,
                short_comment: "希望让人自由，这是一部关于友谊和救赎的经典之作。"
            },
            {
                movie_id: 2,
                movie_name: "教父",
                release_year: 1972,
                avg_rating: 4.2,
                vote_count: 1800000,
                short_comment: "黑帮电影的巅峰之作，马龙·白兰度的表演堪称传奇。"
            },
            {
                movie_id: 3,
                movie_name: "黑暗骑士",
                release_year: 2008,
                avg_rating: 4.0,
                vote_count: 2600000,
                short_comment: "希斯·莱杰的小丑表演让这部超级英雄电影成为艺术。"
            },
            {
                movie_id: 4,
                movie_name: "阿甘正传",
                release_year: 1994,
                avg_rating: 3.8,
                vote_count: 2000000,
                short_comment: "生活就像一盒巧克力，你永远不知道下一颗是什么味道。"
            },
            {
                movie_id: 5,
                movie_name: "指环王：王者归来",
                release_year: 2003,
                avg_rating: 3.9,
                vote_count: 1800000,
                short_comment: "史诗奇幻的终极篇章，中土世界的完美收官。"
            },
            {
                movie_id: 6,
                movie_name: "泰坦尼克号",
                release_year: 1997,
                avg_rating: 2.9,
                vote_count: 1200000,
                short_comment: "跨越阶级的爱情故事，永恒的经典浪漫。"
            },
            {
                movie_id: 7,
                movie_name: "盗梦空间",
                release_year: 2010,
                avg_rating: 3.8,
                vote_count: 2200000,
                short_comment: "诺兰的梦境迷宫，颠覆想象的科幻巨作。"
            },
            {
                movie_id: 8,
                movie_name: "星际穿越",
                release_year: 2014,
                avg_rating: 3.6,
                vote_count: 1700000,
                short_comment: "爱与物理的完美结合，震撼的宇宙探索之旅。"
            },
            {
                movie_id: 9,
                movie_name: "霸王别姬",
                release_year: 1993,
                avg_rating: 4.0,
                vote_count: 1500000,
                short_comment: "戏如人生，人生如戏，中国电影的巅峰之作。"
            },
            {
                movie_id: 10,
                movie_name: "这个杀手不太冷",
                release_year: 1994,
                avg_rating: 4.0,
                vote_count: 1900000,
                short_comment: "大叔与萝莉的温情故事，让·雷诺的经典角色。"
            },
            {
                movie_id: 11,
                movie_name: "辛德勒的名单",
                release_year: 1993,
                avg_rating: 4.0,
                vote_count: 1300000,
                short_comment: "黑白影像中的历史伤痛，人性的光辉与黑暗。"
            },
            {
                movie_id: 12,
                movie_name: "千与千寻",
                release_year: 2001,
                avg_rating: 4.0,
                vote_count: 1600000,
                short_comment: "宫崎骏的奇幻世界，成长与勇气的美丽寓言。"
            }
        ]

        // 生成随机数量（0-8）
        const randomCount = Math.floor(Math.random() * 9) // 0-8的随机整数
        
        // 随机选择电影
        const shuffledMovies = [...mockMovies].sort(() => 0.5 - Math.random())
        const selectedMovies = shuffledMovies.slice(0, randomCount)

        console.log(`Returning ${selectedMovies.length} recommended movies for user ${user_id}`)
        
        return HttpResponse.json({
            success: true,
            message: '获取推荐成功',
            recommend_movies: selectedMovies
        })
    }),
    // 评分接口 handler
    // POST /api/judge
    // 请求体: { user_id: number, movie_id: number, rating: number }
    // 响应: { success: boolean, message?: string }
    http.post('/api/judge', async ({ request }) => {
        console.log('Mocked judge request received')
        const { user_id, movie_id, rating } = await request.json()
        
        // 验证参数
        if (typeof user_id !== 'number') {
            return HttpResponse.json({ 
                success: false, 
                message: '用户ID必须是数字类型' 
            })
        }
        
        if (typeof movie_id !== 'number') {
            return HttpResponse.json({ 
                success: false, 
                message: '电影ID必须是数字类型' 
            })
        }
        
        if (typeof rating !== 'number' || rating < 0.5 || rating > 10) {
            return HttpResponse.json({ 
                success: false, 
                message: '评分必须是0.5到10之间的数字' 
            })
        }

        console.log(`User ${user_id} rated movie ${movie_id} with ${rating} stars`)
        
        // 模拟评分成功
        return HttpResponse.json({
            success: true,
            message: '评分成功'
        })
    }),
    // 新增：用户偏好查询接口
    http.post('/api/like_query', async ({ request }) => {
        console.log('Mocked like_query request received')
        const { user_id } = await request.json()
        
        // 验证用户ID
        if (typeof user_id !== 'number') {
            return HttpResponse.json({ 
                success: false, 
                message: '用户ID必须是数字类型',
                like: []
            })
        }

        // 查询用户偏好
        const preferences = userPreferences.get(user_id) || []
        console.log(`Query preferences for user ${user_id}:`, preferences)
        
        return HttpResponse.json({
            success: true,
            message: '偏好查询成功',
            like: preferences
        })
    }),

    // 新增：用户偏好设置接口
    http.post('/api/like', async ({ request }) => {
        console.log('Mocked like request received')
        const { user_id, like } = await request.json()
        
        // 验证参数
        if (typeof user_id !== 'number') {
            return HttpResponse.json({ 
                success: false, 
                message: '用户ID必须是数字类型'
            })
        }
        
        // 验证偏好数组
        if (!Array.isArray(like)) {
            return HttpResponse.json({ 
                success: false, 
                message: '用户喜好必须是数组类型'
            })
        }

        // 验证数组中的每个元素都是有效的电影类别
        const validCategories = [
            'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
            'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
        ]
        
        const invalidCategories = like.filter(category => 
            !validCategories.includes(category)
        )
        
        if (invalidCategories.length > 0) {
            return HttpResponse.json({ 
                success: false, 
                message: `无效的电影类别: ${invalidCategories.join(', ')}`
            })
        }

        // 更新用户偏好
        userPreferences.set(user_id, like)
        console.log(`Updated preferences for user ${user_id}:`, like)
        
        return HttpResponse.json({
            success: true,
            message: '偏好设置成功'
        })
    }),
    // 修改密码接口 handler
    // POST /api/change_password
    // 请求体: { "user_id": "用户账号" number, "new_password": "新密码" string类型 }
    // 响应: { "success": "修改结果" boolean类型， "message": "提示信息" string类型 }
    http.post('/api/change_password', async ({ request }) => {
        console.log('Mocked change_password request received')
        const { user_id, new_password } = await request.json()
        // 验证new_password
        if (typeof new_password !== 'string') {
            return HttpResponse.json({ 
                success: false, 
                message: '新密码必须是字符串类型' 
            })
        } else if (new_password.length < 6) {
            return HttpResponse.json({ 
                success: false, 
                message: '新密码长度必须至少为6个字符' 
            })
        } else {
            console.log(`Password changed for user ID: ${user_id}`)
            return HttpResponse.json({
                success: true,
                message: '密码修改成功'
            })
        }
    })
]