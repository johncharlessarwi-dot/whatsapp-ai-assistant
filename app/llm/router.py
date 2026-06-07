from flask import current_app
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import logging

logger = logging.getLogger(__name__)


class LLMRouter:

    _cached_llm = None

    def __init__(self):
        self.config = current_app.config

    def get_llm(self):

        if LLMRouter._cached_llm:
            return LLMRouter._cached_llm

        providers = [

            (
                "Groq",
                "GROQ_API_KEY",
                lambda: ChatGroq(
                    model_name="llama-3.3-70b-versatile",
                    temperature=0.3,
                    groq_api_key=self.config["GROQ_API_KEY"]
                )
            ),

            (
                "Gemini",
                "GOOGLE_API_KEY",
                lambda: ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash",
                    google_api_key=self.config["GOOGLE_API_KEY"],
                    temperature=0.3
                )
            ),

            (
                "OpenAI",
                "OPENAI_API_KEY",
                lambda: ChatOpenAI(
                    model="gpt-4o-mini",
                    openai_api_key=self.config["OPENAI_API_KEY"],
                    temperature=0.3
                )
            ),

            (
                "Claude",
                "ANTHROPIC_API_KEY",
                lambda: ChatAnthropic(
                    model="claude-sonnet-4-20250514",
                    anthropic_api_key=self.config["ANTHROPIC_API_KEY"],
                    temperature=0.3
                )
            )

        ]

        for provider_name, key_name, provider_factory in providers:

            api_key = self.config.get(key_name)

            if not api_key:
                continue

            try:

                logger.info(
                    f"Trying provider: {provider_name}"
                )

                llm = provider_factory()

                LLMRouter._cached_llm = llm

                logger.info(
                    f"Connected to {provider_name}"
                )

                return llm

            except Exception as e:

                logger.warning(
                    f"{provider_name} failed: {str(e)}"
                )

        raise RuntimeError(
            "No AI provider available."
        )
