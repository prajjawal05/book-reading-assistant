import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig

import re
from config import INSTRUCTIONS, InstructionType, INSTRUCTIONS_AVAILABLE

speech_config = speechsdk.SpeechConfig(subscription="4a78b0929e514090a534d12ae5b8a1d7", region="eastus")
speech_recogniser = speechsdk.SpeechRecognizer(speech_config=speech_config)

audio_config = AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


def synthesize_to_speaker(text):
    synthesizer.speak_text(text)

class SpeechAssistant(object):
    is_running = False

    def __init__(self, on_label_change):
        self.is_running = False
        self.change_label = on_label_change

    def is_assistant_running(self):
        return self.is_running

    def act_on_input(self, input):
        for inst in INSTRUCTIONS:
            matches = list(filter(
                lambda message: 
                    re.match(re.compile(message, re.IGNORECASE), input), inst["inputMessages"]))
            if matches:
                print(inst["type"])
                break

    def run_assistant(self):
        self.is_running = True
        self.change_label(INSTRUCTIONS_AVAILABLE)
        while True:
            result = speech_recogniser.recognize_once_async()
            if not self.is_running:
                break

            result = result.get()
            
            print("Recognising speech")
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print(result.text)
                self.act_on_input(result.text)

    def stop_assistant(self):
        self.change_label("Please enable assistant.")
        self.is_running = False
    

if __name__ == "__main__":
    s = SpeechAssistant(1)
    s.act_on_input("what books do I have")
    