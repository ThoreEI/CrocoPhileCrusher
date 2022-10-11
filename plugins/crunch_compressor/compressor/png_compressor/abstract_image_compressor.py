import os
from abc import ABC

from PIL import Image

from ..compressor import Compressor
from ...utility.EventHandler import EventHandler


class AbstractImageCompressor(Compressor, ABC):
    def __init__(
            self,
            file_type_from: str = "png",
            file_type_to: str = "png",
            event_handlers: list[EventHandler] = list()
    ):
        super().__init__(
            event_handlers=event_handlers,
            file_type_from=file_type_from,
            file_type_to=file_type_to,
            processed_part="Pages",
        )

    @staticmethod
    def _is_valid_image(path: str) -> bool:
        try:
            with Image.open(path) as img:
                img.verify()
            return True
        except:
            # couldn't open and verify -> not a valid image
            return False

    def compress_file_list(self, source_files: list, destination_files: list) -> None:
        self.compress_file_list_multi_threaded(
            source_files,
            destination_files,
            # use all cores, but after 8 it splits bigger tasks -> only 4 each
            os.cpu_count() if os.cpu_count() < 8 else 4
        )

    def _compare_and_use_better_option(self, file_option_1: str, file_option_2: str, destination_file: str) -> None:

        size_option_1 = OsUtility.get_file_size(file_option_1)
        size_option_2 = OsUtility.get_file_size(file_option_2)

        # compression worked -> copy file to final destination
        if self._is_valid_image(file_option_2) and size_option_1 > size_option_2 or \
                not self._is_valid_image(file_option_1):
            OsUtility.copy_file(file_option_2, destination_file)
        # error in output file -> copy source file to destination
        else:
            OsUtility.copy_file(file_option_1, destination_file)
