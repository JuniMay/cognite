import argparse
import openai


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", type=str, required=True)

    openai.api_key = parser.parse_args().api
    model_engine = "text-davinci-003"

    while True:
        prompt = input("prompt: ")
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=512,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text
        print(f"response: {response}")