import os
import json
from openai import OpenAI

def generate_movie_review_prompt(request_data):
    """
    生成电影短评的Prompt
    :param request_data: JSON格式的请求数据
    :return: JSON格式的响应数据
    """
    try:
        if isinstance(request_data, str):
            request_data = json.loads(request_data)
        
        movie_title = request_data.get("movie_title", "")
        movie_info = request_data.get("movie_info", "")
        
        prompt = f"""
        你是一个风趣幽默的影评人。请为电影《{movie_title}》写一段100字以内的短评。
        电影信息：{movie_info}。
        要求：突出电影最吸引人的特点，语言简洁明快，带有个人观点，避免剧透。
        """
        
        result = {
            "success": True,
            "data": {
                "prompt": prompt,
                "movie_title": movie_title,
                "type": "review_prompt"
            },
            "error": None
        }
        return json.dumps(result, ensure_ascii=False)
        
    except Exception as e:
        error_result = {
            "success": False,
            "data": None,
            "error": {
                "message": f"生成电影短评提示词时出错: {e}",
                "code": "PROMPT_GENERATION_ERROR"
            }
        }
        return json.dumps(error_result, ensure_ascii=False)

def generate_movie_summary_prompt(request_data):
    """
    生成电影摘要的Prompt
    :param request_data: JSON格式的请求数据
    :return: JSON格式的响应数据
    """
    try:
        if isinstance(request_data, str):
            request_data = json.loads(request_data)
        
        movie_title = request_data.get("movie_title", "")
        movie_info = request_data.get("movie_info", "")
        
        prompt = f"""
        你是一个专业的电影编辑。请为电影《{movie_title}》写一段80字以内的剧情摘要。
        电影信息：{movie_info}。
        要求：客观中立，概括主要剧情脉络和背景设定，避免透露关键结局。
        """
        
        result = {
            "success": True,
            "data": {
                "prompt": prompt,
                "movie_title": movie_title,
                "type": "summary_prompt"
            },
            "error": None
        }
        return json.dumps(result, ensure_ascii=False)
        
    except Exception as e:
        error_result = {
            "success": False,
            "data": None,
            "error": {
                "message": f"生成电影摘要提示词时出错: {e}",
                "code": "PROMPT_GENERATION_ERROR"
            }
        }
        return json.dumps(error_result, ensure_ascii=False)