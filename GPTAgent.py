from openai import OpenAI
from pathlib import Path


class GPTAgent(object):
    def __init__(self, key: str | Path, conditioning_message: str = 'You are an helpful assistant',
                 model: str = 'gpt-3.5-turbo'):
        """
        Initializes the agent.
        :param key: The key for the API. Can be provided either as a raw string or as a path to the file containing it.
        :param conditioning_message: String containing the message that conditions the model behavior.
        :param model: String that specifies which model to use from the ones proposed by the API.
        """
        self.model = model
        key_path = Path(key)
        # Retrieves key either by storing it in a variable or retrieving it from local file.
        if not key_path.is_file():
            loaded_key = key
        else:
            with open(key_path, 'r') as f:
                loaded_key = f.read()
                f.close()
        self.client = OpenAI(api_key=loaded_key)
        # Messages history
        self.messages = [
            {'role': 'system', 'content': conditioning_message}
        ]

    def send(self, message: str) -> str:
        """
        Sends message to the client and returns the response.
        :param message: string containing the message
        :return: string with the answer
        """
        self.messages.append({'role': 'user', 'content': message})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
        )
        reply = response.choices[0].message.content
        # Append also GPT reply to history.
        self.messages.append({'role': 'assistant', 'content': reply})
        return reply
