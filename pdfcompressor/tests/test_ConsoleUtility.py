import sys
from io import StringIO
from unittest import TestCase

from pdfcompressor.utility.console_utility import ConsoleUtility


class ConsoleUtilityTest(TestCase):
    @staticmethod
    def get_console_buffer() -> StringIO:
        console_buffer = StringIO()
        sys.stdout = console_buffer
        return console_buffer

    # ConsoleUtility.print()
    def test_print_quiet_mode_is_not_active(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.QUIET_MODE = False
        ConsoleUtility.print("test")
        self.assertEqual("test\n", console_buffer.getvalue())

    def test_print_quiet_mode_is_active(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.quiet_mode = True
        ConsoleUtility.print("test")

        # reset to default
        ConsoleUtility.quiet_mode = False

        self.assertEqual("", console_buffer.getvalue())

    def test_print_with_empty_string(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.QUIET_MODE = False
        ConsoleUtility.print("")
        self.assertEqual("\n", console_buffer.getvalue())

    # ConsoleUtility.get_error_string()
    def test_get_error_string_with_valid_string(self):
        self.fail("not implemented yet")

    def test_get_error_string_with_valid_string_already_ansi_colored(self):
        self.fail("not implemented yet")

    def test_get_error_string_with_empty_string(self):
        self.fail("not implemented yet")

    # ConsoleUtility.get_file_string()
    def test_get_file_string_with_valid_string(self):
        self.fail("not implemented yet")

    def test_get_file_string_with_valid_string_already_ansi_colored(self):
        self.fail("not implemented yet")

    def test_get_file_string_with_empty_string(self):
        self.fail("not implemented yet")

    def test_print_stats_with_zero_as_orig(self):
        ConsoleUtility.QUIET_MODE = False
        self.assertRaises(
            ValueError,
            ConsoleUtility.print_stats, 0, 150, "File"
        )

    def test_print_stats_with_negative_orig(self):
        ConsoleUtility.QUIET_MODE = False
        self.assertRaises(
            ValueError,
            ConsoleUtility.print_stats, -5, 150, "File"
        )

    def test_print_stats_orig_smaller_than_result(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.QUIET_MODE = False
        ConsoleUtility.print_stats(100, 150, "File")
        self.assertTrue(console_buffer.getvalue().__contains__("-50.0%"))

    def test_print_stats_orig_bigger_than_result(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.QUIET_MODE = False
        ConsoleUtility.print_stats(200, 150, "File")
        self.assertTrue(console_buffer.getvalue().__contains__("-25.0%"))

    def test_print_stats_orig_equal_to_result(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.QUIET_MODE = False
        ConsoleUtility.print_stats(150, 150, "File")
        self.assertTrue(console_buffer.getvalue().__contains__("-0.0%"))

    def test_print_stats_with_zero_as_result(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.QUIET_MODE = False
        ConsoleUtility.print_stats(150, 0, "File")
        self.assertTrue(console_buffer.getvalue().__contains__("-100.0%"))

    def test_print_stats_with_empty_string_as_compressed_value(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.QUIET_MODE = False
        ConsoleUtility.print_stats(150, 0, "")
        self.assertTrue(console_buffer.getvalue().__contains__("  "))

    def test_print_stats_normal_compressed_value(self):
        console_buffer = ConsoleUtilityTest.get_console_buffer()
        ConsoleUtility.QUIET_MODE = False
        ConsoleUtility.print_stats(150, 0, "File")
        self.assertTrue(console_buffer.getvalue().__contains__("File"))

    def test_print_stats_with_negative_result(self):
        ConsoleUtility.QUIET_MODE = False
        self.assertRaises(
            ValueError,
            ConsoleUtility.print_stats, 150, -5, "File"
        )
