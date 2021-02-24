..
    Copyright (C) 2020-2021 Diego Miguel Lozano <jizt@diegomiguel.me>
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the section entitled "GNU
    Free Documentation License".

.. _chapter:conclusiones:

========================================
Conclusiones y Líneas de trabajo futuras
========================================

Por último, y no por ello menos importante, recogemos las principales
conclusiones extraídas de la realización de este proyecto. Además, se
indican los posibles pasos a tomar en el futuro próximo.

Principales conclusiones
========================

Como mencionábamos en la , desde un principio supimos que JIZT era un
proyecto ambicioso que requeriría una gran inversión de tiempo y
esfuerzo.

Cuatro meses y medio después, podemos decir, no sin cierto alivio, que
hemos sido capaces de cumplir los objetivos que nos marcamos para la
compleción del Trabajo de Fin de Grado; JIZT es, a día de hoy, una
realidad.

Personalmente, nunca imaginamos que en torno a un 65%  del tiempo y
esfuerzo se acabaría destinando al *backend*. Esta era, a su vez, el
área que menos había trabajado con anterioridad, por lo que fue un reto
aún mayor. Cabe preguntarnos, ¿ha valido la pena todo el esfuerzo? Y la
respuesta es un rotundo sí. Contar con una buena infraestructura en el
*backend* será clave para el futuro de JIZT por los siguientes motivos:

-  Facilita el escalado y asegura una alta disponibilidad de los
   componentes implementados actualmente.

-  Permite la ampliación de las tareas de NLP proporcionadas por JIZT,
   así como la actualización de los modelos de generación de resúmenes
   empleados en la actualidad.

-  Incentiva y facilita la colaboración de otros desarrolladores, dado
   que se siguen estándares de la industria.

-  Todo ello se revierte en una mayor satisfacción de los usuarios.

La lección extraída de todo lo mencionado anteriormente es que la
Ingeniería del *Software*, así como el Diseño de Arquitectura de
*Software* son labores que pueden resultar muy complejas, pero a su vez
gratificantes, especialmente en el momento en que finalmente todos los
*tests* se ejecutan con éxito tras horas de trabajo, e interminables
*quebraderos de cabeza*, si se nos permite la expresión.

No obstante, hablando de dificultades, el Procesamiento de Lenguaje
Natural supone también un gran reto; con la realización de este proyecto
nos hemos percatado de la enorme flexibilidad y ambigüedad del lenguaje
natural, lo cual imposibilita establecer reglas prefijadas que sean
válidas para todos los casos, como se intentó desde el inicio del NLP
hasta ya entrado el siglo XXI. Cuando crees que has dado con una regla
que se ajusta a todos los supuestos considerados, aparece un nuevo caso
que invalida todo lo anterior. Por suerte, en los últimos años se han
producido grandes avances en el campo; no podemos esperar a poder
analizar y probar los nuevos descubrimientos que el futuro nos depare.

Podríamos mencionar muchas otras conclusiones, pero todas ellas se
pueden resumir en la siguiente oración: hemos aprendido *mucho*. Nuestro
proyecto ha tratado con diseño de microservicios e infraestructura en la
nube (Kubernetes, Docker, Kafka, API REST), administración de sistemas
(Google Cloud), bases de datos relacionales (PostgreSQL) y no
relacionales (Hive), Inteligencia Artificial (Procesamiento del Lenguaje
Natural), desarrollo de aplicaciones multiplataforma (Flutter),
validación y pruebas, integración y despliegue continuos\ :math:`\ldots`

Este proyecto ha sido una oportunidad de aprendizaje y formación que
creemos será muy positiva de cara a nuestra futura vida estudiantil y
profesional.

Líneas futuras de trabajo
=========================

JIZT, dada su extensión, cuenta con innumerables aspectos a desarrollar
en numerosos aspectos. A continuación listamos algunos de los más
importantes y/o inmediatos:

-  Estudiar posibles métodos de financiación que aseguren la
   sostenibilidad del proyecto.

-  Incluir modelos en otros idiomas, como español, francés, alemán,
   chino, etc.

-  Ampliar el rango de tareas de NLP que JIZT es capaz de llevar a cabo.

-  Entrenar/reemplazar el modelo de *truecasing* (recomposición de
   mayúsculas), ya que el usado actualmente está entrenado con un corpus
   pequeño, el cual generalmente consigue buenos resultados, pero en
   algunos casos es mejorable.

-  Seguir mejorando la API REST y el *backend*. En este aspecto, las
   mejoras más destacables son:

   -  Incluir la capacidad de extraer textos de ficheros, imágenes o
      URLs.

   -  Incluir un "modo privado", dando al usuario la opción de que su
      texto no sea almacenado en la base de datos.

   -  Actualmente, para detectar si un resumen ya ha sido generado
      previamente, se extrae un *hash* (SHA-256) a partir del texto
      original, el modelo, y los parámetros del resumen solicitados. Una
      mejora pasa por atender al texto pre-procesado, en vez del
      original, dado que ahora mismo si cambia un solo carácter del
      texto original, por ejemplo, un espacio, el texto se considera
      como diferente, y se genera un nuevo resumen. Esta mejora conlleva
      cierta dificultad dado que alteraría en cierto modo el orden
      secuencial del proceso de resumen, esto es: el *Dispatcher*
      enviaría el texto original al pre-procesador, el cual, una vez
      pre-procesado el texto, se lo devolvería al *Dispatcher*. En el
      caso de que el texto pre-procesado no existiera, el *Dispatcher*
      reenviaría el texto directamente al Codificador, dado que ya
      estaría pre-procesado.

   -  Incluir la monitorización y la recogida de métricas del sistema.
      Actualmente, se implementa un *logging* básico, suficiente para la
      detección de errores, pero poco apropiado para llevar a cabo
      análisis detallados de uso de recursos, carga de trabajo, etc.

   -  Ofrecer al usuario mensajes de error más granulares. Por ejemplo,
      si el usuario ha definido parámetros de resumen inexistentes, la
      API le indicaría exactamente qué parámetros han sido, y por qué
      valores por defecto se han reemplazado.

-  En cuanto a la aplicación desarrollada:

   -  Iterar junto a la API REST para incluir las mejoras de esta en
      cuestiones como el "modo privado", la generación de resúmenes a
      partir de ficheros, imágenes o URLs, mensajes de error más
      descriptivos, etc.

   -  Mejorar la internacionalización de la aplicación, traduciéndola a
      otros idiomas. Este punto va ligado, en cierto modo, a la
      inclusión de modelos de generación de resúmenes que soporten
      dichos idiomas.
