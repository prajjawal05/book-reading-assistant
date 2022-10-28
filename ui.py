from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from threading import Thread
from speech import speech_assistant

t2 = None

class MyLayout(BoxLayout):
    action_label = StringProperty()
    info_label = StringProperty()

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
        self.info_label = "Welcome!"
        self.action_label = "Press to initiate assistant"

    def generate_number(self):
        t2.start()
        self.action_label = "Speak something"
        

class Window(App):
    def build(self):
        return MyLayout()


neural_random  = Window()
t2 = Thread(target=speech_assistant)
neural_random.run()
t2.join()