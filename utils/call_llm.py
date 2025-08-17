from google import genai
from openai import OpenAI
import os

def call_llm(prompt: str) -> str:
    """
    调用 LLM API，支持 Gemini 和 OpenAI
    
    Args:
        prompt: 输入提示
        provider: 指定使用的提供商 ('gemini', 'openai', None 表示自动选择)
    
    Returns:
        模型响应文本
    """

    provider = os.getenv("PROVIDER", "openai")
    if provider == "gemini":
        return _call_gemini(prompt)
    elif provider == "openai":
        return _call_openai(prompt)
    else:
        raise ValueError(f"不支持的提供商: {provider}")

def _call_gemini(prompt: str) -> str:
    """调用 Gemini API"""
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY", ""),
    )
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    response = client.models.generate_content(model=model, contents=[prompt])
    return response.text

def _call_openai(prompt: str) -> str:
    """调用 OpenAI API"""
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        base_url=os.getenv("OPENAI_API_URL", ""),

    )
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    test_prompt = "Hello, how are you?"

    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt)
    print(f"Response: {response1}")
