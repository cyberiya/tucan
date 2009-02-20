TUCAN FAQ
---------
 
1 - ¿ Qué es Tucan ?
2 - ¿ Qué licencia tiene ?
3 - ¿ Dónde se puede descargar ?
4.1 - ¿ Cómo se instala en Linux ?
4.2 - ¿ Cómo se instala en Windows ?
4.3 - ¿ Cómo se instala en MacOSX ?
5 - ¿ Qúe servicios soporta ?
6 - ¿ Debo activar los servicios antes de descargar ? ¿ qué significa el
    dialogo de términos de servicio ?
7 - ¿ Es necesario comprobar los enlaces antes de añadirlos ?
8 - Tucan arranca pero no me comprueba los enlaces ¿ qué sucede ?
9 - ¿ Por qué al parar un enlace y reiniciarlo este no continua por donde se
     quedo ?
10 - Pulso el botón "Borrar Completos" ¿ por qué no hace nada ?
11 - Pulso el botón "Mover Arriba"/"Mover Abajo" y no se mueve el enlace ¿ qué
     sucede ? 
12 - He activado la casilla salvar sesión al cerrar en las preferencias ¿ por
     qué al abrir no se carga la sesión guardada ?
13 - ¿ Soporta archivos .dlc ?
14 - ¿ Qué pasará con Tucan después del CUSL III ?
15 - ¿ Dónde puedo encontrar más información ?
 
 
1 - ¿ Qué es Tucan ?
--------------------
 - Leer el archivo README (secciónes: Descripción, Características).
 
 
2 - ¿ Qué licencia tiene ?
--------------------------
 - GPLv2 < http://www.gnu.org/licenses/old-licenses/gpl-2.0.html >
 
 
3 - ¿ Dónde se puede descargar ?
--------------------------------
 - Leer el archivo README (sección: Descargas).
 
 
4.1 - ¿ Cómo se instala en Linux ?
----------------------------------
 - Leer el archivo README (sección: Instalación, Dependencias).
 
 
4.2 - ¿ Cómo se instala en Windows ?
------------------------------------
 - Para Windows existe un instalador que incluye todas las dependencias.
   Tucan se debe instalar en el directorio raiz (ejemplo C:\).
 
 
4.3 - ¿ Cómo se instala en MacOSX ?
-----------------------------------
 - Para MacOSX aun no existe soporte nativo, pero se puede usar con XDarwin
   instalando las dependencias, leer el archivo README (sección: Dependencias).
 
 
5 - ¿ Qúe servicios soporta ?
-----------------------------
 - Leer el archivo README (sección: Plugins).
 
 
6 - ¿ Debo activar los servicios antes de descargar ? ¿ qué significa el
    dialogo de términos de servicio ?
------------------------------------------------------------------------
 - Antes de usar un servicio, éste debe estar activado en la pestaña
   "Configuración de Servicio" de la ventana Preferencias.
 
 - Para poder usar Tucan se debe activar al menos un servicio.
 
   Al activar un servicio aparece un diálogo avisando al usuario de que debe
   aceptar los términos de uso de ese servicio, desde ese momento es el
   usuario el que asume la responsabilidad del uso que se hace de ese servicio.
   Para leer los términos de uso se debe ir a la página web de ese servicio:
 
   - http://www.rapidshare.com/agb.html
   - http://www.megaupload.com/terms/
   - http://www.gigasize.com/page.php?p=terms_fs
   - (...)
 
 
7 - ¿ Es necesario comprobar los enlaces antes de añadirlos ?
-------------------------------------------------------------
 - Es imprescindible comprobar los enlaces antes de que puedan usarse. Además
   esta caracteristica es muy útil ya que si se descarga un archivo de varias
   partes se sabe si estan todas antes de comenzar a descargarlas.
 
 
8 - Tucan arranca pero no me comprueba los enlaces ¿ qué sucede ?
-----------------------------------------------------------------
 - Esta situación puede ser debida a varias causas:
   1) Los servicios a los que pertenecen esos enlaces no estan soportados por
      Tucan. Para saber que servicios estan soportados leer el punto 5 de este
      documento.
   2) Los servicios a los que pertenecen esos enlaces no estan activados en las
      preferencias de Tucan. Solución: leer el punto 7 de este documento.
   3) No se han instalado todas las dependencias de Tucan. Solución: leer el
      archivo README (sección: Dependencias).
   4) Si se está usando Tucan en Windows es posible que no esté instalado en el
      directorio raiz. Solución: leer el punto 4.2 de este documento.
 
 
9 - ¿ Por qué al parar un enlace y reiniciarlo este no continua por donde se
     quedo ?
----------------------------------------------------------------------------
 - Tucan aun no soporta pausar las descargas, asi que cada vez que se paren por
   cualquier motivo se vuelven a comenzar desde cero.
 
 
10 - Pulso el botón "Borrar Completos" ¿ por qué no hace nada ?
---------------------------------------------------------------
 - Actualmente Tucan sólo permite limpiar paquetes descargados por completo,
   asi que si el paquete tiene algunos enlaces no descargados es normal que
   no suceda nada.
 
 
11 - Pulso el botón "Mover Arriba"/"Mover Abajo" y no se mueve el enlace ¿ qué
     sucede ?
------------------------------------------------------------------------------
 - Actualmente Tucan sólo permite mover paquetes enteros (no enlaces sueltos),
   pero sólo es algo visual, la prioridad de las descargas no se modifica.
 
 
12 - He activado la casilla salvar sesión al cerrar en las preferencias ¿ por
     qué al abrir no se carga la sesión guardada ?
------------------------------------------------------------------------------
 - El sistema de sesiones aun no esta completo por lo que de momento el usuario
   debe cargar la sesión salvada previamente desde el menú archivo.
 
 
13 - ¿ Soporta archivos .dlc ?
------------------------------
 - El contenedor .dlc es un sistema propietario de la aplicación JDownloader.
   Tucan no pretende (en principio) soportarlo. Además su uso se basa en el
   objetivo de imposibilitar el reporte de enlaces, pero esto es ficticio ya
   que una vez abierto el .dlc con JDownloader (o las aplicaciones que lo
   soporten) los enlaces son visibles y por lo tanto reportables.
 
 
14 - ¿ Qué pasará con Tucan después del CUSL III ?
--------------------------------------------------
 - No se tiene intención de abandonar el desarrollo de Tucan después del
   concurso, es mas, cuando se cumplan los objetivos con los que fué inscrito
   en el concurso (descargas anónimas, descargas premium, subidas...) se tiene
   pensado ampliar las funcionalidades de Tucan (por ejemplo: con un buscador).
 
 
15 - ¿ Dónde puedo encontrar más información ?
----------------------------------------------
 - Leer el archivo README (sección: Links).
 
   También esta el canal #tucan del IRC-Hispano (irc.irc-hispano.org) para
   cualquier duda los usuarios pueden pasar a preguntar.