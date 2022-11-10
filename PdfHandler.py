from PyPDF2 import PdfFileReader

from SpeechHelper import SpeechHelper
from FileManager import FileManager


class PdfReader(object):
    speech_helper = None
    file_manager = None
    page_num = 0

    def __init__(self) -> None:
        self.speech_helper = SpeechHelper()
        self.file_manager = FileManager()

    def read(self, bookname, init_page_num = 0):
        book_location = self.file_manager.get_book_path(bookname)
        pdffileobj=open('{}.pdf'.format(book_location),'rb')
        pdfreader = PdfFileReader(pdffileobj)
        self.page_num = init_page_num

        while self.page_num < pdfreader.numPages:
            page_obj = pdfreader.getPage(pageNumber=self.page_num)
            page_content = page_obj.extractText()
            page_content = " ".join(page_content.splitlines())
            self.speech_helper.speak(page_content)
            self.page_num = self.page_num + 1
            break

    def stop(self):
        # stop_assistant
        # return page_num
        pass
