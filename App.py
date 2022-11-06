from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from threading import Thread
from SpeechAssistant import SpeechAssistant
import os

class Handler(object):
    assistant = None

    def __init__(self, handle_assistant_label_change):
        self.assistant = SpeechAssistant(handle_assistant_label_change)

    def _start_assistant(self):
        Thread(target=self.assistant.run_assistant).start()

    def toggle_speech(self):
        if not self.assistant.is_assistant_running():
            self._start_assistant()
            action_label = "Speak something. Press to stop"
        else:
            self.assistant.stop_assistant()
            action_label = "Press to initiate assistant"

        return action_label


class MyLayout(BoxLayout):
    action_label = StringProperty()
    info_label = StringProperty()
    handler = None

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.info_label = "Welcome!"
        self.action_label = "Press to initiate assistant"
        self.handler = Handler(self.handle_assistant_label_change)

    def handle_assistant_label_change(self, label):
        self.info_label = label

    def toggle_speech(self):
        self.action_label = self.handler.toggle_speech()
        

class Window(App):
    def build(self):
        return MyLayout()


neural_random = Window()
neural_random.run()