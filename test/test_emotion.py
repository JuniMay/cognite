import cognite
import unittest

class Testchat(unittest.TestCase):

    def test_chat(self):
        emotion = cognite.executor.emotion.Emotion(cognite.llms.openai.OpenAiLlm('text-davinci-003'))
        reply = emotion(input('Input: '))
        print(reply)
        
if __name__ == '__main__':
    unittest.main()