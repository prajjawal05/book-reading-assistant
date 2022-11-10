import re
from config import InstructionType
from SpeechHelper import SpeechHelper
from FileManager import FileManager
from PdfHandler import PdfReader

class BookManager(object):
    last_query = None
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
            return

        book_progress = self.file_manager.get_progress(bookname)
        page_num = 0

        if book_progress:
            self.speech_assistant.speak("Do you want to continue where you last left?")
            decision = self.speech_assistant.listen()
            if re.match(re.compile('yes', re.IGNORECASE), decision):
                page_num = book_progress["page_num"]

        self.pdf_reader.read(bookname, init_page_num=page_num)

        
    def _get_book_name_regex(self, input: str):
        words = input.split()
        if words[0] == "read":
            words = words[1:]
        
        return ".*" + ".*".join(words).lower() + ".*"

    def list_all_books(self):
        all_books = self.file_manager.get_book_names()
        self.last_query = InstructionType.LIST_BOOKS
        if not all_books:
            self.speech_assistant.speak("You do not have any books")
            return

        self.speech_assistant.speak("You have {} books. They are: ".format(len(all_books)))
        for book in all_books:
            self.speech_assistant.speak(book)

    def get_last_reading_book(self):
        last_progress = self.file_manager.last_progress()
        self.last_query = InstructionType.LAST_READING
        self.speech_assistant.speak(last_progress)

    def _read_ambiguos_book(self):
        book_name = None
        if self.last_query == InstructionType.LAST_READING:
            book_name = self.file_manager.last_progress()
        if self.last_query == InstructionType.LIST_BOOKS:
            all_books = self.file_manager.get_book_names()
            if len(all_books) == 1:
                book_name = all_books.pop()

        self._read_book(book_name)

    def read_book(self, input: str):
        if re.match(re.compile("read it", re.IGNORECASE), input):
            self._read_ambiguos_book()

        self.last_query = InstructionType.READ_BOOK
        all_books = self.file_manager.get_book_names()

        matching_books = list(filter(lambda book: re.match(re.compile(self._get_book_name_regex(input), re.IGNORECASE), book.lower()), all_books))
        
        if not matching_books:
            self.speech_assistant.speak("book not found")

        if len(matching_books) > 1:
            self.speech_assistant.speak("be more specific. There are {} books with similar name".format(len(matching_books)))

        book_name = matching_books.pop()
        self._read_book(book_name)
        

        