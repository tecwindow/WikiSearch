# WikiSearch
This simple program enables you to search Wikipedia, the free encyclopedia, without having to open your browser.

## what's new:

### Version 1.2:

This version comes with numerous new features and bug fixes.

- Added French translation, Thanks Riad Assoum.
-  You can now adjust the size and color of the font while reading the article.
-  Added an option to display a dialog with the tables in the article. Warning: it may not always display correctly, but rather depends on the format of the article.
-  Added an option to display a list of external references from within the article so that you can open any of them in your browser.
-  Added an option to display articles that are linked to the currently displayed article. You may interact with them just like you do with the search results.
-  You can now save the article as an HTML file.
-  Added the ability to display random articles with their language depending on the already set search language. You may interact with them just like you do with the search results.
-  Added an option in settings to view the article as HTML (note: buggy and unreliable).
-  Added quite a few communication methods in the main menu to reach the developers.
-  Changed a few options within the action menu of the displayed article window.
-  The program will start faster if you disable the auto check for updates feature.
-  Fixed the bug where an update's changelog was not being shown correctly in the update dialog.
-  Changed some keyboard shortcut.
-  Fixed a few minor bugs here and there.

#### Notes:

- Due to a change in the language suffixes in this version, the program language will automatically revert back to English after the update. You will need to change it only once and it will auto-save just like before.
- All new article options can be found by pressing alt and browsing the menus where you may find and learn all the hotkeys.
- All hotkeys will later be written to this file.

### Version 1.1:

We are still learning and improving this software as we improve our knowledge of programming, and we have been able to add quite a few features in this version.

- The program now supports translation and you can contribute to translating it into your language.
- The English strings have been rechecked and an Arabic translation has been added, many thanks to Riad Assoum.
- A Spanish translation was added, many thanks to Georgiana frincu.
- Hotkeys have been greatly improved, each feature of the program now has its own functioning hotkey.
- Screen readers will now speak a number of actions if performed properly by the user.
- Screen readers will notify you when an article is loaded.
- You can now jump to any of the article headings while reading it.
- You can now customize the number of search results up to 100 at the moment (you can change the number from the settings).
- You can now close the article window using the escape key (you can enable this feature from the settings).
- The program will now warn you if you try to close it while one or more articles are open (this feature can be disabled from the settings).
- The program will now check for updates automatically when launched (you can disable this feature from the settings.
- The program will now remember the selected search language for future uses.

## Features
* Look up any article quickly and efficiently.
* View the entire article from within the program.
* Browse more than one article at a time in separate windows.
* Save articles as text files on your PC.
* Change the color of the entire frame while reading the article. The next versions will allow further customizations to the colors and fonts.
* An auto-updater that allows users quick access to new features.

## Supported OS:
The software supports Windows 8 and above with both 32 and 64 bit architectures.

## Requirements
Python 3.xx 

## Modules and packages
* accessible_output2
* nlpia2_wikipedia
* webbrowser
* subprocess
* threading 
* pyperclip
* wxpython
* request
* mouse
* json
* bs4
* os
* re

## How to use
* install  all packages using pip
`pip install -r requirements.txt`
* start WikiSearch.py
`python WikiSearch.py
* Search for what you want

## Program developers:
* MesterPerfect https://github.com/mesterPerfect
* QaisAlrefai https://github.com/QaisAlrefai
* MahmoudAtef https://github.com/MahmoudAtefFarook

## special thanks:

Many of our friends and users contributed to testing the program and sending us their feedback and suggestions. In no particular order, we would like to thank Riad, ikrami, Mahmoud shrawy, Muhammad Hajjar, Ahmed Manninah, Moataz Geba, Fawaz Abdul Rahman, Georgiana frincu, Agustín aguirre, Angelina, Nacer baaziz, Hermina.