import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in .env")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

def get_llm_client():
    """Get LLM client based on configured provider."""
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    # if provider == "openai":
    #     from llm.providers.openai_client import OpenAIClient
    #     return OpenAIClient()
    # elif provider == "anthropic":
    #     from llm.providers.anthropic_client import AnthropicClient
    #     return AnthropicClient()
    if provider == "gemini":
        from llm.providers.gemini_client import GeminiClient
        return GeminiClient()
    # elif provider == "ollama":
    #     from llm.providers.ollama_client import OllamaClient
    #     return OllamaClient()
    # else:
    #     raise ValueError(f"Unknown LLM provider: {provider}")

# Don't call this at module import time!
# client = get_llm_client()

from utils.session_manager import SessionManager

class MoodAnalyzer:
    def __init__(self):
        self.session_manager = SessionManager()
    
    def analyze_mood(self, text: str) -> str:
        # Placeholder for mood analysis logic
        # This should be replaced with actual implementation
        return "happy" if "good" in text else "neutral"