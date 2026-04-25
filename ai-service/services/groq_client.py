import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
BACKOFF = int(os.getenv("BACKOFF", 2))

PROMPT_FILE = "prompts/security_prompt.txt"


class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env")

        self.client = Groq(api_key=api_key)

    # Load prompt template
    def _load_prompt_template(self) -> str:
        try:
            with open(PROMPT_FILE, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Prompt file not found, using fallback prompt")
            return "Explain the following:\n{input}"

    # Build final prompt
    def _build_prompt(self, user_input: str) -> str:
        template = self._load_prompt_template()
        return template.replace("{input}", user_input)

    # API call
    def _call_api(self, prompt: str):
        return self.client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

    # Main function with retry + backoff
    def generate_response(self, user_input: str) -> dict:
        prompt = self._build_prompt(user_input)

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"Attempt {attempt}")

                res = self._call_api(prompt)
                content = res.choices[0].message.content.strip()

                return {
                    "success": True,
                    "response": content,
                    "model": MODEL
                }

            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {e}")

                if attempt == MAX_RETRIES:
                    return {
                        "success": False,
                        "error": str(e)
                    }

                sleep_time = BACKOFF ** attempt
                time.sleep(sleep_time)