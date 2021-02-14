======================
Objetivos del proyecto
======================

En este apartado, detallamos los objetivos tanto generales, como
técnicos, cuya consecución se pretende lograr a través del desarrollo
del proyecto.

Objetivos generales
===================

Los objetivos generales que persigue el proyecto son:

-  Ofrecer la capacidad de llevar a cabo tareas de NLP tanto al público
   general, como al especializado. Como se ha mencionado con
   anterioridad, la tarea de NLP que implementará el presente TFG
   será la de generación de resúmenes.

-  Emplear modelos pre-entrenados del estado del arte para la generación
   de resúmenes abstractivos. Los resúmenes abstractivos se diferencian de los
   extractivos en que el resumen generado contiene palabras o expresiones que no
   aparecen en el texto original [abigail17]_. Dicho de forma más técnica, existe
   cierto nivel de paráfrasis.

-  Diseñar una arquitectura, tanto como para el servicio de resúmenes en
   la nube, como para la aplicación multiplataforma, con aspectos como
   la flexibilidad, la escalabilidad y la robustez como principios
   fundamentales.

-  Poner en práctica lo aprendido a lo largo del Grado en áreas como
   Ingeniería del Software, Sistemas Distribuidos, Programación, Minería
   de Datos, Algoritmia y Bases de Datos.

-  Ofrecer la totalidad del proyecto bajo licencias de *Software* Libre.

Objetivos técnicos
==================

Además de los objetivos generales listados anteriormente, el proyecto
cuenta con los siguientes objetivos técnicos:

-  Los modelos pre-entrenados de generación de texto admiten parámetros
   específicos para configurar dicha generación, por lo que se deberá
   implementar una interfaz que permita a los usuarios establecer estos
   parámetros de manera opcional. Por defecto, se proporcionarán los
   valores que mejores resultados ofrecen, extraídos mayoritariamente
   experimentalmente.

-  Los modelos pre-entrenados de generación estado del arte presentan
   frecuentemente limitaciones en la longitud de los textos de entrada
   que reciben, derivadas de la longitud de las secuencias de entrada
   con las que han sido entrenados. Esta longitud llega a ser tan baja
   como 512 *tókenes*\ [1]_ [raffel19]_. Por tanto, se
   deberá establecer algún mecanismo que permita sortear esta limitación
   para poder generar resúmenes de textos arbitrariamente largos.

-  Gestionar el pre-procesado de los textos a resumir para ajustarlos a
   la entrada que los modelos pre-entrenados esperan.

-  Algunos modelos pre-entrenados generan textos enteramente en
   minúsculas. Se deberá, por tanto, incluir mecanismos en la etapa de
   post-procesado que permitan recomponer el correcto uso de las
   mayúsculas en los resúmenes generados.

-  Con el fin de cumplir con el objetivo general referente a la
   arquitectura, desarrollar una arquitectura de microservicios, basada en la
   filosofía *Cloud Native* [cloud20]_ [arundel19]_. Este objetivo se divide
   a su vez en dos puntos:

   -  Encapsular cada microservicio en un contenedor Docker.

   -  Implementar la orquestración y balanceo de los microservicios a
      través de herramientas como Kubernetes y Kafka.

-  Complementariamente al punto anterior, implementar una arquitectura
   dirigida por eventos [bellemare20]_. La motivación
   detrás de la utilización de este patrón arquitectónico se justifica
   en el capítulo de :ref:`chapter:conceptos-teoricos`.

-  Implementar una API REST escrita en Python empleando el *framework
   web* Flask. Dicha API será el punto de conexión con el servicio de
   generación de resúmenes en la nube.

-  Desplegar PostgreSQL como servicio en Kubernetes mediante el Operador
   PostgreSQL de Crunchy [crunchy21]_. Esta base de datos
   cumplirá la doble función de (a) servir como caché para no volver a
   producir resúmenes ya generados con anterioridad, incrementando la
   velocidad de respuesta, y (b) almacenar los resúmenes generados con
   fines de evaluación de la calidad de los mismos y extracción de
   métricas.

-  Desarrollar, con ayuda de Flutter, una aplicación multiplataforma con
   soporte nativo para Android, iOS, y *web*. Esta aplicación consumirá
   la API y proporcionará una interfaz gráfica sencilla e intuitiva para
   que usuarios regulares puedan hacer uso del servicio de generación de
   resúmenes.

-  Diseñar una arquitectura modular para la aplicación, inspirada en *Clean
   Architecture* [martin15]_ y Diseño guiado por el dominio (DDD, por sus siglas en
   inglés) [vernon13]_.

.. [1]
   Este término se definirá posteriormente. Por ahora, el lector puede
   considerar que un *tóken* es equivalente a una palabra.

.. [abigail17]
   Abigail See, Peter J. Liu y Christopher D. Manning. eGet To The
   Point: Summarization with Pointer-Generator Networks". En: CoRR
   abs/1704.04368 (2017), pág. 1. arXiv: 1704.04368. URL:
   `<http://arxiv.org/abs/1704.04368>`__.
   Último acceso: 27/01/2020.

.. [raffel19]
   Colin Raffel y col. "Exploring the Limits of Transfer Learning with a
   Unified Text-to-Text Transformer". En: CoRR abs/1910.10683 (2019),
   pág. 11. arXiv: 1910.10683. URL:
   `<http://arxiv.org/abs/1910.10683>`__.
   Último acceso: 27/01/2020.

.. [cloud20]
   Microsoft. Defining Cloud Native. Mayo de 2020. URL:
   `<https://docs.microsoft.com/en-us/dotnet/architecture/cloud-native/definition>`__.
   Último acceso: 27/01/2020.

.. [arundel19]
   John Arundel y Justin Domingus. Cloud Native DevOps with Kubernetes. O’Reilly
   Media, Inc., mar. de 2019. ISBN: 9781492040767.

.. [bellemare20]
   Adam Bellemare. Building Event-Driven Microservices: Leveraging Organizational Data
   at Scale. O’Reilly Media, Inc., 2020. ISBN: 9781492057895.

.. [crunchy21]
   Crunchy Data. Crunchy PostgreSQL Operator. Mayo de 2021. URL:
   `<https://access.crunchydata.com/documentation/postgres-operator/4.5.1/>`__.
   Último acceso: 04/02/2020.

.. [martin15]
   Robert Martin. Clean Architecture: A Craftsman’s Guide to Software
   Structure and Design. Pearson Education, 2015. ISBN: 9780134494166.

.. [vernon13]
   Vaughn Vernon. Implementing Domain-Driven Design. Addison-Wesley
   Professional, 2013. ISBN: 0321834577.
