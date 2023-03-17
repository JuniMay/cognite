import cognite
import unittest
from cognite.extensions.azure.speach import AzureSpeechExtension

class TestAzure(unittest.TestCase):

    def test_azure(self):
        azure = AzureSpeechExtension(speech_key='dfjashfakjshf', region='zh')


if __name__ == '__main__':
    unittest.main()