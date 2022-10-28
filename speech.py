import asyncio
import os
from time import sleep
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig

speech_config = speechsdk.SpeechConfig(subscription="4a78b0929e514090a534d12ae5b8a1d7", region="eastus")
speech_recogniser = speechsdk.SpeechRecognizer(speech_config=speech_config)

audio_config = AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


def synthesize_to_speaker(text):
    synthesizer.speak_text(text)

class SpeechAssistant(object):
    is_running = False

    def __init__(self):
        self.is_running = False

    def is_assistant_running(self):
        return self.is_running

    def run_assistant(self):
        self.is_running = True
        while True:
            print("Waiting for speech")
            result = speech_recogniser.recognize_once_async()
            if not self.is_running:
                break
            result = result.get()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print(result.text)
                synthesize_to_speaker(result.text)

    def stop_assistant(self):
        self.is_running = False
    

def start_assistant():
    pass

if __name__ == "__main__":
    start_assistant()
    