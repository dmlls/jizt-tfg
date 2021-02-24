..
    Copyright (C) 2020-2021 Diego Miguel Lozano <jizt@diegomiguel.me>
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
    A copy of the license is included in the section entitled "GNU
    Free Documentation License".

JIZT - AI Summarization in the cloud
====================================

**¡Gracias por interesarte en JIZT!**

En los últimos cinco años, se han llevado a cabo grandes avances en el campo del
Procesamiento de Lenguaje Natural (NLP). Sin embargo, el alcance de muchos de estos
avances para el público en general, se ha visto limitado a ciertas áreas del NLP, como
la traducción automática, los *bots* conversacionales, el filtrado de
*spam*, etc., mientras que en el caso de otras tareas, como la generación de
resúmenes, sigue existiendo a día de hoy escasez de alternativas.

JIZT es un servicio de generación de resúmenes en la nube basado en la filosofía
*Cloud Native*, y sustentado por una arquitectura de microservicios
dirigida por eventos, hecho que asegura la escalabilidad y la alta
disponibilidad del servicio.

Adicionalmente, se ha desarrollado una aplicación multiplataforma (móvil,
*web* y escritorio), que consume la API REST del servicio de resúmenes en
la nube, permitiendo que cualquier usuario pueda obtener resúmenes de sus textos
de manera sencilla.

La resúmenes generados son, además, fruto de la utilización de los modelos de
generación de lenguaje más avanzados a día de hoy. Como resultado, a diferencia
de otros servicios, JIZT ofrece resúmenes abstractivos, esto es, resúmenes que
contienen palabras y expresiones que no están presentes en el texto original.

.. toctree::
   :caption: Memoria
   :name: memoria
   :maxdepth: 2

   memoria/1_Introduccion
   memoria/2_Objetivos_del_proyecto
   memoria/3_Conceptos_teoricos
   memoria/4_Tecnicas_y_herramientas
   memoria/5_Aspectos_relevantes_del_desarrollo_del_proyecto
   memoria/6_Trabajos_relacionados
   memoria/7_Conclusiones_Lineas_de_trabajo_futuras

.. toctree::
   :caption: Anexos
   :name: anexos
   :maxdepth: 2

   anexos/A_Plan_proyecto
   anexos/B_Requisitos
   anexos/C_Diseno
   anexos/D_Manual_programador
   anexos/E_Manual_usuario
   anexos/F_Experimentos

.. toctree::
   :caption: Ayúdanos
   :name: ayúdanos

   anexos/CONTRIBUTING.rst

¿Estás buscando la documentación de la REST API? Puedes acceder a ella
`aquí <https://dmlls.github.io/jizt-tfg-api-docs>`__.