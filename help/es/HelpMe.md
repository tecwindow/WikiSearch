# WikiSearch

## Función del programa

Este simple programa permite buscar en Wikipedia, la enciclopedia libre, sin tener que abrir el navegador.

## ¿Qué hay de nuevo?

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

### Versión 1.2:

Esta versión trae nuevas características y además corrige algunos errores.

-  Se ha añadido una traducción al francés. Agradecerle a Riad Assoum por ella.
-  Ahora se puede ajustar el tamaño y color de la fuente mientras se lee el artículo.
-  Se agregó una opción para mostrar un diálogo con las tablas que tenga el artículo. Advertencia: puede que no siempre se muestren correctamente, sino que dependerá del formato del artículo.
-  Se agregó una opción para ver una lista de referencias del artículo para que se puedan abrir en el navegador.
-  Se agregó una opción para mostrar aquellos artículos que están vinculados al artículo mostrado en ese momento. Se puede interactuar con ellos tal como se hace en la ventana de resultados de búsqueda.
-  Añadida una opción para guardar el artículo como un fichero HTML.
- Se agregó la posibilidad de mostrar artículos aleatorios en su idioma según el que se tenga de búsqueda establecido. Puede interactuar con ellos tal como lo hace con la ventana de los resultados de búsqueda.
- Se agregó una opción en los ajustes para ver el artículo en formato HTML (Nota: de momento con errores y poco confiable).
-  Se agregaron métodos de contacto en el menú principal para comunicarse con los desarrolladores.
-  Se cambiaron algunas opciones dentro del menú de acciones de la ventana del artículo que se muestra.
-  El programa se iniciará de manera más rápida si no se verifica la casilla de revisión de actualizaciones automáticas
-  Se corrigió el error por el cual el registro de cambios de una actualización no se mostraba correctamente en el cuadro de diálogo de actualizaciones.
- Cambio de algunos atajos de teclado.
-  Correción de errores menores.

#### Notas:

- Debido a un cambio con ajustes de idioma en esta versión, el idioma del programa volverá automáticamente al inglés después de la actualización. Deberá cambiarlo de nuevo una vez y se guardará automáticamente como antes.
- Todas las nuevas opciones relacionadas con los artículos se pueden encontrar presionando alt y navegando por los menús donde puede encontrar y aprender todas las teclas rápidas.
- Todos los atajos serán escritos en este fichero.

### Versión 1.1:

Todavía estamos aprendiendo y mejorando este software a medida que nosotros mejoramos nuestros conocimientos sobre programación, con lo que hemos podido agregar bastantes funciones en esta versión.

- El programa ahora admite traducciones y usted puede contribuir a traducirlo a su idioma.
- Se han vuelto a revisar las cadenas en inglés y se ha agregado una traducción al árabe, muchas gracias a Riad Assoum.
- Se ha añadido una traducción al español, muchas gracias a Georgiana Frincu.
- Los atajos se mejoraron mucho, cada característica del programa ahora tiene su propia tecla de acceso rápido funcionando.
- El lector de pantalla pronunciará una serie de acciones si se han realizado correctamente.
- El lector de pantalla le notificará cuando el artículo se haya cargado.
- Se puede saltar a cualquier encabezado del artículo mientras se esté leyendo
- Puede personalizar el número de resultados de búsqueda, de momento  hasta 100 (puede cambiar el número desde los ajustes).
- Se puede cerrar la ventana del artículo con la tecla Escape (se puede habilitar la característica en los ajustes).
- El programa le avisará si intenta cerrarlo mientras uno o más artículos estén abiertos (se puede deshabilitar la característica en los ajustes).
- El programa buscará si hay actualizaciones de manera automática al iniciarse (se puede deshabilitar la característica en los ajustes).
- El programa recordará el idioma seleccionado para las futuras búsquedas.


## Agradecimientos

Muchos de nuestros amigos y usuarios han contribuido probando el programa y mandándonos feedback y sugerencias. Sin orden concreto,  nos gustaría dar las gracias a Riad, Ikrami, Mahmoud Shrawy, Muhammad Hajjar, Ahmed Manninah, Moataz Geba, Fawaz Abdul Rahman, Georgiana Frincu, Agustín Aguirre, Angelina, Nacer Baaziz, Abdulla Dubais, Hermina.

## Características 

- Buscar cualquier artículo de manera rápida y eficiente.
- Visualizar el artículo directamente en el programa.
- Ver más de un artículo a la vez en ventanas separadas.
- Guardar artículos como archivos de texto en su ordenador.
- Mientras se lea el artículo, poder cambiar el color y la fuente de éste.
- Un actualizador automático que permite a los usuarios acceder rápidamente a nuevas funciones.

## Notas:

- Seguiremos actualizando el programa de manera constante para añadir nuevas funciones que nos sugieran nuestros usuarios. Es decir, cuantas más veces una característica sea pedida, más rápido se implementará.
- Si desea traducir el programa a su idioma, contáctenos a través de una de las direcciones de correo electrónico en este archivo o nuestras cuentas de Telegram.
- Puede sugerir funciones y comunicar errores a través de GitHub o contactar con nosotros a través de nuestras redes sociales disponibles en el menú principal.
- El software es compatible con Windows 8 y superior con arquitecturas de 32 y 64 bits.

Repositorio GitHub: https://github.com/tecwindow/WikiSearch

## Desarrolladores del programa

- Mahmoud Atef: mahmoud.atef.987123@gmail.com
- Mester Perfect: AhmedBakr593@gmail.com
- Qais Alrefai: ww258148@gmail.com
- TecWindow en Telegram: https://t.me/TecWindow
- a2ztec en Telegram: https://t.me/A2zTecChannel
