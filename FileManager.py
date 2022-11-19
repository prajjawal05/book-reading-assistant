import os
import json

class FileManager(object):
    dir = "/Users/prajjawalsbu/Desktop/books"
    progress_fname = 'progress.json'

    def __init__(self) -> None:
        pass

    def _get_file_extension(self, file) -> str:
        print(file.split(".")[-1])
        return file.split(".")[-1]

    def _get_file_name(self, file) -> str:
        print(file.split(".")[0:-1])
        return ".".join(file.split(".")[0:-1])

    def get_book_path(self, book_name) -> str:
        return "{}/{}".format(self.dir, book_name)

    def get_book_names(self) -> list[str]:
            all_files = os.listdir(self.dir)
            pdfs = list(filter(lambda file_name: self._get_file_extension(file_name) == "pdf", all_files))
            return list(map(self._get_file_name, pdfs))        

    def _get_progress_path(self) -> str:
        return "{}/{}".format(self.dir, self.progress_fname)

    def get_progress(self, book_name):
        file_path = self._get_progress_path()
        f = open(file_path, 'r')
        
        all_progress = []
        file_content = f.read()
        if file_content:
            all_progress = json.loads(file_content)

        for progress in all_progress:
            if progress["book_name"] == book_name:
                return progress
        
        return None

    def save_progress(self, book_name, page_num, line_num):
        file_path = self._get_progress_path()
        file_reader = open(file_path, 'r')

        all_progress = []
        file_content = file_reader.read()
        if file_content:
            all_progress = json.loads(file_content)
        file_reader.close()

        modified_progress = [
            *list(filter(lambda progress: progress["book_name"] != book_name, all_progress)),
            {
                "book_name": book_name,
                "page_num": page_num,
                "line_num": line_num
            }
        ]

        f = open(file_path, 'w')
        f.write(json.dumps(modified_progress))
        f.close()
        return

    def last_progress(self) -> str:
        file_path = self._get_progress_path()
        f = open(file_path, 'r')

        all_progress = []
        file_content = f.read()
        if file_content:
            all_progress = json.loads(file_content)

        if not all_progress:
            return None
        
        return all_progress[-1]["book_name"]


#todo: add support for more types than pdf
#todo: add chapter support
#todo: add first page support 
# 
# 
# [test] continue
# line change  