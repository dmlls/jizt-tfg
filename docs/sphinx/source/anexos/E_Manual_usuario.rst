..
    Copyright (C) 2020-2021 Diego Miguel Lozano <jizt@diegomiguel.me>
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the section entitled "GNU
    Free Documentation License"...
    
.. _apendix:manual-usuario:

========================
Documentación de usuario
========================


Introducción
============

En esta sección se recogen los requisitos que requiere nuestra
aplicación, así como los detalles para la instalación y uso de la misma
por el usuario final\ [1]_.

Requisitos de usuarios
======================

Para la versión **Android**, se deben cumplir los siguientes requisitos:

-  Mínimo 18 MB de espacio de almacenamiento libre. El paquete de instalación tiene un
   tamaño de 6,3 MB, y una vez instalada ocupa 16,36 MB. No obstante, ese tamaño
   aumentará ligeramente según se vayan almacenando resúmenes.

-  Versión de Android igual o superior a la 4.1 (*JellyBean* - API 16).

En el caso de **iOS**:

-  Mínimo 20 MB de espacio de almacenamiento libre. En este caso, el peso del paquete
   es de 6,9 MB, y una vez instalada ocupa 17,2 MB.

-  Versión de iOS 8 o superior.

Y en el caso de la versión **web**:

-  Los navegadores *web* soportados son Google Chrome, Mozilla Firefox,
   Safari o Edge.

En todos los casos se requiere conexión a Internet para generar nuevos
resúmenes (los resúmenes ya generados se pueden consultar *offline*). La
*app* de JIZT no requiere de permisos adicionales en ninguna de las
plataformas.

La aplicación solo está disponible por el momento en inglés, dado que
este es el único lenguaje soportado actualmente por el servicio de
generación de resúmenes.

Instalación
===========

En esta sección detallamos el proceso de instalación en las diferentes
plataformas.

Android
-------

Instalación recomendada
~~~~~~~~~~~~~~~~~~~~~~~

Se recomienda que el usuario instale la aplicación desde Google Play.

Para ello, simplemente basta con buscar la aplicación "JIZT AI Summarization" y
pulsar en "Instalar".

.. figure:: ../_static/images/memoria_y_anexos/jizt-google-play.png
   :alt: Instalar JIZT desde Google Play.
   :width: 70%
   :align: center

   Instalar JIZT desde Google Play.

iOS
---

Por el momento, la aplicación no ha sido publicada en la App Store, e
iOS no proporciona ninguna manera oficial para la instalación de
aplicaciones desde fichero\ [2]_.

Por tanto, se recomienda a los usuarios que accedan desde su navegador
móvil a la versión *web* de JIZT (ver siguiente sección).

*Web*
-----

Se puede acceder a la aplicación directamente a través de
`app.jizt.it <https://app.jizt.it>`__, sin ser necesario realizar
ninguna instalación.

Manual del usuario
==================

Una vez instalada la aplicación, el usuario está en disposición de
comenzar a utilizarla. El funcionamiento en interfaz de la aplicación en
las diferentes plataformas es homogéneo, por lo que todo lo explicado a
continuación es válido para cualquiera de ellas.

TODO: añadir capturas de la app.

Generar un nuevo resumen
------------------------

La generación de resúmenes se trata de una de las funciones principales
de la aplicación.

Los pasos que debemos seguir para generar un nuevo resumen son los
siguientes:

#. En la pantalla de inicio, pulsar sobre el campo de texto central, el
   cual contiene escrito "*Type or paste your text*" (en español,
   "Escribe o pega tu texto").

#. Escribir el texto o pulsar en el icono de la esquina superior
   derecha, el sirve para pegar el texto desde el portapapeles.

#. Pulsar en "*Summarize*" ("resumir").

#. Se mostrará una barra que simboliza que el resumen está siendo
   generado.

#. Una vez completado el resumen, se mostrará una nueva pantalla con el
   resumen.

Ver todos los resúmenes generados
---------------------------------

La aplicación muestra en la pantalla principal una vista previa de los
últimos resúmenes generados en forma de lista deslizable. Pulsando sobre
cualquiera de ellos, se accede a los detalles del mismo.

Si se quieren ver todos los resúmenes, se puede pulsar en "*See all*"
("ver todos"). Se mostrará una nueva pantalla en la que aparece una
lista con todos los resúmenes, ordenados temporalmente de más recientes
a más antiguos. Se puede pulsar sobre cualquiera de ellos para obtener
más detalles.

.. _subsection:borrar:

Borrar un resumen
-----------------

Para borrar un resumen, se puede pulsar en el símbolo que aparece en la
esquina superior derecha en la pantalla de "*Summary*" (resumen).

Se puede acceder a esta pantalla de tres formas diferentes:

#. Tras generar un resumen, se muestra dicha pantalla por defecto.

#. Haciendo *click* en cualquiera de los resúmenes que aparecen en la
   parte inferior de la pantalla principal.

#. Pulsando en "*See all*" ("ver todos") y haciendo *click* en
   cualquiera de los resúmenes.

Copiar un resumen
-----------------

Para copiar un resumen, se debe estar en la pantalla de "*Summary*"
(resumen). Para acceder a esta pantalla, seguir cualquiera de las
alternativas listadas en la sección .

Una vez en esta pantalla, se debe pulsar en el siguiente icono:

Tras pulsar dicho icono, el texto se habrá copiado al portapapeles de
nuestro dispositivo.

Compartir un resumen
--------------------

Para copiar un resumen, se debe estar en la pantalla de "*Summary*"
(resumen). Para acceder a esta pantalla, seguir cualquiera de las
alternativas listadas en la sección .

Una vez en esta pantalla, se debe pulsar en el siguiente icono:

A continuación, se mostrará una lista de aplicaciones a través de las
cuales se puede compartir el resumen.

Ver el texto a partir del cual se generó un resumen
---------------------------------------------------

Para ver el texto original de un resumen, se debe estar en la pantalla
de "*Summary*" (resumen). Para acceder a esta pantalla, seguir
cualquiera de las alternativas listadas en la sección .

Una vez en dicha pantalla, se debe pulsar sobre "*Original*".

Obtener más información acerca de un resumen
--------------------------------------------

Para obtener más información de un resumen, se debe estar en la pantalla
de "*Summary*" (resumen). Para acceder a esta pantalla, seguir
cualquiera de las alternativas listadas en la sección .

Una vez en dicha pantalla, se debe pulsar sobre "*More info*" ("Más
información").

Generar un resumen a partir de un documento
-------------------------------------------

Por el momento, esta opción no está disponible. No obstante, pronto será
implementada.

Generar un resumen a partir de una imagen
-----------------------------------------

Por el momento, esta opción no está disponible. No obstante, pronto será
implementada.

.. [1]
   Por ahora, no se incluyen los detalles referentes a la versión de
   escritorio, dado que el soporte de Flutter para estas plataformas
   está aún en fase *alfa* [flutter-desktop]_.

.. [2]
   Como aclaración al margen de Manual de Usuario, la aplicación no ha
   sido publicada en la App Store por su elevado precio (99$ al año por
   la cuenta de desarrollador, frente a los 25$ de por vida, en el caso
   de Play Store).
