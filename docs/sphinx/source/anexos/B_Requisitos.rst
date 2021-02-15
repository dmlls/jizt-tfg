..
    Copyright (C) 2020-2021 Diego Miguel Lozano <jizt@diegomiguel.me>
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the section entitled "GNU
    Free Documentation License".

.. _apendix:requisitos:

============================
Especificación de Requisitos
============================

Introducción
============

En este apéndice se recoge una descripción del sistema *software* a
desarrollar. Más concretamente, se presentan aspectos como el propósito,
alcance y objetivos generales del mismo, así como los requisitos
específicos que el sistema debe implementar.

La forma en la que hemos organizado la Especificación está basada
parcialmente en las recomendaciones del estándar IEEE 830-1998,
considerado como la principal referencia para la aplicación de buenas
prácticas en la escritura del Documento de Especificación de Requistios
(SRS).

Propósito
---------

El propósito de la presente Especificación de Requisitos tiene como
objetivo ofrecer una descripción detallada del sistema *software*
desarrollado.

Este documento está orientado principalmente al equipo de desarrollo del
proyecto, pero queda también a libre disposición de cualquier persona
que pudiera estar interesada.

Alcance
-------

El sistema *software* a desarrollar recibirá el nombre de JIZT. El
objetivo y funcionalidad principal de JIZT será la generación de
resúmenes abstractivos en la nube. Dicho sistema estará orientado tanto
a usuarios con conocimientos de informática básicos, así como usuarios
con experiencia en el campo.

Para los primeros, es decir, usuarios con conocimientos básicos, se
ofrecerá una aplicación multiplataforma desarrollada con la usabilidad
en mente.

Para aquellos usuarios más avanzados, además de la aplicación, se
proporcionará una API REST, permitiéndoles realizar peticiones
directamente, e incluso desarrollar sus propias aplicaciones que
consuman dicha API.

Se pondrá especial atención en el desarrollo de una documentación
completa, accesible y de fácil comprensión. Esta documentación recogerá
tanto los aspectos técnicos de la aplicación y la API REST, así como
manuales de uso para el usuario y para el desarrollador.

Definiciones, siglas, y abreviaciones
-------------------------------------

A continuación se recogen las definiciones, siglas y abreviaciones más
relevantes para el proyecto:

-  **NLP**: Procesamiento de Lenguaje Natural (*Natural Language
   Processing*).

-  **Resumen extractivo**: aquel resumen generado a partir de la
   *extracción* de las frases del texto consideradas más relevantes. Es
   decir, este tipo de resúmenes contienen únicamente frases tomadas
   literalmente del texto original.

-  **Resumen abstractivo**: aquel resumen que incluye palabras o
   expresiones que no aparecen en el texto original.

-  **API REST**: servicio *web* que proporciona una serie de *endpoints*
   para llevar a cabo operaciones HTTP (métodos), que proporcionan
   acceso para crear, recuperar, actualizar o eliminar los recursos del
   servicio.

-  **Endpoint**: punto de entrada en un canal de comunicación cuando dos
   sistemas interactúan. En una API REST los *endpoints* son
   generalmente URLs.

-  **HTTP**: *Hypertext Transfer Protocol*, protocolo para sistemas de
   información distribuidos, colaborativos e hipermedia. Este protocolo
   es la base de la comunicación de datos para la World Wide Web (WWW).

-  **URL**: *Uniform Resource Locator*, referencia a un recurso web que
   especifica su ubicación en una red informática y un mecanismo para
   recuperarlo.

-  **Frontend**: la infraestructura *frontend* incluye todos aquellos
   elementos del sistema con los que el usuario final interactúa.

-  **Backend**:parte de la infraestructura que contiene el conjunto de
   servidores, bases de datos, APIs y los sistemas operativos que
   alimentan el *frontend* de una aplicación.

Descripción global
==================

Objetivos generales
-------------------

Los principales objetivos del sistema *software* a desarrollar son los
siguientes:

-  Implementar un servicio de generación de resúmenes abstractivos en la
   nube, empleando modelos pre-entrenados del estado del arte.

-  Implementar el *backend* que haga posible esta generación de
   resúmenes, así como una API REST para exponer el *backend*.

-  Diseñar la arquitectura del *backend* con aspectos como la
   flexibilidad, la escalabilidad y la alta disponibilidad como pilares
   fundamentales.

-  Implementar un *frontend* (aplicación multiplataforma) que consuma la
   REST API y dé la posibilidad de generar resúmenes a cualquier
   usuario.

-  Implementar una interfaz (tanto en el *backend* como en el *fontend*)
   que permita a los usuarios especificar los parámetros con los que el
   resumen será generado, como por ejemplo, su longitud relativa al
   texto original.

Características del usuario
---------------------------

Los usuarios potenciales de JIZT se pueden dividir en dos categorías
fundamentales:

-  Estudiantes de edades comprendidas entre los 15 y 25 años. El uso
   principal que harán del producto será el resumen de textos
   académicos.

-  Personas de edades comprendidas entre los 25 y 50 años, cuyo
   principal uso será el resumen de noticias y artículos periodísticos.

En cuanto al sexo, el uso por parte tanto de hombres como mujeres será
aproximadamente equivalente.

Un tercer tipo de usuario, no incluido anteriormente, serían partidos
interesados en el uso del producto, como empresas o particulares, que
fueran a hacer un uso extensivo y exhaustivo del mismo. Este tipo de
usuario requiere unas prestaciones más exigentes, pudiendo llegar a
solicitar el despliegue de JIZT en sus propias dependencias.

Es por ello que el producto desarrollado deberá ser lo más independiente
del entorno en el que se despliegue como sea posible.

Catalogo de requisitos
======================

A continuación se detallan los requisitos funcionales y no funcionales
del producto a desarrollar. Estos requisitos son globales al proyecto y,
por tanto, involucran tanto al *backend* como a la aplicación a
desarrollar.

Requisitos funcionales
----------------------

-  **RF-1 Solicitar resumen**: la API REST debe proporcionar un
   *endpoint* para que el usuario pueda solicitar un resumen de un
   texto.

   -  **RF-1.1 Elegir modelo de generación de resumen**: el usuario
      deberá ser capaz de especificar el modelo de generar su
      resumen\ [1]_.

   -  **RF-1.2 Especificar longitud relativa del resumen**: el usuario
      deberá ser capaz de especificar la longitud del resumen generado,
      de manera relativa al texto original.

   -  **RF-1.3 Especificar parámetros del resumen**: el usuario deberá
      ser capaz de especificar los parámetros concretos con los que se
      generará su resumen\ [2]_.

-  **RF-2 Historial de resúmenes**: el usuario podrá acceder a los
   resúmenes que ha generado recientemente.

-  **RF-3 Compartir resumen**: se le brindará al usuario la opción de
   compartir el resumen generado a través de otra aplicación a su
   elección.

-  **RF-4 Copiar resumen**: se le brindará al usuario la opción de
   copiar el resumen generado.

-  **RF-5 Borrar resumen**: el usuario deberá ser capaz de borrar
   permanentemente un resumen previamente generado.

-  **RF-6 Pegar desde el portapapeles**: la aplicación ofrecerá una
   opción para que el usuario pueda pegar el texto a resumir desde el
   portapapeles de forma sencilla.

-  **RF-7 Mostrar metadatos**: el sistema brindará al usuario los
   metadatos relativos al resumen generado, como la hora a la que fue
   creado.

-  **RF-8 Pre-procesado del texto**: el sistema será capaz de recibir
   texto con errores de formateo (exceso de espacios, saltos de carro
   situados en mitad de una frase, etc.), así como caracteres
   <<extraños>>. Independientemente de lo anterior, el resumen generado
   aparecerá correctamente formateado y sin los mencionados caracteres.

-  **RF-9 Textos arbitrariamente largos**: el sistema será capaz de
   producir resúmenes de cualquier texto, independientemente de la
   longitud de los mismos. No se espera, no obstante, que el tiempo de
   resumen de textos extremadamente largos esté por debajo del orden del
   minuto.

Requisitos no funcionales
-------------------------

-  **RNF-1 Escalabilidad**: la arquitectura del sistema deberá permitir
   el escalado del mismo de forma rápida y sencilla.

   -  **RNF-1.1 Autoescalado**: el sistema podrá escalarse de manera
      automática en momentos en los que la carga de trabajo así lo
      requiera. Del mismo modo, cuando dicha carga remita, deberá
      disminuir su escala, a fin de consumir los mínimos recursos
      posibles.

-  **RNF-2 Alta disponibilidad**: el sistema deberá garantizar el acceso
   al mismo por parte de los usuarios en el 99,99 % de los casos.

   -  **RNF-2.1 Tolerancia frente a fallos**: el sistema deberá ser
      capaz de recuperarse de forma automática de posibles errores o
      problemas de funcionamiento de cualquiera de sus componentes en un
      tiempo menor a los 2 minutos.

-  **RNF-3 Eficiencia**: el sistema deberá ser capaz de generar un
   elevado número de resúmenes provenientes de diferentes usuarios de
   forma simultánea, sin que el tiempo medio de resumen se vea afectado.

-  **RNF-4 Seguridad lógica y de datos**: se debe garantizar la correcta
   protección de todos los datos manejados por el sistema.

-  **RNF-5 Privacidad**: se debe asegurar la protección de los datos de
   carácter personal.

   -  **RNF-5.1 Anonimidad**: en ningún caso se recopilará información
      de los usuarios que permita determinar la identidad de los mismos.
      No obstante, el sistema no es responsable de garantizar que los
      textos introducidos no contienen información de carácter personal.

-  **RNF-6 Usabilidad**: el tiempo medio de aprendizaje de la aplicación
   por parte de los usuarios deberá ser inferior a los 5 minutos.
   Además, el sistema contará con documentación en línea detallada del
   producto.

-  **RNF-7 Multiplataforma**: se distribuirán los binarios de la
   aplicación necesarios para su ejecución en móvil (Android e iOS),
   *web* (Google Chrome, Mozilla Firefox, Safari y Microsoft Edge), y
   escritorio (Linux, Apple y Windows).

-  **RNF-8 Tamaño reducido**: el peso de la aplicación no debe superar
   los 30 MB.

Especificación de requisitos
============================

En esta sección, nos centramos en la definición de los casos de uso de
nuestro producto.

Dado que el usuario interactuará únicamente con la aplicación
(*frontend*), el *backend* no se considera en este caso, aunque sigue
siendo vital para que los casos de uso de la aplicación se puedan
completar con éxito.

Diagrama de casos de uso
------------------------

.. figure:: ../_static/images/memoria_y_anexos/use-case-diagram.png
   :alt: Diagrama de casos de uso.
   :name: flutter-widgets-2

   Diagrama de casos de uso.

Actores
-------

Existe un único actor: el usuario que hace uso de la aplicación.

Casos de uso
------------

.. table:: CU-01 Solicitar resumen

   +---------------+-------------------------------------------------------------------------------------------------+
   | **CU-01**     | **Solicitar resumen**                                                                           |
   +===============+=================================================================================================+
   | Descripción   | Solicitar la generación de un resumen a partir de un texto.                                     |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Autor         | Diego Miguel Lozano                                                                             |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Requisitos    | RF-1, RF-6, RF-8, RF-9                                                                          |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Precondición  | La API REST se encuentra accesible.                                                             |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Flujo normal  | | 1. El usuario inicia la aplicación.                                                           |
   |               | | 2. El usuario hace *click* en el área de texto.                                               |
   |               | | 3. El usuario introduce el texto a resumir o, alternativamente lo pega desde el portapapeles. |
   |               | | 4. El usuario pulsa en el botón «*Summarize*».                                                |
   |               | | 5. Se muestra un indicador de «procesando».                                                   |
   |               | | 6. Se muestra un indicador de «resumen completado».                                           |
   |               | | 7. Se muestra el resumen generado.                                                            |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Postcondición | El usuario ha obtenido el resumen de su texto.                                                  |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Excepciones   | API REST inaccesible.                                                                           |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Incluye       | \-                                                                                              |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Extiende      | \-                                                                                              |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Prioridad     | Muy alta.                                                                                       |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Frecuencia    | Muy alta.                                                                                       |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Importancia   | Crítica                                                                                         |
   +---------------+-------------------------------------------------------------------------------------------------+
   | Comentarios   | \-                                                                                              |
   +---------------+-------------------------------------------------------------------------------------------------+

.. table:: CU-02 Establecer longitud relativa mínima del resumen

   +---------------+------------------------------------------------------------------------------------------------------------------+
   | **CU-02**     | **Establecer longitud relativa mínima del resumen**                                                              |
   +===============+==================================================================================================================+
   | Descripción   | | Establecer la longitud mínima que puede tener el resumen                                                       |
   |               | | generado de manera relativa al texto original.                                                                 |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Autor         | Diego Miguel Lozano                                                                                              |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Requisitos    | RF-1.2                                                                                                           |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Precondición  | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Flujo normal  | | 1. El usuario pulsa sobre el cuadro de texto en la pantalla principal.                                         |
   |               | | 2. El usuario ajusta la longitud mínima a través del *slider* que aparece en la parte inferior de la pantalla. |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Postcondición | Se ha establecido la longitud mínima.                                                                            |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Excepciones   | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Incluye       | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Extiende      | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Prioridad     | Alta.                                                                                                            |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Frecuencia    | Alta.                                                                                                            |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Importancia   | Alta.                                                                                                            |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Comentarios   | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+

.. table:: CU-03 Establecer longitud relativa máxima del resumen

   +---------------+------------------------------------------------------------------------------------------------------------------+
   | **CU-03**     | **Establecer longitud relativa máxima del resumen**                                                              |
   +===============+==================================================================================================================+
   | Descripción   | | Establecer la longitud máxima que puede tener el resumen                                                       |
   |               | | generado de manera relativa al texto original.                                                                 |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Autor         | Diego Miguel Lozano                                                                                              |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Requisitos    | RF-1.2                                                                                                           |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Precondición  | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Flujo normal  | | 1. El usuario pulsa sobre el cuadro de texto en la pantalla principal.                                         |
   |               | | 2. El usuario ajusta la longitud máxima a través del *slider* que aparece en la parte inferior de la pantalla. |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Postcondición | Se ha establecido la longitud máxima.                                                                            |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Excepciones   | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Incluye       | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Extiende      | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Prioridad     | Alta.                                                                                                            |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Frecuencia    | Alta.                                                                                                            |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Importancia   | Alta.                                                                                                            |
   +---------------+------------------------------------------------------------------------------------------------------------------+
   | Comentarios   | \-                                                                                                               |
   +---------------+------------------------------------------------------------------------------------------------------------------+

.. table:: CU-04 Consultar historial de resúmenes

   +---------------+----------------------------------------------------------------------+
   | **CU-04**     | **Consultar historial de resúmenes**                                 |
   +===============+======================================================================+
   | Descripción   | Visualizar la lista de resúmenes generados previamente.              |
   +---------------+----------------------------------------------------------------------+
   | Autor         | Diego Miguel Lozano                                                  |
   +---------------+----------------------------------------------------------------------+
   | Requisitos    | RF-2, RF-3, RF-4, RF-5, RF-7                                         |
   +---------------+----------------------------------------------------------------------+
   | Precondición  | Haber generado al menos un resumen previamente.                      |
   +---------------+----------------------------------------------------------------------+
   | Flujo normal  | | 1. El usuario pulsa en «*See all*» en la pantalla principal.       |
   |               | | 2. Se muestra la lista de resúmenes previos.                       |
   +---------------+----------------------------------------------------------------------+
   | Postcondición | Se visualizan los resúmenes generados.                               |
   +---------------+----------------------------------------------------------------------+
   | Excepciones   | \-                                                                   |
   +---------------+----------------------------------------------------------------------+
   | Incluye       | \-                                                                   |
   +---------------+----------------------------------------------------------------------+
   | Extiende      | CU-07                                                                |
   +---------------+----------------------------------------------------------------------+
   | Prioridad     | Alta.                                                                |
   +---------------+----------------------------------------------------------------------+
   | Frecuencia    | Alta.                                                                |
   +---------------+----------------------------------------------------------------------+
   | Importancia   | Alta.                                                                |
   +---------------+----------------------------------------------------------------------+
   | Comentarios   | Si aún no se ha generado ningún resumen, la lista se mostrará vacía. |
   +---------------+----------------------------------------------------------------------+

.. table:: CU-05 Consultar resumen

   +---------------+-------------------------------------------------------------------------------------------+
   | **CU-05**     | **Consultar resumen**                                                                     |
   +===============+===========================================================================================+
   | Descripción   | Consultar un resumen generado previamente.                                                |
   +---------------+-------------------------------------------------------------------------------------------+
   | Autor         | Diego Miguel Lozano                                                                       |
   +---------------+-------------------------------------------------------------------------------------------+
   | Requisitos    | RF-2                                                                                      |
   +---------------+-------------------------------------------------------------------------------------------+
   | Precondición  | Haber generado al menos un resumen previamente.                                           |
   +---------------+-------------------------------------------------------------------------------------------+
   | Flujo normal  | | Flujo 1:                                                                                |
   |               | | 1. El usuario pulsa en uno de los resúmenes que aperecen en el inferior de la pantalla. |
   |               | | 2. Se muestra la lista de resúmenes previos.                                            |
   |               | | Flujo 2 (alternativa):                                                                  |
   |               | | 1. El usuario pulsa en «*See all*» en la pantalla prinpal.                              |
   |               | | 2. Se muestra la lista de resúmenes previos.                                            |
   |               | | 3. El usuario pulsa en uno de los resúmenes.                                            |
   |               |                                                                                           |
   +---------------+-------------------------------------------------------------------------------------------+
   | Postcondición | Se ha mostrado el resumen seleccionado.                                                   |
   +---------------+-------------------------------------------------------------------------------------------+
   | Excepciones   | \-                                                                                        |
   +---------------+-------------------------------------------------------------------------------------------+
   | Incluye       | \-                                                                                        |
   +---------------+-------------------------------------------------------------------------------------------+
   | Extiende      | CU-06                                                                                     |
   +---------------+-------------------------------------------------------------------------------------------+
   | Prioridad     | Muy alta.                                                                                 |
   +---------------+-------------------------------------------------------------------------------------------+
   | Frecuencia    | Alta.                                                                                     |
   +---------------+-------------------------------------------------------------------------------------------+
   | Importancia   | Crítica.                                                                                  |
   +---------------+-------------------------------------------------------------------------------------------+
   | Comentarios   | \-                                                                                        |
   +---------------+-------------------------------------------------------------------------------------------+

.. table:: CU-06 Ver texto original

   +---------------+------------------------------------------------------------------+
   | **CU-06**     | **Ver texto original**                                           |
   +===============+==================================================================+
   | Descripción   | Visualizar el texto a partir del cual se ha generado un resumen. |
   +---------------+------------------------------------------------------------------+
   | Autor         | Diego Miguel Lozano                                              |
   +---------------+------------------------------------------------------------------+
   | Requisitos    | RF-2, RF-7                                                       |
   +---------------+------------------------------------------------------------------+
   | Precondición  | Haber generado un resumen.                                       |
   +---------------+------------------------------------------------------------------+
   | Flujo normal  | | 1. El usuario pulsa en «Original».                             |
   +---------------+------------------------------------------------------------------+
   | Postcondición | Se ha mostrado el texto original.                                |
   +---------------+------------------------------------------------------------------+
   | Excepciones   | \-                                                               |
   +---------------+------------------------------------------------------------------+
   | Incluye       | \-                                                               |
   +---------------+------------------------------------------------------------------+
   | Extiende      | CU-07                                                            |
   +---------------+------------------------------------------------------------------+
   | Prioridad     | Alta.                                                            |
   +---------------+------------------------------------------------------------------+
   | Frecuencia    | Alta.                                                            |
   +---------------+------------------------------------------------------------------+
   | Importancia   | Crítica.                                                         |
   +---------------+------------------------------------------------------------------+
   | Comentarios   | \-                                                               |
   +---------------+------------------------------------------------------------------+

.. table:: CU-07 Compartir el resumen

   +---------------+----------------------------------------------------------------------------------------+
   | **CU-07**     | **Compartir el resumen**                                                               |
   +===============+========================================================================================+
   | Descripción   | Compartir el resumen generado a través de otra aplicación.                             |
   +---------------+----------------------------------------------------------------------------------------+
   | Autor         | Diego Miguel Lozano                                                                    |
   +---------------+----------------------------------------------------------------------------------------+
   | Requisitos    | RF-3                                                                                   |
   +---------------+----------------------------------------------------------------------------------------+
   | Precondición  | Haber generado un resumen.                                                             |
   +---------------+----------------------------------------------------------------------------------------+
   | Flujo normal  | | 1. El usuario pulsa en el icono de compartir.                                        |
   |               | | 2. Se muestra una lista de aplicaciones.                                             |
   |               | | 3. El usuario pulsa en la aplicación a través de la cualquiere compartir el resumen. |
   +---------------+----------------------------------------------------------------------------------------+
   | Postcondición | Se ha compartido el resumen.                                                           |
   +---------------+----------------------------------------------------------------------------------------+
   | Excepciones   | \-                                                                                     |
   +---------------+----------------------------------------------------------------------------------------+
   | Incluye       | \-                                                                                     |
   +---------------+----------------------------------------------------------------------------------------+
   | Extiende      | CU-07                                                                                  |
   +---------------+----------------------------------------------------------------------------------------+
   | Prioridad     | Media.                                                                                 |
   +---------------+----------------------------------------------------------------------------------------+
   | Frecuencia    | Media.                                                                                 |
   +---------------+----------------------------------------------------------------------------------------+
   | Importancia   | Media.                                                                                 |
   +---------------+----------------------------------------------------------------------------------------+
   | Comentarios   | \-                                                                                     |
   +---------------+----------------------------------------------------------------------------------------+

.. table:: CU-08 Borrar el resumen

   +---------------+----------------------------------------------------------------------------+
   | **CU-08**     | **Borrar el resumen**                                                      |
   +===============+============================================================================+
   | Descripción   | Compartir el resumen generado a través de otra aplicación.                 |
   +---------------+----------------------------------------------------------------------------+
   | Autor         | Diego Miguel Lozano                                                        |
   +---------------+----------------------------------------------------------------------------+
   | Requisitos    | RF-5                                                                       |
   +---------------+----------------------------------------------------------------------------+
   | Precondición  | Haber generado un resumen.                                                 |
   +---------------+----------------------------------------------------------------------------+
   | Flujo normal  | | 1. El usuario pulsa en el icono de borrar.                               |
   |               | | 2. Se elimina el resumen y la aplicación vuelve a la pantalla principal. |
   +---------------+----------------------------------------------------------------------------+
   | Postcondición | Se ha borrado el resumen.                                                  |
   +---------------+----------------------------------------------------------------------------+
   | Excepciones   | \-                                                                         |
   +---------------+----------------------------------------------------------------------------+
   | Incluye       | \-                                                                         |
   +---------------+----------------------------------------------------------------------------+
   | Extiende      | CU-07                                                                      |
   +---------------+----------------------------------------------------------------------------+
   | Prioridad     | Media.                                                                     |
   +---------------+----------------------------------------------------------------------------+
   | Frecuencia    | Media.                                                                     |
   +---------------+----------------------------------------------------------------------------+
   | Importancia   | Media.                                                                     |
   +---------------+----------------------------------------------------------------------------+
   | Comentarios   | \-                                                                         |
   +---------------+----------------------------------------------------------------------------+

.. [1]
   Este requisito solo se ha implementado en el *backend*. En la
   aplicación decidimos no incluirlo dado que por el momento solo
   hacemos uso de un modelo.

.. [2]
   Este requisito solo se ha implementado en el *backend*. En la
   aplicación se añadirá en futuras iteraciones, al considerarse no
   prioritario, dado que se trata de opciones avanzadas.
