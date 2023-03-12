import cognite
import unittest


class TestOpenAi(unittest.TestCase):

    def test_embedding(self):
        cognite.llms.openai.set_openai_api_key()
        embedding = cognite.llms.openai.OpenAiEmbedding(
            model='text-embedding-ada-002')
        result = embedding('hello world')

        # print(result)

        self.assertEqual(len(result), 1536, 'embedding length should be 1536')


if __name__ == '__main__':
    unittest.main()