===================
 Descripción
=========
 
 - Tucan es una aplicación libre y de código abierto diseñada para la
   gestión automática de descargas y subidas en sitios de hosting como:
 
   - http://rapidshare.com/
   - http://megaupload.com/
   - http://gigasize.com/
   - http://mediafire.com/
   - http://4shared.com/
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
 - Reconocimiento de captchas donde se necesite (como los accesos anónimos de
   megaupload o gigasize).
 - Gestión de links intercambiables.
 
 
===================
 Plugins
=========
 
 - http://rapidshare.com/
    - Descargas:
       - Acceso anónimo: Disponible = Sí
       - Acceso premium: Disponible = Sí
 
    - Subidas: Disponible = Todavía no
 
 
 - http://megaupload.com/
    - Descargas:
       - Acceso anónimo: Disponible = Sí
       - Acceso premium: Disponible = Sí
 
    - Subidas: Disponible = Todavía no
 
 
 - http://gigasize.com/
    - Descargas:
       - Acceso anónimo: Disponible = Sí
       - Acceso premium: Disponible = No
 
    - Subidas: Disponible = Todavía no
 
 
 - http://mediafire.com/
    - Descargas:
       - Acceso anónimo: Disponible = Sí
       - Acceso premium: Disponible = No
 
    - Subidas: Disponible = Todavía no
 
 
 - http://4shared.com/
    - Descargas:
       - Acceso anónimo: Disponible = Sí
       - Acceso premium: Disponible = No
 
    - Subidas: Disponible = Todavía no
 
 
===================
 Dependencias
=========
 
 - Python >= 2.5
 - PyGTK
 - Python Imaging Library
 - Tesseract OCR (con el paquete del idioma inglés)
 - SVG Rendering Library
 
 --------------------------------------------------------------------------------
 | Paquete \ Distribución  |  Debian / Ubuntu  |       Gentoo       |   Arch    |
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
 
 - Versión de desarrollo (se necesita subversion):
 
   $ svn co https://forja.rediris.es/svn/cusl3-tucan/trunk tucan
 
 
 - Versión estable:
 
   https://forja.rediris.es/projects/cusl3-tucan/ -> Ficheros
 
 
===================
 Instalación y Uso
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
 
 - Antes de ejecutar una nueva versión, se recomienda eliminar el directorio
   ~/.tucan/ si existe.
 - La primera vez que se ejecuta Tucan (si no existe el directorio ~/.tucan/)
   aparece la ventana de Preferencias.
 - Antes de usar un servicio, éste debe estar activado en la pestaña
   "Configuración de Servicio" de la ventana Preferencias.
 
 - Acceso anónimo de http://gigasize.com/:
   - gigasize.com no permite comprobar links si ya hay un link descargándose de
     este servicio.
 
 
===================
 Links
=========
 
 - http://tucaneando.wordpress.com/
 - http://cusl3-tucan.forja.rediris.es/
 - https://forja.rediris.es/projects/cusl3-tucan/