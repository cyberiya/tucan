=======================================
 Tucan
===================
 
 - Tucan es una aplicación libre y de código abierto diseñada para la
   gestión automática de descargas y subidas en sitios de hosting como:
 
   - http://rapidshare.com/
   - http://megaupload.com/
   - http://gigasize.com/
   - (...)
 
 
===================
 Características
=========
 
 - Escrito enteramente en python.
 - Interfaz gráfica de usuario escrita en PyGTK (GTK+ toolkit).
 - Multiplataforma (GNU/Linux, FreeBSD, Microsoft Windows ...).
 - Fácil de ampliar con plugins.
 - Ligero y rápido.	
 - Gestión de esperas entre descargas (accesos anónimos).
 - Reconocimiento de captchas donde se necesite (como en los accesos anónimos de
   megaupload o gigasize).
 - Gestión de links intercambiables.
 
 
===================
 Plugins
=========
 
 - http://rapidshare.com/
    - Descargas:
       - Acceso Anónimo: Disponible = Sí (captcha = No)
       - Acceso Premium: Disponible = Todavía no
 
    - Subidas: Disponible = Todavía no
 
 
 - http://megaupload.com/
    - Desacargas:
       - Acceso Anónimo: Disponible = Sí (captcha = Sí)
       - Acceso Premium: Disponible = Todavía no
 
    - Subidas: Disponible = Todavía no
 
 
 - http://gigasize.com/
    - Descargas:
       - Acceso Anónimo: Disponible = Sí (captcha = Sí)
       - Acceso Premium: Disponible = No
 
    - Subidas: Disponible = No
 
 
===================
 Tips & Tricks
=========
 
 - Antes de ejecutar una nueva versión, se recomienda eliminar el directorio
   ~/.tucan/ si existe.
 - La primera vez que se ejecuta Tucan (no existe el directorio ~/.tucan/), aparece
   la ventana de Preferencias.
 - Antes de usar un servicio, éste debe estar activado en la pestaña
   "Configuración de Servicio" de la ventana Preferencias.
 
 
 - Acceso anónimo de http://gigasize.com/:
   - gigasize.com no permite comprobar links si ya hay un link descargándose de este
     servicio.
 
 
===================
 Dependencias
=========
 
 - Python >= 2.5
 - PyGTK
 - Python Imaging Library
 - Tesseract OCR con English language pack
 - SVG Rendering Library
 
 --------------------------------------------------------------------------------------------------------
 | Paquete \ Distribución  |  Debian / Ubuntu  |       Gentoo       |     Arch     |       Fedora       |
 --------------------------------------------------------------------------------------------------------
 | Python >= 2.5           | python2.5         | dev-lang/python    | python       | python             |
 --------------------------------------------------------------------------------------------------------
 | PyGTK                   | python-gtk2       | dev-python/pygtk   | pygtk        | pygtk2             |
 --------------------------------------------------------------------------------------------------------
 | Python Imaging Library  | python-imaging    | dev-python/imaging | pil          | python-imaging     |
 --------------------------------------------------------------------------------------------------------
 | Tesseract OCR           | tesseract-ocr     | app-text/tesseract | tesseract    | tesseract          |
 | (english language pack) | tesseract-ocr-eng |    (linguas_en)    |              | tesseract-langpack |
 --------------------------------------------------------------------------------------------------------
 | SVG Rendering Library   | librsvg2-common   | gnome-base/librsvg | librsvg      | librsvg2           |
 --------------------------------------------------------------------------------------------------------
 
 
===================
 Descargas
=========
 
 - Versión de desarrollo (se necesita subversion):
 
   $ svn co https://forja.rediris.es/svn/cusl3-tucan/trunk tucan
 
 
 - Versión estable:
 
   https://forja.rediris.es/projects/cusl3-tucan/ -> Ficheros
 
 
===================
 Instalación
=========
 
 # TODO
 
 
===================
 Uso
=========
 
 - De momento... descomprimir y ejecutar:
 
   $ python tucan.py
 
 
===================
 Links
=========
 
 - http://tucaneando.wordpress.com/
 - http://cusl3-tucan.forja.rediris.es/
 - https://forja.rediris.es/projects/cusl3-tucan/