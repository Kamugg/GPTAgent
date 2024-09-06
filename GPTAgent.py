from openai import OpenAI
from pathlib import Path


class GPTAgent(object):
    def __init__(self, key: str | Path, conditioning_message: str, model: str = 'gpt-3.5-turbo'):
        self.model = model
        key_path = Path(key)
        if not key_path.is_file():
            loaded_key = key
        else:
            with open(key_path, 'r') as f:
                loaded_key = f.read()
                f.close()
        self.client = OpenAI(api_key=loaded_key)
        self.messages = [
            {'role': 'system', 'content': conditioning_message}
        ]

    def send(self, message: str) -> str:
        self.messages.append({'role': 'user', 'content': message})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        reply = response.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply
