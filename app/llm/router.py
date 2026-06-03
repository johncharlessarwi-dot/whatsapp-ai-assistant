from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from flask import current_app
import logging

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self):
        self.config = current_app.config

    def get_llm(self):
        """
        Fallback logic: Groq -> Gemini -> OpenAI -> xAI -> Claude
        """
        # 1. Groq (Llama 3) - Fast & Cheap
        if self.config.get('GROQ_API_KEY'):
            try:
                logger.info("Initializing Groq LLM")
                return ChatGroq(
                    temperature=0,
                    model_name="llama-3.3-70b-versatile",
                    groq_api_key=self.config['GROQ_API_KEY']
                )
            except Exception as e:
                logger.warning(f"Groq initialization failed: {e}")

        # 2. Gemini
        if self.config.get('GOOGLE_API_KEY'):
            try:
                logger.info("Falling back to Gemini")
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=self.config['GOOGLE_API_KEY']
                )
            except Exception as e:
                logger.warning(f"Gemini initialization failed: {e}")

        # 3. OpenAI
        if self.config.get('OPENAI_API_KEY'):
            try:
                logger.info("Falling back to OpenAI")
                return ChatOpenAI(
                    model_name="gpt-4o-mini",
                    openai_api_key=self.config['OPENAI_API_KEY']
                )
            except Exception as e:
                logger.warning(f"OpenAI initialization failed: {e}")

        # 4. xAI (Grok) - Placeholder as LangChain support varies
        # if self.config.get('XAI_API_KEY'):
        #     pass

        # 5. Anthropic Claude 3.5 Sonnet
        if self.config.get('ANTHROPIC_API_KEY'):
            try:
                logger.info("Falling back to Claude")
                return ChatAnthropic(
                    model_name="claude-3-5-sonnet-20240620",
                    anthropic_api_key=self.config['ANTHROPIC_API_KEY']
                )
            except Exception as e:
                logger.error(f"Claude initialization failed: {e}")

        raise ValueError("No LLM providers available or configured correctly.")
