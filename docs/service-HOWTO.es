TUCAN SERVICE HOWTO
-------------------

Indice:
 1 - Introducci�n
 2 - Breve Resumen
 3 - Secciones
 3.1 - Directorio de servicio (obligatorio)
 3.2 - Archivo __init__.py (obligatorio)
 3.3 - Archivo service.conf (obligatorio)
 3.4 - Archivo imagen o icono (opcional)
 3.5 - Archivo check_links.py (opcional)
 3.6 - Archivo anonymous_download.py (opcional)
 3.7 - Archivo premium.accounts (opcional)
 3.8 - Archivo premium_downloads.py (opcional)
 3.9 - Archivo premium_cookie.py (opcional)


1 - Introducci�n
----------------
En este documento se van a explicar las lineas generales para implementar un
nuevo servicio para Tucan (archivos m�nimos, ubicaci�n de esos archivos, 
formato, par�metros de entrada/salida... etc).


2 - Breve Resumen
-----------------
servicio/             : obligatorio: Directorio que contiene todos los
                                     archivos del servicio, no puede contener
                                     ning�n punto "." en el nombre.

__init__.py           : obligatorio: Necesario para que python reconozca el
                                     directorio como m�dulo.

service.conf          : obligatorio: Descripci�n e informaci�n del servicio
                                     para que el sistema de plugins sepa que
                                     soporta el plugin de este servicio.

<imagen o icono>      : opcional: Imagen o icono de tama�o 48x48 pixels
                                  representativo del servicio.

check_links.py        : opcional: S�lo necesario si el servicio tiene soporte
                                  para descargas. Puede ser un archivo o puede
                                  ser un metodo de un plugin de descarga.

anonymous_download.py : opcional: S�lo necesario si el servicio tiene soporte
                                  para descargas an�nimas.

premium.accounts      : opcional: S�lo necesario si el servicio tiene soporte
                                  para cuentas premium (se genera desde el GUI).

premium_download.py   : opcional: S�lo necesario si el servicio tiene soporte
                                  para descargas premium.

premium_cookie.py     : opcional: S�lo necesario si el servicio tiene soporte
                                  para descargas premium.

3 - Secciones
-------------

3.1 - Directorio de Servicio (obligatorio)
------------------------------------------
El directorio contendr� todos los archivos de los diferentes plugins del
servicio, no debe contener ning�n punto "." en el nombre. Ejemplos:

   http://rapidshare.com  ->  rapidshare/
   http://megaupload.com  ->  megaupload/
   http://gigasize.com    ->  gigasize/
   http://foobar.com      ->  foobar/


3.2 - Archivo __init__.py (obligatorio)
---------------------------------------
Este archivo es necesario para que python reconozca el directorio como m�dulo.
Es un archivo vacio.


3.3 - Archivo service.conf (obligatorio)
----------------------------------------
Este archivo describe y da informaci�n de los distintos plugins al sistema de 
plugins de Tucan para que conozca las funcionalidades del servicio.

Consta de varias secciones:

   [main]
   enabled = False
   name = rapidshare.com
   icon = rapidshare.png
   premium_cookie = PremiumCookie
   downloads = True
   uploads = False
   update = 0

   [anonymous_download]
   name = AnonymousDownload
   author = Crak
   captcha = True
   version = 0.1
   slots = 1

   [premium_download]
   name = PremiumDownload
   author = Crak
   version = 0.2
   accounts = premium.accounts


Secci�n [main]:
"enabled"        : Opci�n para notificar que el servicio esta activado o
                   desactivado. Valores: True, False. Por defecto estar�
                   desactivado (False).
"name"           : Opci�n para notificar el nombre del servicio.
                   Ejemplos: rapidshare.com, megaupload.com, gigasize.com
"icon"           : Opci�n para notificar el nombre del icono o imagen
                   representativa del servicio que se va a usar en el GUI.
                   Opcional: si no se va a usar se debe poner None.
"downloads"      : Opci�n para notificar que el servicio puede realizar
                   descargas. Valores: True, False.
"premium_cookie" : Opci�n para notificar el nombre de la clase que se va a
                   usar para gestionar la cookie necesaria en las cuentas
                   premium.
"uploads"        : Opci�n para notificar que el servicio puede realizar
                   subidas. Valores: True, False.
"update"	 : Opcion para la actualizacion automatica del servicio, ser� un 
		   numero a incrementar cuando se quiera actualizar el servicio.
		   Valores: int.


Secci�n [anonymous_download]:
"name"    : Opci�n para notificar el nombre de la clase que se va a usar para
            realizar este tipo de acceso.
            Valor por defecto: AnonymousDownload.
"author"  : Opci�n para notificar el nombre (o nick o email) del creador.
"captcha" : Opci�n para notificar si el servicio tiene captcha en las
            descargas an�nimas.
            Valores: True, False.
"version" : Versi�n del plugin.
"slots"   : N�mero m�ximo de descargas an�nimas simultaneas permitidas por
            este servicio.


Secci�n [premium_download]:
"name"     : Opci�n para notificar el nombre de la clase que se va a usar para
             realizar este tipo de acceso.
             Valor por defecto: PremiumDownload.
"author"   : Opci�n para notificar el nombre (o nick o email) del creador.
"version"  : Versi�n del plugin.
"accounts" : Nombre del archivo donde se van a almacenar los datos de las
             cuentas premium de este servicio.


3.4 - Archivo imagen o icono (opcional)
---------------------------------------
Imagen o icono de tama�o 48x48 pixels representativo del servicio que se va a
usar en el GUI.
Si no se va a usar se debe notificar en el archivo service.conf, secci�n [main]
opci�n "icon = None".


3.5 - Archivo check_links.py (opcional)
---------------------------------------
Este archivo s�lo es necesario si el servicio tiene soporte para descargas.
Puede ser un archivo si lo usan varios plugins (descargas an�nimas, 
descargas premium) o puede ser un metodo de los distintos plugins de descarga.

par�metros de entrada: url.
par�metros de salida: nombre del archivo a descargar, tama�o y unidades.

    comprobaciones/tareas m�nimas:
        url activa
        determinar nombre del archivo y tama�o total.


3.6 - Archivo anonymous_download.py (opcional)
----------------------------------------------
Este archivo s�lo es necesario si el servicio tiene soporte para descargas
an�nimas. Plugin t�pico.

clases: AnonymousDownload (declarada en el archivo service.conf, secci�n
                          [anonymous_download])
m�todos:
  __init__: inicializaci�n de slots.py y download_plugin.py
  add: par�metros de entrada: ruta, link y nombre del archivo
  delete: par�metros de entrada: nombre del archivo.
  check_links: par�metros de entrada: url. par�metros de salida: nombre del 
  archivo a descargar, tama�o y unidades.


3.7 - Archivo premium.accounts (opcional)
-----------------------------------------
Este archivo s�lo es necesario si el servicio tiene soporte para cuentas premium.
Se genera desde el GUI (preferencias) y esta cifrado.


3.8 - Archivo premium_downloads.py (opcional)
---------------------------------------------
Este archivo s�lo es necesario si el servicio tiene soporte para descargas
Premium. Plugin t�pico.

clases: PremiumDownload (declarada en el archivo service.conf, secci�n
                          [premium_download])
m�todos:
  __init__: inicializaci�n de accounts.py
  add: par�metros de entrada: ruta, link y nombre del archivo
  delete: par�metros de entrada: nombre del archivo
  check_links: par�metros de entrada: url. par�metros de salida: nombre del 
  archivo a descargar, tama�o y unidades.


3.9 - Archivo premium_cookie.py (opcional)
------------------------------------------
Este archivo s�lo es necesario si el servicio tiene soporte para cuentas
Premium.

clases: PremiumCookie (declarada en el archivo service.conf, secci�n
                          [main])
m�todos:
  get_cookie: par�metros de entrada: user, password url. 
  par�metros de salida: cookie (cookielib.CookieJar).
