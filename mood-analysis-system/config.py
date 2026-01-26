import os


class Config:
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    MODELS = {
        'openai': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
        'gemini': os.getenv('GEMINI_MODEL', 'gemini-1.5-flash'),
        'anthropic': os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022'),
        'ollama': os.getenv('OLLAMA_MODEL', 'llama3.1')
    }
    
    LLM_MODEL = MODELS.get(LLM_PROVIDER)
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        provider = cls.LLM_PROVIDER.lower()
        
        # if provider == 'openai' and not cls.OPENAI_API_KEY:
        #     raise ValueError("OPENAI_API_KEY not set in .env")
        # elif provider == 'anthropic' and not cls.ANTHROPIC_API_KEY:
        #     raise ValueError("ANTHROPIC_API_KEY not set in .env")
        if provider == 'gemini' and not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in .env")
        
        print(f"✅ Configuration valid - Using {provider.upper()}")