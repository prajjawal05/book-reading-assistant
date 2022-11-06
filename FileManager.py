import os
import json

from SpeechHelper import SpeechHelper

class FileManager(object):
    speech_helper = None
    dir = "/Users/prajjawalsbu/Desktop/books"
    progress_fname = 'progress.json'

    def __init__(self) -> None:
        self.speech_helper = SpeechHelper()

    def _get_file_extension(self, file) -> str:
        print(file.split(".")[-1])
        return file.split(".")[-1]

    def _get_file_name(self, file) -> str:
        print(file.split(".")[0:-1])
        return ".".join(file.split(".")[0:-1])

    def list_books(self):
        def _get_pdfs():
            all_files = os.listdir(self.dir)
            pdfs = list(filter(lambda file_name: self._get_file_extension(file_name) == "pdf", all_files))
            return list(map(self._get_file_name, pdfs))

        file_names = _get_pdfs()

        if not file_names:
            self.speech_helper.speak("You do not have any books")
            return

        print(self.get_progress("hello"))
        self.speech_helper.speak("You have {} books. They are: ".format(len(file_names)))
        for file in file_names:
            self.speech_helper.speak(file)

    def _get_progress_path(self) -> str:
        return "{}/{}".format(self.dir, self.progress_fname)

    def get_progress(self, book_name):
        file_path = self._get_progress_path()
        f = open(file_path, 'r')
        
        all_progress = []
        if f.read():
            all_progress = json.loads(f.read())

        for progress in all_progress:
            if progress["book_name"] == book_name:
                return progress
        
        return None

    def save_progress(self, book_name, page_num, line_num):
        file_path = self._get_progress_path()
        f = open(file_path, 'w')

        all_progress = []
        if f.read():
            all_progress = json.loads(f.read())

        modified_progress = [
            *list(filter(lambda progress: progress["book_name"] == book_name, all_progress)),
            {
                "book_name": book_name,
                "page_num": page_num,
                "line_num": line_num
            }
        ]

        f.write(json.loads(modified_progress))
        return