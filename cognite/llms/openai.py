import os
import openai
from typing import Optional, Callable, List, Tuple


def set_openai_api_key(api_key: Optional[str] = None) -> None:
    """Set OpenAI API key
    
    Args:
        api_key (Optional[str]): OpenAI API key. API key will be retrieved 
            from environment variable OPENAI_API_KEY if not provided.
        
    """

    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")

    openai.api_key = api_key


class OpenAiLlm:

    def __init__(self,
                 model: str,
                 streaming: bool = False,
                 manager: Optional[Callable[[str], None]] = None) -> None:
        """OpenAI Completion API wrapper
        """

        self.model = model
        self.streaming = streaming
        self.manager = manager

    def __call__(self,
                 prompt: str,
                 temperature: float = 0.5,
                 top_p: int = 1,
                 max_tokens: int = 512,
                 stop: Optional[str | list] = None) -> str:

        completion = ""

        if self.streaming:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=True,
                stop=stop,
            )
            for chunk in response:
                if self.manager is not None:
                    self.manager(chunk['choices'][0]['text'])

                completion += chunk['choices'][0]['text']

        else:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=False,
                stop=stop,
            )
            if self.manager is not None:
                self.manager(response['choices'][0]['text'])

            completion = response['choices'][0]['text']

        return completion


class OpenAiChatLlm:

    def __init__(self,
                 model: str,
                 streaming: bool = False,
                 manager: Optional[Callable[[str], None]] = None) -> None:
        self.model = model
        self.streaming = streaming
        self.manager = manager

    def __call__(self,
                 system_prompt: str,
                 user_input: str,
                 history: Optional[List[Tuple[str, str]]] = None,
                 temperature: float = 0.5,
                 top_p: int = 1,
                 max_tokens: int = 512,
                 stop: Optional[str | list] = None) -> str:

        messages = [{"role": "system", "content": system_prompt}]

        if history is not None:
            for user, assistant in history:
                messages.append({"role": "user", "content": user})
                messages.append({"role": "assistant", "content": assistant})

        messages.append({"role": "user", "content": user_input})

        chat_completion = ""

        if self.streaming:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=True,
                stop=stop,
            )
            for chunk in response:
                if chunk['choices'][0]['delta'].get('content') is None:
                    continue

                if self.manager is not None:
                    self.manager(chunk['choices'][0]['delta']['content'])

                chat_completion += chunk['choices'][0]['delta']['content']

        else:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=False,
                stop=stop,
            )
            if self.manager is not None:
                self.manager(response['choices'][0]['message']['content'])

            chat_completion = response['choices'][0]['message']['content']

        return chat_completion

class OpenAiEmbedding:

    def __init__(self, model: str = 'text-embedding-ada-002') -> None:
        """OpenAI Embedding API wrapper
        Args:
            model (str): model used for embedding.
        """
        self.model = model

    def __call__(self, text: str) -> List[float]:
        """returns embedding for text
        Args:
            text (str): text to be embedded
        Returns:
            List[float]: embedding vector in 1536 dimensions
        """
        response = openai.Embedding.create(
            model=self.model,
            input=text,
        )
        return response['data'][0]['embedding']
    