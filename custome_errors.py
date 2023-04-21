import traceback
import os
import ctypes
import sys
def my_excepthook(exctype, value, tb):
    tb_list = traceback.extract_tb(tb)
    error_message = ""

    for tb in tb_list:
        file_name = os.path.basename(tb.filename)
        line_number = tb.lineno
        code = tb.line

        error_message += f"\nFile: {file_name}\nLine: {line_number}\nCode: {code}\n"

    error_message += f"\n{exctype.__name__}: {value}"

    ctypes.windll.user32.MessageBoxW(None, error_message, "Error", 0x10)
