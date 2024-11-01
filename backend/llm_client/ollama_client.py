from backend.llm_client.llm_client import LLMClient
import ollama


class OllamaClient(LLMClient):

    def __init__(self, model: str = "llama3"):
        super().__init__()
        self.model = model

    def prompt(self, message: str) -> str:
        return ollama.generate(model=self.model, prompt=message)
