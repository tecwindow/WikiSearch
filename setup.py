# setup.py

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
"build_exe": "WikiSearch",
"optimize": 1,
"include_files": ["LanguageCodes.json", "help", "languages"],
"packages": ["web_viewer", "view_search_dialog", "view_article_window", "update_dialog", "settings", "my_classes", "functions", "dialogs"],
"includes": ["wx", "nlpia2_wikipedia", "pyperclip", "accessible_output2", "mouse", "bs4", "requests", ],
"zip_include_packages": ["wx"],
"excludes": ["tkinter", "test", "setuptools", "PyInstaller", "pip", "numpy"],
"include_msvcr": False
}

description="WikiSearch"

# GUI applications require a different base on Windows (the default is for a
# console application).
base= None
if sys.platform == "win32":
	base = "Win32GUI"
	setup(name="WikiSearch", version="1.4.0", description=description, options={"build_exe": build_exe_options}, executables=[Executable("WikiSearch.py", base=base)])