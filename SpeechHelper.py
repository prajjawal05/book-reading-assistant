import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig

# Note: The subscription code won't work. Have fun checking it out in the VCS anyways.
speech_config = speechsdk.SpeechConfig(subscription="x", region="eastus")
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
