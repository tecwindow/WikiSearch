# WikiSearch

## Función del programa

Este simple programa permite buscar en Wikipedia, la enciclopedia libre, sin tener que abrir el navegador.

## ¿Qué hay de nuevo?

### Versión 1.4

Esta versión incluye muchas nuevas funcionalidades y corrección de errores.

- Añadidas varias listas de artículos.
    - Se ha añadido la posibilidad de guardar artículos para leerlos sin conexión. Puede guardar el artículo dentro del programa y volver a él en cualquier momento.
    - Se ha añadido la función Artículos favoritos, que permite guardar cualquier artículo en la lista de artículos favoritos para poder volver a él en cualquier momento desde la lista.
    - Se ha añadido una función de Historial, una lista que almacena los artículos que ha visitado y le permite volver a ellos en cualquier momento.
        - La lista de Favoritos y la de Artículos guardados permiten cambiar el nombre del artículo al guardarlo y eliminar los artículos almacenados. Pulse la tecla Aplicaciones sobre cualquier artículo de cualquiera de las dos listas y encontrará las opciones adecuadas. También puede utilizar la tecla Suprimir para borrar artículos o la tecla F2 para renombrarlos.
        - Puede guardar cualquier artículo desde el menú de acciones de la ventana de vista de artículos, y puede acceder a estas listas desde el menú principal de la ventana principal. Cada opción tiene su propio acceso directo.
        - Los datos de los artículos se almacenan en un archivo llamado WikiSearch.db en la carpeta WikiSearch en AppData\Roaming. Puede eliminar una parte específica del contenido del archivo desde los ajustes del programa.

- Se ha añadido una función para detectar enlaces de Wikipedia desde el portapapeles al abrir WikiSearch. Se puede ver el artículo en el programa, abrir en el navegador o ignorar el mensaje. Se puede activar o desactivar esta función en los ajustes del programa.
- Al pegar un enlace de un artículo de Wikipedia en el campo de búsqueda y pulsar Intro, el artículo se mostrará inmediatamente.
- WikiSearch ahora se inicia en el idioma seleccionado durante la instalación.
- Se han realizado algunas mejoras en la ventana de visualización de artículos en la página html. Debido a un cambio en wxPython, el lector de pantalla nvda no puede navegar por la lista de acciones. Para solucionar este problema, vaya a cualquier botón de la ventana y pulse alt, y los menús funcionarán correctamente.
- Se ha añadido la barra de estado a la ventana Ver artículo, que contiene un contador del número de letras, palabras, etc. del artículo. Se Puede obtener la misma información pulsando los números del 1 al 5.
- Añadida una casilla para desactivar la ventana de aviso de cierre cuando hay artículos abiertos, la casilla aparece en la misma ventana.
- La ventana de ver tablas ya no muestra líneas vacías.
- Las ventanas del programa ahora permiten redimensionar y arrastrar en la pantalla.
- Añadida una opción en los ajustes para restaurar el programa a su configuración por defecto.
- Actualizada la versión de Python utilizada a Python 3.10 y wxPython a 4.2.0. Sustituido Pyinstaller por Cx_Frees.
- Corregido un error por el que WikiSearch devolvía un artículo diferente al seleccionado en los resultados de la búsqueda.
- Corregido un error por el que WikiSearch buscaba en un idioma diferente al seleccionado en el idioma de búsqueda.
- Corregido un error por el que la ventana de aviso de cierre no mostraba correctamente el número de artículos abiertos.
- Desactivado el método disponible anteriormente para aumentar el número de resultados por encima de 100.
- WikiSearch ya no utiliza Sapi5 para pronunciar algunas acciones cuando se utiliza sin un lector de pantalla.
- Se han realizado varias mejoras de código, al igual que algunas correcciones de errores por aquí y por allí.

#### Notas

- La funcionalidad de imprimir un artículo ha sido añadida, debería funcionar bien cuando se trata de la ventana de vista de artículo en HTML. Si lo que usted hace es usar la vista clásica nos entristece decirle que no hemos conseguido hacer que la funcionlidad cumpla su función correctamente. Si cree que es capaz de ayudarnos a resolver esta funcionalidad estamos abiertos a sus contribuciones en github.

### Versión 1.3

Esta versión corrige algunos errores:

- La traducción al francés aparecerá correctamente.
- Corregido el problema relacionado con unicode.
- Corregido el error que hacía que el programa no se iniciara si el programa se instalaba por primera vez y no estaba actualizado.

### Versión 1.2

Esta versión trae nuevas características y además corrige algunos errores.

- Se ha añadido una traducción al francés. Agradecerle a Riad Assoum por ella.
- Ahora se puede ajustar el tamaño y color de la fuente mientras se lee el artículo.
- Se agregó una opción para mostrar un diálogo con las tablas que tenga el artículo. Advertencia: puede que no siempre se muestren correctamente, sino que dependerá del formato del artículo.
- Se agregó una opción para ver una lista de referencias del artículo para que se puedan abrir en el navegador.
- Se agregó una opción para mostrar aquellos artículos que están vinculados al artículo mostrado en ese momento. Se puede interactuar con ellos tal como se hace en la ventana de resultados de búsqueda.
- Añadida una opción para guardar el artículo como un fichero HTML.
- Se agregó la posibilidad de mostrar artículos aleatorios en su idioma según el que se tenga de búsqueda establecido. Puede interactuar con ellos tal como lo hace con la ventana de los resultados de búsqueda.
- Se agregó una opción en los ajustes para ver el artículo en formato HTML (Nota: de momento con errores y poco confiable).
- Se agregaron métodos de contacto en el menú principal para comunicarse con los desarrolladores.
- Se cambiaron algunas opciones dentro del menú de acciones de la ventana del artículo que se muestra.
- El programa se iniciará de manera más rápida si no se verifica la casilla de revisión de actualizaciones automáticas
- Se corrigió el error por el cual el registro de cambios de una actualización no se mostraba correctamente en el cuadro de diálogo de actualizaciones.
- Cambio de algunos atajos de teclado.
- Correción de errores menores.

#### Notas

- Debido a un cambio con ajustes de idioma en esta versión, el idioma del programa volverá automáticamente al inglés después de la actualización. Deberá cambiarlo de nuevo una vez y se guardará automáticamente como antes.
- Todas las nuevas opciones relacionadas con los artículos se pueden encontrar presionando alt y navegando por los menús donde puede encontrar y aprender todas las teclas rápidas.
- Todos los atajos serán escritos en este fichero.

### Versión 1.1

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

## Notas

- Seguiremos actualizando el programa de manera constante para añadir nuevas funciones que nos sugieran nuestros usuarios. Es decir, cuantas más veces una característica sea pedida, más rápido se implementará.
- Si desea traducir el programa a su idioma, contáctenos a través de una de las direcciones de correo electrónico en este archivo o nuestras cuentas de Telegram.
- Puede sugerir funciones y comunicar errores a través de GitHub o contactar con nosotros a través de nuestras redes sociales disponibles en el menú principal.
- El software es compatible con Windows 8 y superior con arquitecturas de 32 y 64 bits.

Repositorio GitHub: <https://github.com/tecwindow/WikiSearch>

## Desarrolladores del programa

- Mahmoud Atef: mahmoud.atef.987123@gmail.com
- Mester Perfect: AhmedBakr593@gmail.com
- Qais Alrefai: ww258148@gmail.com
