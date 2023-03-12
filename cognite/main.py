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

    prompt_template = cognite.PromptTemplate(
        """You are a artificial intelligence named Cognite. Your job is helping users with their problem.
        
        You performs like a chatbot. With a given user input, you will generate a response according to the current input and the conversation history. You need to notice the information given by the user.
        
        Now, the conversation history is as following:
        
        {history}
        
        User: {user_input}
        Cognite: 
        """,
        variables=['user_input', 'history'])

    llm_chain = cognite.LlmChain(model=model,
                                 prompt_template=prompt_template,
                                 streaming=args.streaming,
                                 generators=[])

    repl = cognite.Repl(llm_chain)

    repl.run()