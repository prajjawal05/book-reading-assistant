import re
from config import InstructionType, INSTRUCTIONS_AVAILABLE
from SpeechHelper import SpeechHelper
from FileManager import FileManager
from PdfHandler import PdfReader
from threading import Thread
from time import sleep

class BookManagerInterface:
    last_query = None
    speech_assistant = None
    file_manager = None
    pdf_reader = None
    change_label = lambda _: None

    def stop_book_read():
        pass

    def pause_book_read():
        pass

    def list_all_books():
        pass

    def get_last_reading_book():
        pass

    def continue_last_reading_book():
        pass

    def read_book():
        pass


class BookManager(BookManagerInterface):
    
    def __init__(self, on_label_change) -> None:
        self.speech_assistant = SpeechHelper()
        self.file_manager = FileManager()
        self.pdf_reader = PdfReader(on_label_change)
        self.change_label = on_label_change

    def _read_book(self, bookname: str, continue_reading = False):
        if not bookname:
            self.change_label("Specify a book name")
            self.speech_assistant.speak("I need a book name")
            self.change_label(INSTRUCTIONS_AVAILABLE)
            return

        book_progress = self.file_manager.get_progress(bookname)
        page_num = 0
        line_num = 0

        if book_progress and not book_progress.get("completed", None):
            if continue_reading:
                decision = 'yes'
            else:
                self.change_label("Continue? Yes or No")
                self.speech_assistant.speak("Do you want to continue where you last left?")
                decision = self.speech_assistant.listen()
                print("continue decision - {}".format(decision))

            if decision and re.match(re.compile('yes', re.IGNORECASE), decision):
                page_num = book_progress["page_num"]
                line_num = book_progress["line_num"]

        self.change_label("Reading: {}".format(bookname))
        Thread(target=self.pdf_reader.read, args=(bookname, page_num, line_num)).start()

    def pause_book_read(self):
        # add this when pause is sayed
        self.change_label("Pausing")
        sleep(1)
        self.pdf_reader.stop()

        self.change_label(INSTRUCTIONS_AVAILABLE)

    def stop_book_read(self):
        self.pdf_reader.stop()
        
    def _get_book_name_regex(self, input: str):
        words = input.split()
        if words[0].lower() == "read":
            words = words[1:]
        
        return ".*" + ".*".join(words).lower()

    def list_all_books(self):
        all_books = self.file_manager.get_book_names()
        self.last_query = InstructionType.LIST_BOOKS
        if not all_books:
            self.change_label("No books found")
            self.speech_assistant.speak("You do not have any books")
            self.change_label(INSTRUCTIONS_AVAILABLE)
            return

        self.change_label("You have {} books. They are: ".format(len(all_books)))
        self.speech_assistant.speak("You have {} books. They are: ".format(len(all_books)))
        for book in all_books:
            self.change_label(book)
            self.speech_assistant.speak(book)
        
        self.change_label(INSTRUCTIONS_AVAILABLE)

    def get_last_reading_book(self):
        last_progress = self.file_manager.last_progress()
        if not last_progress:
            self.change_label("No book found")
            self.speech_assistant.speak("No book found")
            self.change_label(INSTRUCTIONS_AVAILABLE)
            return
    
        self.last_query = InstructionType.LAST_READING
        self.change_label("Last reading book: {}".format(last_progress))
        self.speech_assistant.speak(last_progress)
        
        self.change_label(INSTRUCTIONS_AVAILABLE)

    def continue_last_reading_book(self):
        last_progressed_book = self.file_manager.last_progress()
        if not last_progressed_book:
            self.change_label("No book found")
            self.speech_assistant.speak("No book found")
            self.change_label(INSTRUCTIONS_AVAILABLE)
            return

        book_progress = self.file_manager.get_progress(last_progressed_book)
        if book_progress.get("completed", None):
            self.change_label("Restart? Yes or No")
            self.speech_assistant.speak("Book Already completed, do you want to restart")
            decision = self.speech_assistant.listen()
            print("restart decision - {}".format(decision))
            if decision and not re.match(re.compile('yes', re.IGNORECASE), decision):
                self.change_label(INSTRUCTIONS_AVAILABLE)
                return
                
        self._read_book(last_progressed_book, True)

    def _read_ambiguos_book(self):
        book_name = None
        if self.last_query == InstructionType.LAST_READING:
            self.change_label("Continuing the last reading book")
            book_name = self.file_manager.last_progress()
        if self.last_query == InstructionType.LIST_BOOKS:
            self.change_label("You have only one book")
            all_books = self.file_manager.get_book_names()
            if len(all_books) == 1:
                book_name = all_books.pop()

        self._read_book(book_name)

    def read_book(self, input: str):
        input = input[:-1]

        if re.match(re.compile("read it", re.IGNORECASE), input):
            self._read_ambiguos_book()
            return

        self.last_query = InstructionType.READ_BOOK
        all_books = self.file_manager.get_book_names()

        matching_books = list(filter(lambda book: re.match(re.compile(self._get_book_name_regex(input), re.IGNORECASE), book.lower()), all_books))
        
        if not matching_books:
            self.change_label("Book not found")
            self.speech_assistant.speak("book not found")
            self.change_label(INSTRUCTIONS_AVAILABLE)
            return

        if len(matching_books) > 1:
            self.change_label("Multiple matches Found.")
            self.speech_assistant.speak("be more specific. There are {} books with similar name".format(len(matching_books)))
            self.change_label(INSTRUCTIONS_AVAILABLE)
            return

        book_name = matching_books.pop()
        self._read_book(book_name)
        

        