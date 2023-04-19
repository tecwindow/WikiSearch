# WikiSearch

## Fonction du programme :

Ce programme simple vous permet de faire des recherches dans Wikipédia, l'encyclopédie libre, sans avoir à ouvrir votre navigateur.

## Nouveautés :

### Version 1.4 :

Cette version comprend de nombreuses fonctionnalités et corrections de bugs.

- Ajout de plusieurs listes d'articles.
    - Ajout de la possibilité de sauvegarder des articles pour une lecture hors ligne. Vous pouvez sauvegarder l'article dans le programme et y revenir à tout moment.
    - Ajout de la fonction Articles favoris, qui vous permet d'enregistrer n'importe quel article dans la liste des articles favoris afin de pouvoir y revenir à tout moment à partir de la même liste.
    - Ajout de la fonction Historique, une liste qui enregistre les articles que vous avez consultés et vous permet d'y revenir à tout moment.
        - Les listes Favoris et Articles sauvegardés vous permettent de renommer l'article et de supprimer les articles sauvegardés. Appuyez sur la touche Applications sur n'importe quel élément de l'une ou l'autre liste et vous trouverez les options appropriées. Vous pouvez également utiliser la touche Suppr pour supprimer des articles ou la touche F2 pour les renommer.
        - Vous pouvez sauvegarder n'importe quel article à partir du menu d'action de la fenêtre d'affichage des articles, et vous pouvez accéder à ces listes à partir du menu principal de la fenêtre principale. Chaque option possède son propre raccourci.
        - Les données des articles sont stockées dans un fichier nommé WikiSearch.db dans le dossier WikiSearch dans AppData\Roaming. Vous pouvez supprimer une partie spécifique du contenu du fichier à partir des paramètres du programme.
- Ajout d'une fonctionnalité permettant de détecter les liens Wikipédia à partir de votre presse-papiers lorsque vous ouvrez WikiSearch. Vous pouvez afficher l'article dans le programme, l'ouvrir dans le navigateur ou ignorer le message. Vous pouvez activer ou désactiver cette fonctionnalité dans les paramètres.
- Si vous collez le lien d'un article de Wikipedia dans le champ de recherche et que vous appuyez sur Entrée, l'article s'affichera immédiatement.
- WikiSearch se lance désormais dans la langue sélectionnée lors de l'installation.
- Des améliorations ont été apportées à la fenêtre d'affichage des articles dans la page html. En raison d'un changement dans wxPython, le lecteur d'écran nvda ne peut pas naviguer dans la liste des actions. Pour contourner ce problème, allez sur n'importe quel bouton de la fenêtre et appuyez sur alt, et les menus fonctionneront correctement.
- Ajout d'une barre d'état à la fenêtre Affichage de l'article, contenant un compteur pour le nombre de lettres, de mots, etc. dans l'article. Vous pouvez obtenir la même information en appuyant sur les chiffres de 1 à 5.
- Ajout d'une case à cocher pour désactiver la fenêtre d'avertissement de fermeture lorsqu'il y a des articles ouverts, la case à cocher apparaît dans la même fenêtre.
- La fenêtre d'affichage des tableaux n'affiche plus de lignes vides.
- Les fenêtres du programme peuvent désormais être redimensionnées et déplacées sur l'écran.
- Ajout d'une option dans les paramètres pour restaurer les paramètres par défaut du programme.
- Mise à jour de la version de Python utilisée à Python 3.10 et de wxPython à 4.2.0. Remplacement de Pyinstaller par Cx_Frees.
- Correction d'un bug à cause duquel WikiSearch renvoyait un article différent de celui sélectionné dans les résultats de la recherche.
- Correction d'un bug à cause duquel WikiSearch recherchait dans une langue différente de celle sélectionnée dans la langue de recherche.
- Correction d'un bug à cause duquel la fenêtre d'avertissement de fermeture n'affichait pas correctement le nombre d'articles ouverts.
- Désactivation de l'astuce permettant d'augmenter le nombre de résultats au-delà de 100.
- WikiSearch n'utilise plus Sapi5 pour prononcer certaines actions lorsqu'il est utilisé sans lecteur d'écran.
- Plusieurs améliorations du code ont été apportées, ainsi qu'un certain nombre de petites corrections de bugs ici et là.

#### Note :

- La fonction Imprimer l'article a été ajoutée. Elle devrait fonctionner correctement lorsqu'elle est utilisée à partir de la fenêtre d'affichage de l'article en html. Si vous utilisez le ode d'affichage classique pour lire l'article, nous sommes désolés de vous dire que nous n'avons pas réussi à faire fonctionner cette fonctionnalité de manière optimale pour le moment. Si vous êtes en mesure de contribuer à l'achèvement de cette fonctionnalité, vous pouvez le faire via GitHub.

### Version 1.3 :

Cette version contient quelques corrections de bugs.

- La traduction française s'affiche désormais correctement.
- Correction du problème lié à l'Unicode.
- Correction du bug où le programme ne se lançait pas s'il était installé pour la première fois et n'était pas mis à jour depuis une version précédente.

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
