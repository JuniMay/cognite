import cognite
import unittest

class Testchat(unittest.TestCase):

    def test_chat(self):
        chat = cognite.chat.Chat(cognite.llms.openai.OpenAiLlm('text-davinci-003'))
        reply = chat('hello')
        print(reply)
        
if __name__ == '__main__':
    unittest.main()