import argparse
import cognite

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", type=str)
    parser.add_argument("--model", type=str, default='text-davinci-003')
    parser.add_argument("--embedding-model",
                        type=str,
                        default='text-embedding-ada-002')
    parser.add_argument("--streaming", type=bool, default=True)

    args = parser.parse_args()

    cognite.llms.openai.set_openai_api_key(args.api_key)
    model = cognite.llms.openai.OpenAiLlm(model=args.model,
                                          streaming=args.streaming,
                                          manager=None)

    chat = cognite.executor.chat.Chat(model)
    while True:
        user = input('User: ')
        reply = chat(user)
        print(f'Cognite: {reply}')