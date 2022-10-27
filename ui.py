from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from speech import synthesize_from_mic

class MyLayout(BoxLayout):

    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

    def generate_number(self):
        synthesize_from_mic()

class Window(App):
    def build(self):
        return MyLayout()


neural_random  = Window()
neural_random.run()