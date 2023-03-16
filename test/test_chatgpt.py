import cognite
import unittest

class Testchat(unittest.TestCase):

    def test_chat(self):
        chat = cognite.executor.chatgpt.ChatGPT(cognite.llms.openai.OpenAiChatLlm('gpt-3.5-turbo'))
        reply = chat('Hi, introduce yourself!')
        print(reply)
        
if __name__ == '__main__':
    unittest.main()