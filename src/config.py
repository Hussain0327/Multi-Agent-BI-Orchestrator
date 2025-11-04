"""Configuration management for the Business Intelligence Orchestrator."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for the application."""

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-nano")

    # LangSmith Configuration
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true"
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "business-intelligence-orchestrator")
    LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

    # Application Configuration
    MAX_MEMORY_MESSAGES = 10

    # GPT-5 Specific Configuration
    REASONING_EFFORT = "medium"  # minimal, low, medium, high
    TEXT_VERBOSITY = "medium"   # low, medium, high
    MAX_OUTPUT_TOKENS = 2000

    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # LangSmith is optional, just warn if not configured
        if not cls.LANGCHAIN_API_KEY and cls.LANGCHAIN_TRACING_V2:
            print("Warning: LANGCHAIN_TRACING_V2 is enabled but LANGCHAIN_API_KEY is not set")
            print("Get your API key from: https://smith.langchain.com/settings")
            cls.LANGCHAIN_TRACING_V2 = False

    @classmethod
    def is_gpt5(cls) -> bool:
        """Check if using GPT-5 model."""
        return "gpt-5" in cls.OPENAI_MODEL.lower()


# Validate configuration on import
Config.validate()
