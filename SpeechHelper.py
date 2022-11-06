import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig


speech_config = speechsdk.SpeechConfig(subscription="4a78b0929e514090a534d12ae5b8a1d7", region="eastus")
speech_recogniser = speechsdk.SpeechRecognizer(speech_config=speech_config)

audio_config = AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

class SpeechHelper(object):
    def listen(self):
        result = speech_recogniser.recognize_once_async()
        result = result.get()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text

        return None

    def speak(self, text): 
        synthesizer.speak_text(text)
