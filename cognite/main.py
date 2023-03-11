import argparse
import cognite
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", type=str)
    parser.add_argument("--model", type=str, default='text-davinci-001')
    parser.add_argument("--streaming", type=bool, default=True)

    api_key = parser.parse_args().api

    cognite.llms.openai.set_openai_api_key(api_key)

    model = parser.parse_args().model
    streaming = parser.parse_args().streaming

    def stream_stdout_manager(x):
        sys.stdout.write(x)
        sys.stdout.flush()

    manager = stream_stdout_manager if streaming else print

    llm = cognite.llms.openai.OpenAiLlm(model=model,
                                        streaming=streaming,
                                        manager=manager)

    while True:
        prompt = input("Prompt: ")
        llm(prompt=prompt)
        print()