import os
import shutil

from pdfcompressor.utility.ConsoleUtility import ConsoleUtility


class OsUtility:
    @staticmethod
    def get_file_list(folder: str, ending: str = "") -> list:
        if not os.path.exists(folder):
            raise FileNotFoundError
        if os.path.isfile(folder):
            raise ValueError
        # get all the png files in temporary folder <=> all pdf pages
        files = []
        for r, _, f in os.walk(folder):
            for file_name in f:
                if not file_name.endswith(ending):
                    continue
                files.append(os.path.join(r, file_name))
        return files

    @staticmethod
    def clean_up_folder(folder: str) -> None:
        if os.path.isfile(folder):
            raise ValueError
        if not os.path.exists(folder):
            raise FileNotFoundError
        # removes the directory and files in 'folder'
        ConsoleUtility.print("--cleaning up--")
        if os.path.isdir(folder):
            shutil.rmtree(folder)

    @staticmethod
    def create_folder_if_not_exist(file_path: str) -> None:
        # checks if .pdf file else creates folder if there is no folder, yet
        if not file_path.endswith(".pdf") and not os.path.isdir(file_path):
            os.mkdir(file_path)
        elif not os.path.isdir(os.path.dirname(file_path)):
            os.mkdir(os.path.dirname(file_path))

    @staticmethod
    def get_filename(full_path_to_file: str) -> str:
        # TODO file ending regex
        # remove .pdf, path (only Filename)
        return full_path_to_file[:-4].split(os.path.sep)[-1]
