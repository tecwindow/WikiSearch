# WikiSearch

## Fonction du programme :

Ce programme simple vous permet de faire des recherches dans Wikipédia, l'encyclopédie libre, sans avoir à ouvrir votre navigateur.

## Nouveautés :

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

#### Notes:

- The Print Article feature has been added, it should work fine when used from the article view window in html. If you are using the classic view to read the article, we are sorry to say that we have not been able to get the feature to work optimally at this time. If you are able to contribute to the completion of the feature, you can do so via GitHub.
- Please note that saving a large number of articles offline may increase the file size.

### Version 1.3:

This version comes with some bug fixes.

- Now the French translation will appear correctly.
- Fixed the issue related to the Unicode.
- Fixed the bug where the program did not launch if it was installed for the first time and not updated from a previous version.

### Version 1.2:

Cette version comporte de nombreuses nouvelles fonctionnalités et corrections de bugs.

- Ajout de la traduction française, Merci Riad Assoum.
-  Vous pouvez maintenant ajuster la taille et la couleur de la police pendant la lecture de l'article.
- Ajout d'une option pour afficher un dialogue avec les tableaux de l'article. Attention : cela ne s'affiche pas toujours correctement, cela dépend plutôt du format de l'article.
-  Ajout d'une option permettant d'afficher une liste de références externes à l'intérieur de l'article afin que vous puissiez les ouvrir dans votre navigateur.
- Ajout d'une option permettant d'afficher les articles liés à l'article actuellement affiché. Vous pouvez interagir avec eux comme vous le faites avec les résultats de la recherche.
- Vous pouvez maintenant sauvegarder l'article en tant que fichier HTML.
- Ajout de la possibilité d'afficher des articles au hasard dont la langue dépend de la langue de recherche déjà définie. Vous pouvez interagir avec eux comme vous le faites avec les résultats de la recherche.
-  Ajout d'une option dans les paramètres pour afficher l'article au format HTML (note : boguée et peu fiable).
-  Ajout de plusieurs méthodes de communication dans le menu principal pour contacter les développeurs.
-  Modification de quelques options dans le menu d'action de la fenêtre de l'article affiché.
- Le programme démarrera plus rapidement si vous désactivez la fonction de vérification automatique des mises à jour.
- Correction d'un bug où le journal des modifications d'une mise à jour ne s'affichait pas correctement dans la boîte de dialogue de mise à jour.
- Modification de certains raccourcis clavier.
- Correction de quelques bugs mineurs çà et là.

#### Remarques :

- En raison d'un changement dans les suffixes de langue dans cette version, la langue du programme reviendra automatiquement à l'anglais après la mise à jour. Vous n'aurez à la changer qu'une seule fois et elle sera sauvegardée automatiquement comme avant.
- Toutes les nouvelles options d'article peuvent être trouvées en appuyant sur alt et en parcourant les menus où vous pouvez trouver et apprendre toutes les touches de raccourci.
- Tous les raccourcis seront plus tard écrits dans ce fichier.

### Version 1.1:

Nous continuons à apprendre et à améliorer ce logiciel au fur et à mesure que nous améliorons notre connaissance de la programmation, et nous avons pu ajouter un certain nombre de fonctionnalités dans cette version.

- Le programme supporte maintenant la traduction et vous pouvez contribuer à le traduire dans votre langue.
- Le fichier de langue anglaise a été revérifié et une traduction arabe a été ajoutée, un grand merci à Riad Assoum.
- Une traduction en espagnol a été ajoutée, un grand merci à Georgiana frincu.
- Les touches de raccourci ont été grandement améliorées, chaque fonctionnalité du programme a maintenant sa propre touche de raccourci fonctionnelle.
- Les lecteurs d'écran prononcent désormais un certain nombre d'actions si elles sont effectuées correctement par l'utilisateur.
- Les lecteurs d'écran vous avertiront lorsqu'un article est chargé.
- Vous pouvez désornais sauter à n'importe quelle entête de l'article tout en le lisant.
- Vous pouvez désormais personnaliser le nombre de résultats de recherche, jusqu'à 100 pour le moment (vous pouvez modifier ce nombre dans les paramètres).
- Vous pouvez maintenant fermer la fenêtre de l'article en utilisant la touche "Echap" (vous pouvez activer cette fonction dans les paramètres).
- Le programme vous avertit désormais si vous essayez de le fermer alors qu'un ou plusieurs articles sont ouverts (cette fonction peut être désactivée dans les paramètres).
- Le programme vérifie désormais automatiquement les mises à jour lorsqu'il est lancé (vous pouvez désactiver cette fonction dans les paramètres).
- Le programme se souvient désormais de la langue de recherche sélectionnée pour les utilisations futures.

## remerciements spéciaux :

Beaucoup de nos amis et des utilisateurs du programme ont contribué à le tester et à nous envoyer leurs commentaires et suggestions. Sans ordre particulier, nous aimerions remercier Riad, ikrami, Mahmoud shrawy, Muhammad Hajjar, Ahmed Manninah, Moataz Geba, Fawaz Abdul Rahman, Georgiana frincu, Agustín aguirre, Angelina, Nacer baaziz, Abdulla dubais, Hermina.

## fonctionnalités du programme :

- Rechercher n'importe quel article rapidement et efficacement.
- Afficher l'article entier à partir du programme.
- Parcourir plus d'un article à la fois dans des fenêtres séparées.
- Sauvegarder les articles en tant que fichiers texte sur votre PC.
- Changer la couleur et la police pendant la lecture de l'article.
- Une mise à jour automatique qui permet aux utilisateurs d'accéder rapidement aux nouvelles fonctionnalités.

## Remarques :

- Nous mettrons constamment à jour le programme pour ajouter de nouvelles fonctionnalités demandées par nos utilisateurs. Cela signifie que plus une fonctionnalité est suggérée, plus vite elle sera mise en œuvre.
- Si vous souhaitez traduire le programme dans votre langue, veuillez nous contacter via l'une des adresses e-mail de ce fichier ou nos comptes Telegram.
- Vous pouvez suggérer des fonctionnalités et signaler des bugs via GitHub ou nous contacter via nos comptes de médias sociaux disponibles dans le menu principal.
- Le logiciel prend en charge Windows 8 et plus avec les architectures 32 et 64 bits.

Dépôt GitHub : https://github.com/tecwindow/WikiSearch
## Développeurs du programme :

- Mahmoud Atef: mahmoud.atef.987123@gmail.com
- Mester Perfect: AhmedBakr593@gmail.com
- Qais Alrefai: ww258148@gmail.com
- TecWindow sur Telegram: https://t.me/TecWindow
- a2ztec sur Telegram: https://t.me/A2zTecChannel
