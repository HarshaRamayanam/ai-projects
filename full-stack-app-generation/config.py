from dotenv import load_dotenv

import os

load_dotenv()

REQUIREMENTS_MODEL = os.getenv("REQUIREMENTS_MODEL", "qwen2.5-coder:7b")
CODER_MODEL = os.getenv("CODER_MODEL", "qwen2.5-coder:14b")
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "deepseek-coder:6.7b")
FIXER_MODEL = os.getenv("FIXER_MODEL", "qwen2.5-coder:7b")
DOCUMENTATION_MODEL = os.getenv("DOCUMENTATION_MODEL", "llama3.2:3b")