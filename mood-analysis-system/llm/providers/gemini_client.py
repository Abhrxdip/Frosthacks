import os
import importlib

# Optional real integration (install google-generative-ai / google-generative-aiplatform)
try:
    genai = importlib.import_module("google.generativeai")
    HAS_GENAI = True
except Exception:
    genai = None
    HAS_GENAI = False


class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in .env")
        self.model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        if HAS_GENAI:
            genai.configure(api_key=self.api_key)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        If google.generativeai is installed it will call Gemini.
        Otherwise returns a safe fallback string so the app continues.
        """
        if HAS_GENAI:
            try:
                # Add safety settings to reduce blocking
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
                
                resp = genai.GenerativeModel(self.model).generate_content(
                    f"{system_prompt}\n\n{user_prompt}",
                    safety_settings=safety_settings
                )
                
                # Try to extract text from response
                text_result = None
                
                # Method 1: Use .text accessor if available
                try:
                    if hasattr(resp, 'text') and resp.text:
                        text_result = resp.text
                except Exception:
                    pass
                
                # Method 2: Extract from candidates
                if not text_result and hasattr(resp, 'candidates') and resp.candidates:
                    candidate = resp.candidates[0]
                    if hasattr(candidate, 'content') and candidate.content.parts:
                        text_parts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                        if text_parts:
                            text_result = " ".join(text_parts)
                
                # Return result or fallback
                if text_result:
                    return text_result
                else:
                    return "[Gemini] No valid response. API may be rate-limited or safety filters blocking content. Try switching to OpenAI/Anthropic provider."
                    
            except Exception as e:
                return f"[Gemini error] {str(e)}"
        
        # Fallback: simple canned questions / message
        return ("[Gemini stub] Gemini client not installed/configured. "
                "Install the Google GenAI SDK and set GEMINI_API_KEY in .env, "
                "or switch LLM_PROVIDER to openai/anthropic.")