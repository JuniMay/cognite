import cognite

if __name__ == '__main__':
    cognite.llms.openai.set_openai_api_key()
    emb = cognite.llms.openai.OpenAiEmbedding()
    print(len(emb('hello world')))