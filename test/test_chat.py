import cognite
import unittest

class Testchat(unittest.TestCase):

    def test_chat(self):
        chat = cognite.executor.chat.Chat(cognite.llms.openai.OpenAiLlm('text-davinci-003'))
        reply = chat().send('hello')
        print(reply)
        
if __name__ == '__main__':
    chat = cognite.executor.chat.Chat(cognite.llms.openai.OpenAiLlm('text-davinci-003'))
    reply = chat('hello').send(None)
    print(reply)