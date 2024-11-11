import os
import openai
from openai import OpenAI
from dotenv import load_dotenv


class LLMManager:
    _instance = None
    _client = None
    _cs_categories = ("DATA_STRUCTURE", "ALGORITHM", "COMPUTER_ARCHITECTURE", "NETWORK", "OPERATING_SYSTEM",
                     "DATABASE")
    _language_categories = ("JAVA", "JAVASCRIPT", "PYTHON")
    _tool_categories = ("SPRING", "REACT", "PYTORCH", "DOCKER")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if LLMManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LLMManager._instance = self

    def load_model(self):
        if self._client is None:
            try:
                load_dotenv()

                openai.api_key = os.getenv("OPENAI_API_KEY")
                self._client = OpenAI()

            except Exception as e:
                print(f"Error loading model: {str(e)}")
                raise

