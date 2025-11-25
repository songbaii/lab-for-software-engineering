from llm_client import llm_client
from prompts import generate_movie_review_prompt, generate_movie_summary_prompt
import json

def generate_movie_review_interface(movie_data):
    """
    电影短评生成接口
    
    参数:
        movie_data: 包含电影信息的字典，格式如下:
            {
                "movie_title": "电影标题",
                "movie_info": "电影信息(可选)",
                "model": "模型名称(可选，默认gpt-4o-mini)",
                "max_tokens": "最大token数(可选，默认500)",
                "temperature": "温度参数(可选，默认0.7)"
            }
    
    返回:
        dict: 包含生成结果或错误信息的字典
    """
    try:
        # 验证必要字段
        if not movie_data or 'movie_title' not in movie_data:
            return {
                "success": False,
                "error": {
                    "code": "MISSING_FIELD",
                    "message": "缺少必要字段: movie_title"
                }
            }
        
        # 设置默认值
        movie_title = movie_data.get("movie_title", "")
        movie_info = movie_data.get("movie_info", "")
        model = movie_data.get("model", "gpt-4o-mini")
        max_tokens = movie_data.get("max_tokens", 500)
        temperature = movie_data.get("temperature", 0.7)
        
        # 生成电影短评提示词
        review_request = {
            "movie_title": movie_title,
            "movie_info": movie_info
        }
        
        review_prompt_json = generate_movie_review_prompt(review_request)
        prompt_content = review_prompt_json
        if isinstance(review_prompt_json, dict):
            prompt_content = json.dumps(review_prompt_json, ensure_ascii=False)
        
        # 生成内容
        content_request = {
            "prompt": prompt_content,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        content_result_json = llm_client.generate_content(content_request)
        content_result = json.loads(content_result_json)
        
        # 返回结果
        if content_result["success"]:
            return {
                "success": True,
                "data": {
                    "movie_title": movie_title,
                    "generated_review": content_result["data"]["generated_text"],
                    "model_used": model
                }
            }
        else:
            return {
                "success": False,
                "error": {
                    "code": "LLM_ERROR",
                    "message": content_result['error']['message']
                }
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": f"内部错误: {str(e)}"
            }
        }