=======================================
 Tucan
===================
 
 - Tucan es una aplicaci�n libre y de c�digo abierto dise�ada para la
   gesti�n autom�tica de descargas y subidas en sitios de hosting como:
 
   - http://rapidshare.com/
   - http://megaupload.com/
   - http://gigasize.com/
   - (...)
 
 
===================
 Caracter�sticas
=========
 
 - Escrito enteramente en python.
 - Interfaz gr�fica de usuario escrita en PyGTK (GTK+ toolkit).
 - Multiplataforma (GNU/Linux, FreeBSD, Microsoft Windows ...).
 - F�cil de ampliar con plugins.
 - Ligero y r�pido.
 - Gesti�n de esperas entre descargas (accesos an�nimos).
 - Reconocimiento de captchas donde se necesite (como los accesos an�nimos de
   megaupload o gigasize).
 - Gesti�n de links intercambiables.
 
 
===================
 Plugins
=========
 
 - http://rapidshare.com/
    - Descargas:
       - Acceso An�nimo: Disponible = S� (captcha = No)
       - Acceso Premium: Disponible = Todav�a no
 
    - Subidas: Disponible = Todav�a no
 
 
 - http://megaupload.com/
    - Desacargas:
       - Acceso An�nimo: Disponible = S� (captcha = S�)
       - Acceso Premium: Disponible = Todav�a no
 
    - Subidas: Disponible = Todav�a no
 
 
 - http://gigasize.com/
    - Descargas:
       - Acceso An�nimo: Disponible = S� (captcha = S�)
       - Acceso Premium: Disponible = No
 
    - Subidas: Disponible = No
 
 
===================
 Tips & Tricks
=========
 
 - Antes de ejecutar una nueva versi�n, se recomienda eliminar el directorio
   ~/.tucan/ si existe.
 - La primera vez que se ejecuta Tucan (si no existe el directorio ~/.tucan/)
   aparece la ventana de Preferencias.
 - Antes de usar un servicio, �ste debe estar activado en la pesta�a
   "Configuraci�n de Servicio" de la ventana Preferencias.
 
 
 - Acceso an�nimo de http://gigasize.com/:
   - gigasize.com no permite comprobar links si ya hay un link descarg�ndose de
     este servicio.
 
 
===================
 Dependencias
=========
 
 - Python >= 2.5
 - PyGTK
 - Python Imaging Library
 - Tesseract OCR (con el paquete del idioma ingl�s)
 - SVG Rendering Library
 
 --------------------------------------------------------------------------------
 | Paquete \ Distribuci�n  |  Debian / Ubuntu  |       Gentoo       |   Arch    |
 --------------------------------------------------------------------------------
 | Python >= 2.5           | python2.5         | dev-lang/python    | python    |
 --------------------------------------------------------------------------------
 | PyGTK                   | python-gtk2       | dev-python/pygtk   | pygtk     |
 --------------------------------------------------------------------------------
 | Python Imaging Library  | python-imaging    | dev-python/imaging | pil       |
 --------------------------------------------------------------------------------
 | Tesseract OCR           | tesseract-ocr     | app-text/tesseract | tesseract |
 | (english language pack) | tesseract-ocr-eng |    (linguas_en)    |           |
 --------------------------------------------------------------------------------
 | SVG Rendering Library   | librsvg2-common   | gnome-base/librsvg | librsvg   |
 --------------------------------------------------------------------------------
 
 ---------------------------------------
 |       Fedora       |    OpenSuSE    |
 ---------------------------------------
 | python             | python         |
 ---------------------------------------
 | pygtk2             | python-gtk     |
 ---------------------------------------
 | python-imaging     | python-imaging |
 ---------------------------------------
 | tesseract          | tesseract      |
 | tesseract-langpack |                |
 ---------------------------------------
 | librsvg2           | librsvg        |
 ---------------------------------------
 
 
===================
 Descargas
=========
 
 - Versi�n de desarrollo (se necesita subversion):
 
   $ svn co https://forja.rediris.es/svn/cusl3-tucan/trunk tucan
 
 
 - Versi�n estable:
 
   https://forja.rediris.es/projects/cusl3-tucan/ -> Ficheros
 
 
===================
 Instalaci�n
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