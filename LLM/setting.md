## 使用api
gpt-4o-mini

## 调用格式

1.输入格式:
{
    "movie_title": "电影标题",           # 必需
    "movie_info": "电影信息",            # 可选
    "model": "模型名称",                # 可选，默认"gpt-4o-mini"
    "max_tokens": 最大token数,          # 可选，默认500
    "temperature": 温度参数             # 可选，默认0.7
}

输出格式:
{
    "success": True,
    "data": {
        "movie_title": "电影标题",
        "generated_review": "生成的短评内容",
        "model_used": "使用的模型名称"
    }
}

错误格式:
{
    "success": True,
    "data": {
        "movie_title": "电影标题",
        "generated_review": "生成的短评内容",
        "model_used": "使用的模型名称"
    }
}

## 使用示例
# 调用接口
result = generate_movie_review_interface({
    "movie_title": "肖申克的救赎",
    "movie_info": "导演：弗兰克·德拉邦特",
    "temperature": 0.8
})
