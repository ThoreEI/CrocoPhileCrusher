#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==================================================================
#  crunch
#    A PNG file optimization tool built on pngquant and zopflipng
#
#   Copyright 2019 Christopher Simpkins
#   MIT License
#
#   Source Repository: https://github.com/chrissimpkins/Crunch
# ==================================================================
#
#   Edited by Philip Dell
#   Easy Implementation of crunch png
#   Copyright 2021 Philip Dell
#   MIT Licence
#
#========================

import sys
import os
import shutil
import struct
import subprocess
from subprocess import CalledProcessError

from multiprocessing import Lock
stdstream_lock = Lock()

# Dependency Path Constants for Command Line Executable
#  - Redefine these path strings to use system-installed versions of
#    pngquant and zopflipng (e.g. to "/usr/local/bin/[executable]")
PNGQUANT_CLI_PATH = os.path.join(os.path.expanduser("~"), "pngquant", "pngquant")
ZOPFLIPNG_CLI_PATH = os.path.join(os.path.expanduser("~"), "zopfli", "zopflipng")


def crunch(png_path = None, pngquant_path = None, zoplfi_path = None ):
    global PNGQUANT_CLI_PATH, ZOPFLIPNG_CLI_PATH
    if not pngquant_path is None:
        PNGQUANT_CLI_PATH = pngquant_path
    if not zoplfi_path is None:
        ZOPFLIPNG_CLI_PATH = zoplfi_path

    ERROR_STRING = "[ ! ]"
    # No Path Specified
    if png_path is None:
        sys.stderr.write(ERROR_STRING + " filepath not specified")
        sys.exit(1)

    # Not a file test
    if not os.path.isfile(png_path):  # is not an existing file
        sys.stderr.write(ERROR_STRING +" '"+ png_path
            +"' does not appear to be a valid path to a PNG file\n")
        sys.exit(1)  # not a file, abort immediately

    # PNG validity test
    if not is_valid_png(png_path):
        sys.stderr.write(ERROR_STRING +" '"+ png_path
            +"' is not a valid PNG file.\n")
        sys.exit(1)

    # Dependency error handling
    if not os.path.exists(PNGQUANT_CLI_PATH):
        sys.stderr.write(ERROR_STRING +" pngquant executable was not identified on path '"
            + PNGQUANT_CLI_PATH +"'\n")
        sys.exit(1)
    elif not os.path.exists(ZOPFLIPNG_CLI_PATH):
        sys.stderr.write(ERROR_STRING +" zopflipng executable was not identified on path '"
            + ZOPFLIPNG_CLI_PATH +"'\n")
        sys.exit(1)
    print("    Init compression")
    optimize_png(png_path)


def optimize_png(png_path):
    img = ImageFile(png_path)

    ERROR_STRING = "[ ! ]"

    # --------------
    # pngquant stage
    # --------------
    pngquant_options = (
        " --quality=80-98 --skip-if-larger --force --strip --speed 1 --ext '-crunch.png' "
    )
    system_extra = ""
    if os.name == 'nt':#windows
        system_extra = "powershell.exe "#cmd doesnt work for the command
    pngquant_command = (
        system_extra + PNGQUANT_CLI_PATH + pngquant_options + shellquote(img.pre_filepath)
    )
    try:
        subprocess.check_output(pngquant_command, stderr=subprocess.STDOUT, shell=True)
        print("    pngquant compression finished.")
    except CalledProcessError as cpe:
        if cpe.returncode == 98:
            # this is the status code when file size increases with execution of pngquant.
            # ignore at this stage, original file copied at beginning of zopflipng processing
            # below if it is not present due to these errors
            pass
        elif cpe.returncode == 99:
            # this is the status code when the image quality falls below the set min value
            # ignore at this stage, original lfile copied at beginning of zopflipng processing
            # below if it is not present to these errors
            pass
        else:
            stdstream_lock.acquire()
            sys.stderr.write(ERROR_STRING +" "+ img.pre_filepath
                +" processing failed at the pngquant stage.\n")
            stdstream_lock.release()
            raise cpe
    except Exception as e:
            raise e

    # ---------------
    # zopflipng stage
    # ---------------
    # use --filters=0 by default for quantized PNG files (based upon testing by CS)
    zopflipng_options = " -y --filters=0 "
    # confirm that a file with proper path was generated by pngquant
    # pngquant does not write expected file path if the file was larger after processing
    if not os.path.exists(img.post_filepath):
        shutil.copy(img.pre_filepath, img.post_filepath)
        # If pngquant did not quantize the file, permit zopflipng to attempt compression with mulitple
        # filters.  This achieves better compression than the default approach for non-quantized PNG
        # files, but takes significantly longer (based upon testing by CS)
        zopflipng_options = " -y --lossy_transparent "
    zopflipng_command = (
        ZOPFLIPNG_CLI_PATH + zopflipng_options +
        shellquote(img.post_filepath) +" "+ shellquote(img.post_filepath)
    )
    try:
        subprocess.check_output(zopflipng_command, stderr=subprocess.STDOUT, shell=True)
        print("    zopfli compression finished.")
    except CalledProcessError as cpe:
        stdstream_lock.acquire()
        sys.stderr.write(ERROR_STRING +" "+ img.pre_filepath
            + " processing failed at the zopflipng stage.\n")
        stdstream_lock.release()
        raise cpe
    except Exception as e:
        raise e

    # Check file size post-optimization and report comparison with pre-optimization file
    img.get_post_filesize()
    percent = img.get_compression_percent()
    percent_string = "{0:.2f}%".format(percent)

    # report percent original file size / post file path / size (bytes) to stdout (command line executable)
    stdstream_lock.acquire()
    print("[ Compressed to " + percent_string + " ] ")
    stdstream_lock.release()

# -----------
# Utilities
# -----------

def is_valid_png(filepath):
    # The PNG byte signature (https://www.w3.org/TR/PNG/#5PNG-file-signature)
    expected_signature = struct.pack("8B", 137, 80, 78, 71, 13, 10, 26, 10)
    # open the file and read first 8 bytes
    with open(filepath, "rb") as filer:
        signature = filer.read(8)
    # return boolean test result for first eight bytes == expected PNG byte signature
    return signature == expected_signature


def shellquote(filepath):
    return "'" + filepath.replace("'", "'\\''") + "'"


class ImageFile(object):
    def __init__(self, filepath):
        self.pre_filepath = filepath
        self.post_filepath = self._get_post_filepath()
        self.pre_size = self._get_filesize(self.pre_filepath)
        self.post_size = 0

    def _get_filesize(self, file_path):
        return os.path.getsize(file_path)

    def _get_post_filepath(self):
        path, extension = os.path.splitext(self.pre_filepath)
        return path + "-crunch" + extension

    def get_post_filesize(self):
        self.post_size = self._get_filesize(self.post_filepath)

    def get_compression_percent(self):
        ratio = float(self.post_size) / float(self.pre_size)
        percent = ratio * 100
        return percent
