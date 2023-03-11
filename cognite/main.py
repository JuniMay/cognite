import argparse
import cognite
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", type=str)
    parser.add_argument("--model", type=str, default='gpt-3.5-turbo')
    parser.add_argument("--streaming", type=bool, default=True)

    api_key = parser.parse_args().api

    cognite.llms.openai.set_openai_api_key(api_key)

    model = parser.parse_args().model
    streaming = parser.parse_args().streaming

    def stream_stdout_manager(x):
        sys.stdout.write(x)
        sys.stdout.flush()

    manager = stream_stdout_manager if streaming else print

    # llm = cognite.llms.openai.OpenAiLlm(model=model,
    #                                     streaming=streaming,
    #                                     manager=manager)

    chat_llm = cognite.llms.openai.OpenAiChatLlm(model=model,
                                                 streaming=streaming,
                                                 manager=manager)

    # while True:
    #     prompt = input("Prompt: ")
    #     llm(prompt=prompt)
    #     print()

    system_prompt = "This is a chatbot that can generate a response to a user input. You can ask it to do anything, but it's best at answering questions about the world. Try asking it about the weather, or about the coronavirus. You can also ask it to tell you a joke, or to sing you a song. It's also good at playing games like tic-tac-toe. If you want to play a game, just say 'play a game'. If you want to stop playing a game, just say 'stop'."
    history = []
    while True:
        user_input = input("Human: ")
        completion = chat_llm(system_prompt=system_prompt,
                              user_input=user_input,
                              history=history)

        history.append((user_input, completion))

        if len(history) > 10:
            history.pop(0)

        print()