import azure.cognitiveservices.speech as speechsdk

class AzureSpeechExtension:
    def __init__(self, speech_key, speech_region) -> None:
        self.speech_key = speech_key
        self.speech_region = speech_region
        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.speech_region)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
        
    def from_mic(self):
        print("Speak into your microphone.")
        result = self.speech_recognizer.recognize_once_async().get()
        return result.text
