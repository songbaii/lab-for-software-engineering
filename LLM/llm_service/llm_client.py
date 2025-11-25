import os
import json
from openai import OpenAI


class LLMClient:
    def __init__(self):
        self.api_key = 'sk-5NRAokzo8lMTP1yOnB2qZR9dOIHEhx95FurHyHChydAtQQfV'
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://ai.nengyongai.cn/v1"
        )

    def generate_content(self, request_data):
        """
        调用LLM API生成内容的核心函数
        :param request_data: JSON格式的请求数据
        :return: JSON格式的响应数据
        """
        try:
            # 解析请求数据
            if isinstance(request_data, str):
                request_data = json.loads(request_data)
            
            prompt = request_data.get("prompt", "")
            model = request_data.get("model", "gpt-4o-mini")
            max_tokens = request_data.get("max_tokens", 500)
            temperature = request_data.get("temperature", 0.7)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个专业的影评人和内容摘要专家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # 构建JSON格式的响应
            generated_text = response.choices[0].message.content.strip()
            result = {
                "success": True,
                "data": {
                    "generated_text": generated_text,
                    "model": model,
                    "tokens_used": response.usage.total_tokens if response.usage else None
                },
                "error": None
            }
            return json.dumps(result, ensure_ascii=False)
            
        except Exception as e:
            # 错误响应
            error_result = {
                "success": False,
                "data": None,
                "error": {
                    "message": f"调用LLM API时出错: {e}",
                    "code": "API_ERROR"
                }
            }
            return json.dumps(error_result, ensure_ascii=False)

# 创建一个全局实例，方便其他地方导入使用
llm_client = LLMClient()