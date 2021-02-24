..
    Copyright (C) 2020-2021 Diego Miguel Lozano <jizt@diegomiguel.me>
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the section entitled "GNU
    Free Documentation License".

.. _apendix:manual-programador:

=====================================
Documentación técnica de programación
=====================================

Introducción
============

En este apéndice se detalla toda la información que pueda ser de ayuda
para cualquier desarrollador interesado en desplegar y/o contribuir al
proyecto.

De igual modo a como hemos venido haciendo en los anteriores apéndices,
separaremos los detalles referentes al *backend* y al *frontend*, ya que
se trata de entornos completamente independientes, cada uno con sus
características y peculiaridades concretas.

Documentación técnica del *backend*
===================================

Estructura de directorios
-------------------------

La estructura de directorios del *backend* de JIZT, a la cual se puede
acceder a través de
`github.com/dmlls/jizt-tfg <https://https://github.com/dmlls/jizt-tfg>`__, es la
siguiente:

-  ``/src``: este directorio contiene el código fuente completo del
   *backend*.

-  ``/src/helm``: ficheros relativos a Helm [helm]_.

-  ``/src/helm/jizt``: ficheros para el despliegue de los componentes
   relativos a JIZT en Kubernetes.

-  ``/src/helm/jizt/charts``: dependencias de paquetes Helm externos.

-  ``/src/helm/jizt/jiztlibchart``: librería de plantillas Helm para los
   componentes de JIZT.

-  ``/src/helm/jizt/setup``: *scripts* para el despliegue de JIZT en
   Kubernetes.

-  ``/src/services``: microservicios de JIZT.

-  ``/src/services/dispatcher``: microservicio *Dispatcher*.

-  ``/src/services/postgres``: esquemas iniciales de la base de datos.

-  ``/src/services/t5_large_text_encoder``: microservicio Codificador.

-  ``/src/services/t5_large_text_summarizer``: microservicio Generador
   de resúmenes.

-  ``/src/services/text_postprocessor``: microservicio Postprocesador de
   texto.

-  ``/src/services/text_preprocessor``: microservicio Preprocesador de
   texto.

-  ``/test``: pruebas unitarias y de sistema.

Manual del programador
----------------------

En esta sección, se recogen todos los detalles necesarios para la
instalación y despliegue de la arquitectura de microservicios en
Kubernetes.

Instalación y despliegue del *backend*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El primer paso será descargarnos el código fuente correspondiente al
*backend*, clonando el repositorio del proyecto alojado en GitHub:

``git clone https://github.com/dmlls/jizt-tfg.git``

Una vez disponemos del código fuente, debemos proceder primero a la
instalación y provisión de los prerrequisitos necesarios para la
instalación de JIZT.

.. warning::

   El despliegue del *backend* requiere de
   **conocimientos intermedios de Kubernetes**. En el presente manual,
   trataremos de explicar el proceso de instalación de la manera más
   detallada posible. No obstante, **no podemos condensar todo el
   conocimiento necesario de Kubernetes en este manual**, dado que para
   ello ya existe la propia documentación oficial de Kubernetes, la cual se
   recomienda encarecidamente revisar antes de comenzar la instalación de
   JIZT. Dicha documentación es accesible a través de
   https://kubernetes.io/es/docs/home.

En cualquier caso, para cualquier tipo de ayuda o duda acerca de la
instalación o utilización de JIZT, se puede contactar con el equipo de
soporte técnico de JIZT a través de la siguiente dirección de correo
electrónico: jizt@diegomiguel.me. Estaremos encantados de atenderle.

**Prerrequisitos**

La infraestructura en la nube de JIZT se apoya en la utilización de
diferentes plataformas y *frameworks* que se deben instalar con
antelación.

.. note::

   Se recomienda ejecutar la instalación de JIZT a través de una máquina
   **GNU/Linux**. La instalación a través de otros sistemas operativos no
   ha sido probada y, por tanto, no se asegura una instalación exitosa.

**Programas requeridos**

Antes de comenzar con la instalación de JIZT, se deben instalar
localmente los siguientes programas:

-  ``kubectl``: herramienta de línea de comandos de Kubernetes, empleada
   para el despliegue y la gestión de aplicaciones en Kubernetes. Se
   pueden encontrar las instrucciones de instalación en
   https://kubernetes.io/es/docs/tasks/tools/install-kubectl.

-  ``helm``: CLI para Helm, un popular gestor de paquetes para
   Kubernetes. Para su instalación, se deben seguir los pasos recogidos
   en https://helm.sh/docs/intro/install.

-  ``pgo``: CLI para el operador de PostgreSQL de Crunchy. A través de
   esta herramienta, podemos conectarnos con nuestra base de datos
   PostgreSQL desplegada en Kubernetes. Se puede consultar
   https://access.crunchydata.com/documentation/postgres-operator/4.5.1/installation/pgo-client
   para su instalación.

-  SDK de Google Cloud: este SDK nos permite conectarnos y gestionar
   *clústers* de Kubernetes alojados en Google Cloud. En
   https://cloud.google.com/sdk/docs/install se detalla el proceso de
   instalación.

Se considera, asimismo, que el programador cuenta con ``git`` de
antemano. En caso contrario, puede acceder a las instrucciones para su
instalación en
https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.

**Requisitos de hardware**

La arquitectura ha de desplegarse, como es lógico, en un servidor
físico. Existen dos alternativas para ello:

-  **Bare metal**: con esta opción, se dispone de un servidor dedicado
   en el que es necesario instalar todas las dependencias (listadas a
   continuación) manualmente.

-  **Cloud provider**: **esta es la opción de despliegue recomendada**.
   En este caso, contratamos un servicio *cloud* con un *cloud provider*
   concreto, como puede ser Google Cloud, Amazon Web Services (AWS), o
   Microsoft Azure. Estos *cloud providers* disponen de servicios
   concretos para el despliegue de aplicaciones en Kubernetes (como
   Google Kubernetes Engine, GKE, en el caso de Google Cloud). Esto
   facilita en gran medida la labor de despliegue.

**Despliegue en Google Kubernetes Engine (GKE)**

Google Kubernetes Engine, GKE, ha sido la plataforma con la que se ha
trabajado en el desarrollo del proyecto. Es, por tanto, la **opción que
más garantías de correcto funcionamiento ofrece**.

Google Cloud ofrece actualmente 300$ de crédito gratuitos durante 90
días la primera vez que nos registramos en el servicio.

Para la creación de una cuenta de Google Cloud, y la creación de un
*clúster* de Kubernetes en GKE, se deben seguir los pasos recogidos en la
siguiente página:
https://cloud.google.com/kubernetes-engine/docs/quickstart.

La configuración recomendada a la hora de crear un nuevo *clúster* es la
siguiente:

-  **Tipo de ubicación**: zonal.

-  **Zona principal**: europe-west2-a.

-  **Canal de versiones**: Canal rápido.

-  **Versión**: 1.18.12-gke.1206.

-  **Nodos**:

   -  **Número de nodos**: 1.

   -  **Tipo de máquina**: e2-standard-4 (4 vCPUS, 16GB de RAM).

   -  **Tipo de imagen**; Container-Optimized OS con Docker (cos).

Además, se debe crear un Disco Persistente de GCE, siguiendo los pasos
listados en
https://cloud.google.com/compute/docs/disks/add-persistent-disk?hl=es-419.
En este disco, se almacenarán los modelos de generación de lenguaje que
empleará JIZT.

Actualmente, se hace uso del modelo **t5-large** implementado por
Hugging Face, el cual se puede descargar a través del siguiente *link*:
https://huggingface.co/t5-large. Este modelo se divide a su vez en el
*tokenizer*, encargado de la codificación, y el modelo propiamente
dicho, el cual se encarga de la generación de los resúmenes.

Una vez tenemos el modelo descargado localmente, los cargaremos en el
Disco Persistente creado anteriormente. Para ello, nos conectamos a
través de ``ssh`` o desde la Consola de Google Cloud (`más
información <https://cloud.google.com/compute/docs/instances/connecting-to-instance?hl=es-419#console>`__),
y copiamos el modelo a las siguientes rutas:

-  | El *tokenizer* debe estar alojado en el directorio
   | ``/home/text_encoder/models``.

-  El modelo debe situarse en ``/home/text_summarizer/models``.

Finalizados estos pasos, estamos en disposición de instalar las
dependencias de JIZT.

**Instalación del Operador de PostgreSQL**

Este operador nos permite desplegar PostgreSQL en Kubernetes. Para su
instalación y despliegue, se deben seguir los pasos recogidos en
https://access.crunchydata.com/documentation/postgres-operator/4.5.1/installation/other/google-cloud-marketplace.

Una vez instalado el operador, nos conectaremos al *clúster* de PostgreSQL
creado del siguiente modo:
https://access.crunchydata.com/documentation/postgres-operator/4.5.1/tutorial/connect-cluster.

Una vez conectados al *clúster*, debemos ejecutar el *script* SQL situado
en el directorio del proyecto de JIZT:
``src/services/postgres/schemas.sql``. Este *script* proveerá la base de
datos con la estructura de tablas iniciales.

Finalmente debemos crear un *secret* de Kubernetes conteniendo los
detalles de conexión a la base de datos, esto es, el nombre de usuario y
la contraseña especificados a la hora de instalar el *clúster* de
PostgreSQL. Para ello, se deben seguir los pasos indicados en
https://kubernetes.io/docs/concepts/configuration/secret/#creating-a-secret.
El nombre del secreto debe ser ``pg-dispatcher``.

**Instalación de JIZT**

La instalación de los prerrequisitos es, probablemente, la parte más
complicada de todo el proceso de instalación.

Por suerte, para la instalación de JIZT, hemos creado un *script* bash
que automatiza el despliegue de Strimzi (Kafka en Kubernetes) y de los
componentes propios de JIZT\ [1]_.

Dicho *script* se encuentra en el directorio
``src/helm/setup/setup.sh``. Si se ejecuta sin especificar ninguna
opción, se instalan los componentes tanto de Strimzi como de JIZT. El
*script* también admite la opción ``-p`` o ``--partial`` para realizar
una instalación parcial únicamente de los componentes de JIZT. Esto es
útil para el caso de que ya hayamos instalado previamente los
componentes relativos a Strimzi.

Podemos comprobar la correcta instalación de los componentes ejecutando:
``kubectl get deployment``. Deberían aparecer los siguientes
*deployments*:

-  ``dispatcher-deployment``

-  ``jizt-cluster-entity-operator``

-  ``t5-large-text-encoding-deployment``

-  ``t5-large-text-summarization-deployment``

-  ``text-postprocessing-deployment``

-  ``text-preprocessing-deployment``

Fichero de configuración de Kubernetes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A través del fichero ``src/helm/jizt/values.yaml``, se pueden configurar
los parámetros de instalación y despliegue de JIZT en Kubernetes.

A continuación, se detallan los parámetros que este fichero permite
modificar:

-  ``namespace``: *namespace* (espacio de nombres) en el que se
   instalarán los componentes de JIZT. Para más información sobre los
   *namespaces* de Kubernetes, se puede consultar
   https://kubernetes.io/es/docs/concepts/overview/working-with-objects/namespaces.

-  ``ingress``: configuración de Ingress. Para más información sobre el
   componente Ingress de Kubernetes, se puede visitar
   https://kubernetes.io/docs/concepts/services-networking/ingress.

-  ``replicaCount``: número de réplicas global para todos los
   *deployments*. Es decir, si por ejemplo se configura con 2 réplicas,
   todos los *deployments* relativos a JIZT tendrán 2 *pods*.

-  ``autoscaling``: permite activar o desactivar el auto-escalado, de
   modo que en momentos de mayor carga, el número de réplicas aumente
   automáticamente. Desactivado por defecto.

-  ``dispatcher``: configuración relativa al *deployment* del
   *Dispatcher*.

   -  ``name``: nombre del microservicio.

   -  ``ports``: puertos relativos al microservicio.

      -  ``svc``: puerto del *service* asociado al *deployment*.

      -  ``container``: puerto de la aplicación que se ejecuta en la
         imagen Docker que emplean los *pods* del *deployment*.

   -  ``image``: imagen Docker que ejecutan los *pods* del *deployment*.

-  Los campos del ``dispatcher`` son comunes al resto de microservicios,
   esto es ``textPreprocessor``, ``t5LargeTextEncoder``,
   ``t5LargeTextSumma``-``rizer``, y ``textPostprocessor``.

-  ``t5LargeTextEncoder`` y ``t5LargeTextSummarizer``: además de los
   campos comunes a ``dispatcher``, estos microservicios disponen de la
   siguiente configuración:

   -  ``volumeMounts``: configuración relativa al Volumen Persistente en
      el que se almacenan los modelos de *tokenización* y generación de
      resúmenes.

      -  ``modelsMountPath``: ruta (directorio) en la que se encuentran
         almacenados los modelos.

      -  ``tokenizerPath``: ruta del *tokenizer*. Esto es, la ruta
         absoluta del *tokenizer* será ``modelMountPath/tokenizerPath``.

      -  ``modelPath``: ruta del modelo generador de resúmenes. Esto es,
         la ruta absoluta del modelo generador será
         ``modelMountPath/modelPath``.

-  ``t5LargeTextSummarizer``: además de los campos mencionados
   anteriormente, este microservicio permite establecer los parámetros
   por defecto para la generación de resúmenes a través del campo
   ``params``. El significado de cada uno de los parámetros se recoge en
   la sección correspondiente a la :ref:`subsection:api-docs`.

-  ``postgres``: configuración referente a la base de datos PostgreSQL.

   -  ``host``: *host* de PostgreSQL.

   -  ``dbName``: nombre de la base de datos.

   -  ``secret``: información relativa al *secret* de Kubernetes que
      contiene el nombre de usuario y la contraseña de PostgreSQL.

-  ``modelsPV``: configuración relativa al Volumen Persistente en el que
   se alojan los modelos.

-  ``kafka``: configuración de Kafka. Para más información, se puede
   consultar la documentación de Strimzi en
   https://strimzi.io/docs/0.5.0.

   -  ``name``: nombre del *clúster* de Kafka.

   -  ``namespace``: espacio de nombres en el que se desplegarán los
      componentes de Kafka.

   -  ``version``: versión de Kafka.

   -  ``replicas``: número de réplicas de los componentes de Kafka.

   -  ``resources``: límites de recursos para los componentes de Kafka.

      -  ``memoryRequests``: memoria solicitada por los componentes de
         Kafka.

      -  ``memoryLimits``: límites de memoria que los componentes de
         Kafka pueden solicitar.

   -  ``config``: otras configuraciones.

      -  ``autoCreateTopics``: permitir a Kafka crear *topics* de manera
         automática. Desactivado por defecto.

      -  ``messageMaxBytes``: máximo tamaño que un mensaje puede tener.
         Por defecto 1MB.

      -  ``topicReplicationFactor``: factor de replicación de los
         *topics*.

   -  ``zookeeper``: configuración relativa al *zookeeper* de Kafka. Se
      puede encontrar más información relativa a este componente en
      https://kafka.apache.org/documentation/#zk.

-  ``topics``: configuración relativa a los *topics* de Kafka. Para más
   información acerca de los *topics* de Kafka, visitar
   https://kafka.apache.org/documentation/#intro_topics.

   -  ``partitions``: número de particiones (común a todos los
      *topics*).

   -  ``replicas``: número de réplicas (común a todos los *topics*).

   -  ``retentionMs``: máximo tiempo de retención de los mensajes en los
      *topics*. Si tras este tiempo, el mensaje no ha sido consumido, se
      descarta. Por defecto fijado a 10 minutos.

.. _subsection:api-docs:

Especificación de la API REST
-----------------------------

En esta sección se incluye documentación detallada sobre la API REST de
JIZT. Más concretamente, se especifican los *enpoints* existentes, así
como las operaciones HTTP permitidas, y la estructura tanto de las
peticiones HTTP, como de las respuestas del *backend*.

.. note::

   En `docs.api.jizt.it <https://dmlls.github.io/jizt-tfg-api-docs>`__ se puede encontrar la
   documentación en línea referente a la API REST. Dado que dicha
   documentación está en inglés, recogemos su traducción al español. El
   usuario puede referirse a cualquiera de las dos documentaciones, ya que
   son idénticas.

Operación POST - Solicitar resumen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Endpoint**: ``https://api.jizt.it/v1/summaries/plain-text``

**Petición HTTP**:

-  Content-Type: ``application/json``

-  Atributos del JSON del cuerpo de la petición\ [2]_:

   -  ``source`` (*string*) **obligatorio**: el texto a resumir.

   -  ``model`` (*string*): el modelo a emplear para la generación del
      resumen. Valores permitidos: ``"t5-large"``.

   -  ``params`` (*object*): parámetros del resumen.

      -  ``relative_max_length`` (*number <float>*): longitud máxima del
         resumen a generar, relativa a la longitud del texto original.
         Por ejemplo, un valor de ``0.4`` significa que la longitud del
         resumen será, como máximo, un 40% de la longitud del texto
         original.

      -  ``relative_min_length`` (*number <float>*): longitud mínima del
         resumen a generar, relativa a la longitud del texto original.

      -  ``do_sample`` (*boolean*): usar muestreo o no. Si se establece
         como falso, se emplea búsqueda voraz\ [3]_.

      -  ``early_stopping`` (*boolean*): detener la búsqueda si se
         terminan ``num_beams`` frases o no.

      -  ``num_beams`` (*integer <int32>*): número de *beams* en la
         *beam_search*. Si se fija como ``1``, no se lleva a cabo *beam
         search*. Cuanto mayor sea el número, más tiempo tardará en
         generarse el resumen, pero su calidad será probablemente mejor.

      -  ``temperature`` (*number <float>*): valor utilizado para
         modular las probabilidades del siguiente *token*.

      -  ``top_k`` (*integer <int32>*): número de *tókenes* con mayor
         probabilidad a considerar al realizar muestreo *top-k*.

      -  ``top_p`` (*number <float>*): si se fija a valores menores de
         ``1``, solo se consideran los *tókenes* más probables cuya suma
         de probabilidades es igual o mayor a *top_k*.

      -  ``repetition_penalty`` (*number <float>*): penalización
         aplicada a la repetición de *tókenes*. Si se establece a *1.0*
         no se aplica penalización.

      -  ``length_penalty`` (*number <float>*): penalización aplicada de
         manera exponencial a la longitud de las secuencias generadas.
         Si se establece a ``1.0`` no hay penalización. Valores por
         debajo de ``1.0`` resultarán en resúmenes más cortos.

      -  ``no_repeat_ngram_size`` (*integer <int32>*):longitud de los
         *n-gramas* que se pueden repetir una única vez. Por ejemplo, si
         se fija a *2*, las palabras "Ingeniería Informática" solo
         podrán aparecer una vez en el resumen.

   -  ``language`` (*string*): el idioma del texto. Valores permitidos:
      ``"en"``.

**Respuestas**

**Status code: 200 OK**

-  *Response schema*: ``application/json``

-  Atributos del JSON del cuerpo de la respuesta:

   -  ``summary_id`` (*string*): el *id* del resumen.

   -  ``started_at`` (*string <date-time>*): el instante de tiempo en el
      que se solicitó por primera vez un resumen con un texto de
      entrada, parámetros, y modelo específicos.

   -  ``ended_at`` (*string <date-time>*): el instante de tiempo en el
      que se finalizó por primera vez un resumen con un texto de
      entrada, parámetros, y modelo específicos. Restando este valor al
      anterior, se puede conocer el tiempo que tomó la generación del
      resumen.

   -  ``status`` (*string*): el estado del resumen. Posibles valores:
      ``"preprocessing"``, ``"encoding"``, ``"summarizing"``,
      ``"postprocessing"``.

   -  ``output`` (*string*): el resumen generado.

   -  ``model`` (*string*): modelo empleado para la generación del
      resumen. Valores posibles: ``"t5-large"``.

   -  ``params`` (*object*): los parámetros con los que se ha generado
      el resumen (mismo esquema que en la petición).

   -  ``language`` (*string*): el idioma del resumen. Valores posibles:
      ``"en"``.

**Status code: 502 Server Error**

-  *Response schema*: ``text/html; charset=utf-8``

Operación GET - Consultar resumen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Endpoint**:
``https://api.jizt.it/v1/summaries/plain-text/{summaryId}``

**Parámetros del path**:

-  ``summaryId`` (*string*) **obligatorio**: el *id* del resumen a
   consultar.

**Respuestas**

**Status code: 200 OK**

-  *Response schema*: ``application/json``

-  Atributos del JSON del cuerpo de la respuesta: mismos que en la
   respuesta HTTP 200 de la operación POST.

**Status code: 404 Not found**

-  *Response schema*: ``application/json``

-  Atributos del JSON del cuerpo de la respuesta:

   -  ``errors`` (*string*): mensaje de error.

**Status code: 502 Server Error**

-  *Response schema*: ``text/html; charset=utf-8``

Operación GET - Salud del servidor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Endpoint**: ``https://api.jizt.it/v1/healthz``

**Respuestas**

**Status code: 200 OK**

-  *Response schema*: ``text/html; charset=utf-8``

**Status code: 502 Server Error**

-  *Response schema*: ``text/html; charset=utf-8``

Pruebas del sistema
-------------------

Las pruebas de sistema para el *backend* de JIZT comprenden varias
pruebas unitarias, de cada una de las etapas en la generación de resumen
(pre-procesado, codificación, resumen y post-procesado) y una prueba de
integración que prueba el correcto funcionamiento de la API REST y el
*backend* en su conjunto.

Prerrequisitos
~~~~~~~~~~~~~~

Para poder ejecutar las pruebas, se requiere tener instalado el
*framework* de pruebas para Python ``pytest``.

Las instrucciones para su instalación se pueden encontrar en
https://docs.pytest.org/en/stable/getting-started.html. Si se dispone de
``pip``, se puede instalar fácilmente ejecutando:

``pip install -U pytest``.

Ejecución de las pruebas
~~~~~~~~~~~~~~~~~~~~~~~~

Para ejecutar todas las pruebas, basta con ejecutar: ``pytest``, bien
desde el directorio raíz del proyecto, o desde el directorio de
``tests``.

Si se quieren ejecutar únicamente alguna de las pruebas en específico,
se puede pasar el nombre del fichero al invocar a ``pytest``.

Documentación técnica de la aplicación
======================================

En esta sección, se recoge toda la información necesaria para poder
trabajar sobre el código fuente de la aplicación, así como compilarlo.

.. _estructura-de-directorios-1:

Estructura de directorios
-------------------------

La estructura de directorios de la aplicación de JIZT, a la cual se
puede acceder a través de
`github.com/dmlls/jizt-tfg-app <https://github.com/dmlls/jizt-tfg-app>`__, es la
siguiente:

-  ``/``: el directorio raíz contiene todos los ficheros que componen el
   proyecto Flutter de la aplicación.

-  ``/lib``: se trata del directorio principal del proyecto, donde se
   encuentra el código fuente de la aplicación, escrito en Dart.

-  ``/lib/home)``: implementación de la interfaz gráfica y de la lógica
   de la pantalla principal de la aplicación.

-  ``/lib/new_text_summary``: implementación de la interfaz gráfica y de
   la lógica de la pantalla para generar resúmenes a partir de texto.

-  ``/lib/summaries``: implementación de la interfaz gráfica y de la
   lógica de la pantalla que lista todos los resúmenes generados por el
   usuario.

-  ``/lib/summary``: implementación de la interfaz gráfica y de la
   lógica de la pantalla de detalle de un resumen.

-  ``/lib/utils``: utilidades varias.

-  ``/lib/widgets``: *widgets* de Flutter adicionales.

-  ``/modules/data``: componentes relativos a la capa de datos de la
   aplicación.

-  ``/modules/domain``: componentes relativos a la capa de dominio de la
   aplicación.

-  ``/assets/drawables``: imágenes y fuentes de las que hace uso la
   aplicación.

-  ``/android``: proyecto de Android.

-  ``/ios``: proyecto de iOS.

-  ``/web``: proyecto para *web*.

.. _manual-del-programador-1:

Manual del programador
----------------------

Una vez introducida la estructura de directorios, explicaremos cómo
podemos compilar la aplicación para las diferentes plataformas, y qué
programas necesitamos para ello.

.. _prerrequisitos-1:

Prerrequisitos
~~~~~~~~~~~~~~

Lo primero que debemos hacer, es instalar Flutter en nuestro ordenador.
Flutter está disponible para GNU/Linux, macOS, Windows, y Chrome OS. A
diferencia del caso del *backend*, el cual recomendamos instalar y
desplegar empleando un dispositivo GNU/Linux, la compilación de la *app*
se puede llevar a cabo en el sistema operativo que el programador
considere oportuno.

Las instrucciones para instalar Flutter en los distintos sistemas
operativos se pueden encontrar en
https://flutter.dev/docs/get-started/install.

Se considera, asimismo, que el programador cuenta con ``git`` de
antemano. En caso contrario, puede acceder a las instrucciones para su
instalación en
https://git-scm.com/book/en/v2/Getting-Started-Installing-Git.

Entorno de desarrollo
~~~~~~~~~~~~~~~~~~~~~

Para conseguir la mejor experiencia de desarrollo en Flutter, se
recomienda emplear uno de los siguientes tres IDEs:

-  **Android Studio**: se trata del IDE que proporciona oficialmente
   Google para el desarrollo de aplicaciones Android [android-studio]_.

-  **IntelliJ IDEA**: es otro de los IDEs recomendados para el
   desarrollo en Flutter, en este caso desarrollado por JetBrains. Como
   curiosidad, Android Studio se construyó sobre este IDE [intellij]_.

-  **Visual Studio Code**: este es el tercer IDE recomendado,
   desarrollado por Microsoft [visual-code]_.

Estos tres IDEs cuentan con sendos *plugins* para la programación en
Dart en el contexto de Flutter. Se puede encontrar más información de
como configurar cada uno de los IDEs a través de la documentación
oficial de Flutter:
https://flutter.dev/docs/development/tools/android-studio.

Compilación de la aplicación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La compilación de la *app* requiere únicamente de tres comandos:

-  | Clonar el repositorio desde GitHub:
   | ``git clone https://github.com/dmlls/jizt-tfg-app.git``

-  | Descargar los paquetes requeridos por la aplicación:
   | ``flutter pub get``

-  Compilar la aplicación para la plataforma deseada:

   ``flutter build [appbundle|apk|ios|web|linux|windows|macos]``

   -  ``appbundle``: compila a un App Bundle de Android.

   -  ``apk``: compilar a una APK de Android.

   -  ``ios``: compilar una aplicación para iOS. Solo se puede ejecutar
      desde MacOS.

   -  ``web``: compilar para *web*\ [4]_.

   -  ``linux``: compilar para GNU/Linux\ [5]_. Solo se puede ejecutar
      desde Linux.

   -  ``windows``: compilar para Windows. Solo se puede ejecutar desde
      Windows.

   -  ``macos``: compilar para MacOS. Solo se puede ejecutar desde
      MacOS.

Con estos tres sencillos pasos, obtendremos un binario de la aplicación
para la plataforma deseada.

Contribuir al proyecto
======================

A fin de organizar las posibles contribuciones de la comunidad al
proyecto JIZT, se ha creado un documento que contiene algunas pautas y
recomendaciones a la hora de contribuir.

Dicho documento es válido tanto para el caso del *backend*, como de la
aplicación. Se ha escrito en un registro informal, a fin de animar todo
tipo de contribuciones, por muy pequeñas que parezcan, ya que no es
necesario tener conocimientos de programación para contribuir al
proyecto.

El documento se puede consultar en el apartado :ref:`contributing`.


.. [1]
   Este *script* solo se ha probado en GNU/Linux. No se asegura su
   correcto funcionamiento en otros sistemas operativos.

.. [2]
   Todos los atributos no marcados como "obligatorio" se pueden
   omitir. En ese caso, tomarán valores por defecto.

.. [3]
   Para más información sobre los distintos tipos de generación de
   lenguaje, referirse al capítulo de :ref:`chapter:conceptos-teoricos` de la
   Memoria

.. [4]
   El soporte de Flutter para *web* se encuentra aún en fase *beta*
   [flutter-web]_. No se recomienda su uso en
   producción.

.. [5]
   El soporte de Flutter para escritorio (GNU/Linux, MacOS y Windows)
   se encuentra en fase *alfa* [flutter-desktop]_.
   No se recomienda su uso fuera del entorno de desarrollo.

.. [helm]
   Helm. Helm - The package manager for Kubernetes. Dic. de 2020. URL:
   https://helm.sh.
   Último acceso: 11/02/2021.

.. [android-studio]
   Wikipedia - La enciclopedia libre. Android Studio. Ene. de 2021. URL:
   https://en.wikipedia.org/wiki/Android_Studio.
   Últimso: 11/02/2021.

.. [intellij]
   Wikipedia - La enciclopedia libre. IntelliJ IDEA. Ene. de 2021. URL:
   https://en.wikipedia.org/wiki/IntelliJ_IDEA.
   Últimso: 11/02/2021.

.. [visual-code]
   Wikipedia - La enciclopedia libre. Visual Studio Code. Ene. de 2021. URL:
   https://en.wikipedia.org/wiki/Visual_Studio_Code.
   Último: 11/02/2021.

.. [flutter-desktop]
   Flutter. Desktop support for Flutter. Feb. de 2021. URL:
   https://flutter.dev/desktop.
   Últimso: 11/02/2021.