from interface import generate_movie_review_interface 
result = generate_movie_review_interface({
    "movie_title": "肖申克的救赎",
    "movie_info": "导演：弗兰克·德拉邦特",
    "temperature": 0.8
})

# 处理结果
if result["success"]:
    print("电影短评生成成功:")
    print(f"电影: {result['data']['movie_title']}")
    print(f"短评: {result['data']['generated_review']}")
    print(f"使用模型: {result['data']['model_used']}")
else:
    print(f"错误: {result['error']['message']}")