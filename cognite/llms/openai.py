import os
import openai
from typing import Optional, Callable


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
                 model: str = '',
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
                 stop: Optional[str | list] = None) -> None:
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

        else:
            response = openai.Completion.create(
                model=self.model,
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stop=stop,
            )
            if self.manager is not None:
                self.manager(response['choices'][0]['text'])