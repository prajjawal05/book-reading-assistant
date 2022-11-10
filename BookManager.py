import re
from SpeechHelper import SpeechHelper
from FileManager import FileManager
from PdfHandler import PdfReader

class BookManager(object):
    book_last_queried = None
    speech_assistant = None
    file_manager = None
    pdf_reader = None

    def __init__(self) -> None:
        self.speech_assistant = SpeechHelper()
        self.file_manager = FileManager()
        self.pdf_reader = PdfReader()

    def _read_book(self, bookname: str):
        if not bookname:
            self.speech_assistant.speak("I need a book name")

        book_progress = self.file_manager.get_progress(bookname)
        
        if book_progress:
            self.speech_assistant.speak("Do you want to continue where you last left?")

        self.pdf_reader.read(bookname)

        
    def _get_book_name_regex(self, input: str):
        words = input.split()
        if words[0] == "read":
            words = words[1:]
        
        return ".*" + ".*".join(words).lower() + ".*"

    def read_book(self, input: str):
        if re.match(re.compile("read it", re.IGNORECASE), input):
            self._read_book(self.book_last_queried)

        all_books = self.file_manager.get_book_names()

        matching_books = list(filter(lambda book: re.match(re.compile(self._get_book_name_regex(input), re.IGNORECASE), book.lower()), all_books))
        
        if not matching_books:
            self.speech_assistant.speak("book not found")

        if len(matching_books) > 1:
            self.speech_assistant.speak("be more specific. There are {} books with similar name".format(len(matching_books)))

        book_name = matching_books.pop()
        self._read_book(book_name)
        

        