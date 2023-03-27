# WikiSearch

## Program function:

This simple program enables you to search Wikipedia, the free encyclopedia, without having to open your browser.

## what's new:

### Version 1.4:

This version includes many features and bug fixes.

- Added several article lists.
    - Added the ability to save articles for offline reading. You can save the article within the program and return to it at any time.
    - Added the Favorite articles feature, which allows you to save any article to the list of favorite articles so that you can return to it at any time from the same list.
    - Added the History feature, a list that stores the articles you have visited and allows you to return to them at any time.
        - The Favorites and Saved articles lists allow you to rename the article and delete any saved articles. Press the Applications key on any item in either list and you will find the appropriate options. You can also use the Delete key to delete items or the F2 key to rename them.
        - You can save any article from the action menu in the article view window, and you can access these lists from the main menu in the main window. Each option has its own shortcut.
        - Articles data is stored in a file named WikiSearch.db in the WikiSearch folder in AppData\Roaming. You can delete a specific portion of the file's contents from within the program's settings.

- Added a feature to detect Wikipedia links from your clipboard when you open WikiSearch. You can view the article in the program, open it in the browser, or ignore the message. You can enable or disable this feature in the settings.
- If you paste the link of an article from Wikipedia into the search field and press Enter, the article will be displayed immediately.
- WikiSearch now launches in the language selected during installation.
- Some  improvements have been made to the article display window in the html page. Due to a change in wxPython, the nvda screen reader cannot navigate through the list of actions. To work around this problem, go to any button in the window and press alt, and the menus will work fine.
- Added the status bar to View article window, containing a counter for the number of letters, words, etc. in the article. You can get the same information by pressing numbers from 1 to 5.
- Added a checkbox to disable the closing warning window when there are open articles, the checkbox appears in the same window.
- The view tables window no longer shows empty lines.
- Program windows now support resizing and dragging on the screen.
- Added an option in the settings to restore the program to its default settings.
- Updated the version of Python used to Python 3.10 and wxPython to 4.2.0. Replaced Pyinstaller with Cx_Frees.
- Fixed a bug where WikiSearch returned a different article than the one selected in the search results.
- Fixed a bug where WikiSearch would search in a different language than the one selected in the search language.
- Fixed a bug where the closing warning window did not correctly display the number of open articles.
- Disabled the previously available trick to increase the number of results above 100.
- WikiSearch no longer uses Sapi5 to speak some actions when used without a screen reader.
- Several code improvements have been made, as well as a number of small bug fixes here and there.

#### Note:

- The Print Article feature has been added, it should work fine when used from the article view window in html. If you are using the classic view to read the article, we are sorry to say that we have not been able to get the feature to work optimally at this time. If you are able to contribute to the completion of the feature, you can do so via GitHub.

### Version 1.3:

This version comes with some bug fixes.

- Now the French translation will appear correctly.
- Fixed the issue related to the Unicode.
- Fixed the bug where the program did not launch if it was installed for the first time and not updated from a previous version.

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
- A Spanish translation was added, many thanks to Georgiana Frincu.
- Hotkeys have been greatly improved, each feature of the program now has its own functioning hotkey.
- Screen readers will now speak a number of actions if performed properly by the user.
- Screen readers will notify you when an article is loaded.
- You can now jump to any of the article headings while reading it.
- You can now customize the number of search results up to 100 at the moment (you can change the number from the settings).
- You can now close the article window using the escape key (you can enable this feature from the settings).
- The program will now warn you if you try to close it while one or more articles are open (this feature can be disabled from the settings).
- The program will now check for updates automatically when launched (you can disable this feature from the settings).
- The program will now remember the selected search language for future uses.

## special thanks:

Many of our friends and users contributed to testing the program and sending us their feedback and suggestions. In no particular order, we would like to thank Riad, ikrami, Mahmoud shrawy, Muhammad Hajjar, Ahmed Manninah, Moataz Geba, Fawaz Abdul Rahman, Georgiana frincu, Agustín aguirre, Angelina, Nacer baaziz, Abdulla dubais, Hermina.

## Features:

- Look up any article quickly and efficiently.
- View the entire article from within the program.
- Browse more than one article at a time in separate windows.
- Save articles as  files on your PC.
- Change the color and font while reading the article.
- An auto-updater that allows users quick access to new features.

## Notes:

- We will constantly update the program to add new features requested by our users. This means that the more a feature is suggested, the quicker it will be implemented.
- If you want to translate the program into your language, please contact us via one of the E-mail addresses in this file or our Telegram accounts.
- You can suggest features and report bugs via GitHub or contact us via our social media accounts available in the main menu.
- The software supports Windows 8 and above with both 32 and 64 bit architectures.

GitHub repository: https://github.com/tecwindow/WikiSearch
## Program developers:

- Mahmoud Atef: mahmoud.atef.987123@gmail.com
- Mester Perfect: AhmedBakr593@gmail.com
- Qais Alrefai: ww258148@gmail.com
