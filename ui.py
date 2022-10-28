from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from threading import Thread
from speech import SpeechAssistant
import os

class Handler(object):
    assistant = None

    def __init__(self):
        self.assistant = SpeechAssistant()

    def generate_number(self):
        if not self.assistant.is_assistant_running():
            Thread(target=self.assistant.run_assistant).start()
            self.action_label = "Speak something. Press to stop"
        else:
            self.assistant.stop_assistant()
            self.action_label = "Press to initiate assistant"


class MyLayout(BoxLayout):
    action_label = StringProperty()
    info_label = StringProperty()
    handler = None

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.info_label = "Welcome!"
        self.action_label = "Press to initiate assistant"
        self.handler = Handler()

    def generate_number(self):
        self.handler.generate_number()
        

class Window(App):
    def build(self):
        return MyLayout()


neural_random  = Window()
neural_random.run()