from PyPDF2 import PdfFileReader

from SpeechHelper import SpeechHelper
from FileManager import FileManager


class PdfReader(object):
    speech_helper = None
    file_manager = None
    reading = False

    def __init__(self) -> None:
        self.speech_helper = SpeechHelper()
        self.file_manager = FileManager()
        self.reading = False

    def read(self, bookname, init_page_num = 0, init_line_num = 0):
        self.reading = True
        book_location = self.file_manager.get_book_path(bookname)
        pdffileobj=open('{}.pdf'.format(book_location),'rb')
        pdfreader = PdfFileReader(pdffileobj)
        page_num = init_page_num
        start_line = init_line_num

        while page_num < pdfreader.numPages:
            page_obj = pdfreader.getPage(pageNumber=page_num)
            page_content = page_obj.extractText()
            page_content = (" ".join(page_content.splitlines())).split(".")
            
            for line_num, line in enumerate(page_content):
                if line_num < start_line:
                    continue
                
                if not self.reading:
                    self.file_manager.save_progress(bookname, page_num, line_num)
                    return

                self.speech_helper.speak(line)

            page_num = page_num + 1
            start_line = 0

            if not self.reading:
                self.file_manager.save_progress(bookname, page_num, 0)
                return

        self.reading = False

    def stop(self):
        self.reading = False
        pass
