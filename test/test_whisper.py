import cognite
import unittest
from cognite.extensions.whisper.whisper import WhisperExtention

class TestWhisper(unittest.TestCase):
    def test_whisper(self):
        whisper = WhisperExtention()
        text = whisper.transcribe_file('test/test.m4a')
        print(text)

if __name__ == '__main__':
    unittest.main()