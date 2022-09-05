import os
import subprocess
import sys
from unittest import TestCase
from io import StringIO
import jsons

from pdfcompressor.utility.os_utility import OsUtility


class TestOsUtility(TestCase):
    config_file = "../../config.json"

    program_path: str = os.path.abspath('../..')
    source_path = os.path.join(".", "TestData", "singlePagePdf.pdf")
    result_path = os.path.join(".", "TestData", "singlePagePdf_compressed.pdf")

    @staticmethod
    def get_console_buffer() -> StringIO:
        console_buffer = StringIO()
        sys.stdout = console_buffer
        return console_buffer

    def __run_simple_compression(self, assume_success: bool, simple_and_lossless: bool) -> tuple[StringIO, int]:
        console_buffer = self.get_console_buffer()

        if os.path.isfile(self.result_path):
            os.remove(self.result_path)

        args = [
            "python3", self.program_path,
            "-p", self.source_path
        ]
        if simple_and_lossless:
            args.append("--simple-and-lossless")

        return_code = subprocess.call(args)
        if assume_success or simple_and_lossless:
            self.assertTrue(os.path.exists(self.result_path))
            os.remove(self.result_path)
            self.assertEqual(0, return_code)
            self.assertFalse("Error:" in console_buffer.getvalue())  # TODO console buffer
        else:
            self.assertTrue("Error:" in console_buffer.getvalue())  # TODO console buffer

        return console_buffer, return_code

    def __get_config(self):
        with open(self.config_file, "r") as f:
            return jsons.loads(f.read())

    def __write_new_config(self, json_config: object):
        with open(self.config_file, "w") as f:
            f.write(jsons.dumps(json_config))

    def __change_path(self, path_to_change: str, new_path_value: str):
        config = self.__get_config()
        config[path_to_change] = new_path_value
        self.__write_new_config(config)

    def __change_to_empty_path(self, path_to_change: str):
        self.__change_path(path_to_change, "")

    def __change_to_invalid_path(self, path_to_change: str):
        self.__change_path(path_to_change, "some_invalid/path")

    def test_with_advpng_path_is_empty(self):
        self.__change_to_empty_path("advpng_path")
        self.__run_simple_compression(False, False)

    def test_with_advpng_path_is_valid(self):  # should be valid for all paths
        self.__run_simple_compression(True, False)

    def test_with_advpng_path_is_invalid(self):
        self.__change_to_invalid_path("advpng_path")
        self.__run_simple_compression(False, False)

    def test_with_advpng_path_is_valid_with_simple_and_lossless(self):  # should be valid for all paths
        self.__run_simple_compression(True, True)

    def test_with_advpng_path_is_invalid_with_simple_and_lossless(self):
        self.__change_to_invalid_path("advpng_path")
        self.__run_simple_compression(True, True)

    def test_with_pngquant_path_is_empty(self):
        self.__change_to_empty_path("pngquant_path")
        self.__run_simple_compression(False, False)

    '''
    def test_with_pngquant_path_is_valid(self):
        self.fail("Not implemented yet")
    '''

    def test_with_pngquant_path_is_invalid(self):
        self.__change_to_invalid_path("pngquant_path")
        self.__run_simple_compression(False, False)

    '''
    def test_with_pngquant_path_is_valid_with_simple_and_lossless(self):
        self.fail("Not implemented yet")
    '''

    def test_with_pngquant_path_is_invalid_with_simple_and_lossless(self):
        self.__change_to_invalid_path("pngquant_path")
        self.__run_simple_compression(True, True)

    def test_with_pngcrush_path_is_empty(self):
        self.__change_to_empty_path("pngcrush_path")
        self.__run_simple_compression(False, False)

    '''
    def test_with_pngcrush_path_is_valid(self):
        self.fail("Not implemented yet")
    '''

    def test_with_pngcrush_path_is_invalid(self):
        self.__change_to_invalid_path("pngcrush_path")
        self.__run_simple_compression(False, False)

    '''
    def test_with_pngcrush_path_is_valid_with_simple_and_lossless(self):
    self.fail("Not implemented yet")
    '''

    def test_with_pngcrush_path_is_invalid_with_simple_and_lossless(self):
        self.__change_to_invalid_path("pngcrush_path")
        self.__run_simple_compression(True, True)

    def test_with_cpdfsqueeze_path_is_empty(self):
        self.__change_to_empty_path("cpdfsqueeze_path")
        self.__run_simple_compression(False, False)

    '''
    def test_with_cpdfsqueeze_path_is_valid(self):
        self.__test_invalid_path("cpdfsqueeze_path")
    '''

    def test_with_cpdfsqueeze_path_is_invalid(self):
        self.__change_to_invalid_path("cpdfsqueeze_path")
        self.__run_simple_compression(False, False)

    '''
    def test_with_cpdfsqueeze_path_is_valid_with_simple_and_lossless(self):
        self.fail("Not implemented yet")
    '''

    def test_with_cpdfsqueeze_path_is_invalid_with_simple_and_lossless(self):
        self.fail("Not implemented yet")

    def test_with_tesseract_path_is_empty(self):
        self.__change_to_empty_path("tesseract_path")
        self.__run_simple_compression(False, False)

    '''
    def test_with_tesseract_path_is_valid(self):
        self.fail("Not implemented yet")
    '''

    def test_with_tesseract_path_is_invalid(self):
        self.__change_to_invalid_path("tesseract_path")
        self.__run_simple_compression(False, False)

    def test_with_tessdata_prefix_is_empty(self):
        # TODO precondition
        self.__change_to_empty_path("tessdata_prefix")
        self.__run_simple_compression(False, False)
        self.fail("Not fully implemented yet")

    def test_with_tessdata_prefix_is_valid(self):
        self.fail("Not implemented yet")

    def test_with_tessdata_prefix_is_invalid(self):
        # self.__change_to_invalid_path("tessdata_prefix")
        # self.__run_simple_compression(False, False)
        self.fail("Not implemented yet")

    def test_tesseract_with_no_ocr(self):
        self.fail("Not implemented yet")

    def setUp(self) -> None:
        # save the original file as a copy
        OsUtility.copy_file(self.config_file, self.config_file + "_tmp")

    def tearDown(self) -> None:
        # restore the original
        OsUtility.move_file(self.config_file + "_tmp", self.config_file)
        # restore stout
#        sys.stdout = sys.__stdout__