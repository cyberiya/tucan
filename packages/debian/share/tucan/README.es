===================
 Descripci�n
=========
 
 - Tucan es una aplicaci�n libre y de c�digo abierto dise�ada para la
   gesti�n autom�tica de descargas y subidas en sitios de hosting como:
 
   - http://rapidshare.com/
   - http://megaupload.com/
   - http://gigasize.com/
   - http://mediafire.com/
   - http://4shared.com/
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
       - Acceso an�nimo: Disponible = S�
       - Acceso premium: Disponible = S�
 
    - Subidas: Disponible = Todav�a no
 
 
 - http://megaupload.com/
    - Descargas:
       - Acceso an�nimo: Disponible = S�
       - Acceso premium: Disponible = S�
 
    - Subidas: Disponible = Todav�a no
 
 
 - http://gigasize.com/
    - Descargas:
       - Acceso an�nimo: Disponible = S�
       - Acceso premium: Disponible = No
 
    - Subidas: Disponible = Todav�a no
 
 
 - http://mediafire.com/
    - Descargas:
       - Acceso an�nimo: Disponible = S�
       - Acceso premium: Disponible = No
 
    - Subidas: Disponible = Todav�a no
 
 
 - http://4shared.com/
    - Descargas:
       - Acceso an�nimo: Disponible = S�
       - Acceso premium: Disponible = No
 
    - Subidas: Disponible = Todav�a no
 
 
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
 Instalaci�n y Uso
=========
 
 - Desempaquetar el tarball:
 
   $ tar zxvf tucan-<version>.tar.gz
   $ cd tucan-<version>/
 
 - Instalar Tucan escribiendo (se necesitan privilegios de root):
 
   # make install
 
 - Desinstalar Tucan escribiendo (se necesitan privilegios de root):
 
   # make uninstall
 
 
 - Ejecutar Tucan escribiendo en un terminal:
 
   $ tucan
 
 
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
 Links
=========
 
 - http://tucaneando.wordpress.com/
 - http://cusl3-tucan.forja.rediris.es/
 - https://forja.rediris.es/projects/cusl3-tucan/