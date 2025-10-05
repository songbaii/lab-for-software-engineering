import os
from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.api_key = 'sk-5NRAokzo8lMTP1yOnB2qZR9dOIHEhx95FurHyHChydAtQQfV'
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://ai.nengyongai.cn/v1"
        )

    def generate_content(self, prompt, model="deepseek-chat", max_tokens=500):
        """
        调用LLM API生成内容的核心函数
        :param prompt: 构造好的提示词
        :param model: 模型名称，默认为deepseek-chat
        :param max_tokens: 生成内容的最大长度
        :return: 模型生成的文本内容
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一个专业的影评人和内容摘要专家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7 # 控制创造性，0.0-1.0
            )
            # 从响应中提取生成的文本内容
            generated_text = response.choices[0].message.content
            return generated_text.strip()
        except Exception as e:
            # 非常重要的错误处理，便于调试
            print(f"调用LLM API时出错: {e}")
            return f"生成内容时出错: {e}"

# 创建一个全局实例，方便其他地方导入使用
llm_client = LLMClient()