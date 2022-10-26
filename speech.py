import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig

speech_config = speechsdk.SpeechConfig(subscription="4a78b0929e514090a534d12ae5b8a1d7", region="eastus")
speech_recogniser = speechsdk.SpeechRecognizer(speech_config=speech_config)

audio_config = AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)


def synthesize_to_speaker(text):
    synthesizer.speak_text(text)

def synthesize_from_mic():
    result = speech_recogniser.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        synthesize_to_speaker(result.text)

if __name__ == "__main__":
    synthesize_from_mic()
    