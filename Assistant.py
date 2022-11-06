import re
from config import INSTRUCTIONS, InstructionType, INSTRUCTIONS_AVAILABLE

from FileManager import FileManager
from SpeechHelper import SpeechHelper

class Assistant(object):
    _is_running = False
    speech_helper = None
    file_manager = None

    def _get_instruction_handler(self, inst_type):
        handlers = {
            InstructionType.LIST_BOOKS:  lambda _: self.file_manager.list_books()
        }

        return handlers.get(inst_type)

    def __init__(self, on_label_change):
        self._is_running = False
        self.change_label = on_label_change
        self.speech_helper = SpeechHelper()
        self.file_manager = FileManager()

    def is_running(self):
        return self._is_running

    def act(self, input):
        print(input)
        for inst in INSTRUCTIONS:
            matches = list(filter(
                lambda message: 
                    re.match(re.compile(message, re.IGNORECASE), input), inst["inputMessages"]))
            if matches:
                handler = self._get_instruction_handler(inst["type"])
                handler(input)
                break

    def run(self):
        self._is_running = True
        self.change_label(INSTRUCTIONS_AVAILABLE)
        while True:
            result = self.speech_helper.listen()
            if not self._is_running:
                break

            if not result:
                continue

            self.act(result)

    def stop(self):
        self.change_label("Please enable assistant.")
        self._is_running = False
    

if __name__ == "__main__":
    s = Assistant(1)
    s.act("what books do I have")
    