import openai
from .types import ChatGPTConfig
from .utils import logger


class ChatGPT:
    def __init__(self, config: ChatGPTConfig):
        openai.api_key = config.api_key
        self.model = config.model or "gpt-3.5-turbo"
        self.temperature = config.temperature or 1
        self.top_p = config.top_p or 1
        self.language = config.language or "Chinese"

    def generate_prompt(self, patch: str) -> str:
        answer_language = f"Answer me in {self.language},"

        return f"Below is a git code patch diff, please help me do a brief code review,${answer_language} if any bug risk and improvement suggestion are welcome\n{patch}"

    async def code_review(self, patch: str):
        if not patch:
            logger.error("patch is empty")
            return ""

        prompt = self.generate_prompt(patch)

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                temperature=self.temperature,
                top_p=self.top_p,
                presence_penalty=1,
                stream=False,
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )
            return response.choices[0].message.content.strip()
        except Exception as error:
            logger.error(error)
            return "An error occurred during the code review."
