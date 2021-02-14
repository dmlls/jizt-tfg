=====================
Trabajos relacionados
=====================
A continuación, enumeraremos algunos proyectos que guardan ciertas
similitudes con nuestro trabajo desarrollado.

Bert Extractive Summarizer
~~~~~~~~~~~~~~~~~~~~~~~~~~

Este proyecto *open-source* implementa un generador de resúmenes
extractivos haciendo uso del modelo BERT [devlin19]_ de
Google para la codificación de palabras, y aplicando *clústering* por
*k-means* para determinar las frases que se incluirán en el resumen.
Este proceso se detalla en [miller19]_.

El generador de resúmenes puede ser *dockerizado*, pudiéndose ejecutar
como servicio, proporcionando una REST API para solicitar la generación
de resúmenes. El autor ofrece *endpoints* gratuitos con limitaciones a
la hora de realizar peticiones, y *endpoints* privados de pago para
aquellos particulares o empresas que requieran de mayores prestaciones.

Se puede acceder al proyecto a través del siguiente enlace:
https://github.com/dmmiller612/bert-extractive-summarizer.

ExplainToMe
~~~~~~~~~~~

ExplainToMe es un proyecto también *open-source* centrado en la
generación de resúmenes extractivos de páginas *web*, permitiendo
cómodamente pegar y copiar el *link* de la *web* que se quiere resumir.

Emplea el algoritmo de TextRank [mihalce04]_, el cual a su
vez está inspirado en el conocido PageRank [page99]_, el
algoritmo basado en grafos que empleaba originalmente Google en su motor
de búsqueda. En su caso, TextRank aplica los principios del algoritmo de
Google a la extracción de las frases más importantes de un texto.

Como en el caso anterior, también implementa una API REST.

El proyecto no ha sido actualizado desde finales de 2018. Se puede
visitar a través de:
https://github.com/jjangsangy/ExplainToMe/tree/master.

SMMRY
~~~~~

Se trata de una de las primeras opciones que aparecen en los motores de
búsqueda a la hora de buscar «*summarizers*». También genera resúmenes
extractivos, aunque a diferencia de los anteriores, no es un proyecto
*open-source*.

Destacan su velocidad (*cachea* los textos resumidos recientemente), y
sus múltiples opciones de resumen, como por ejemplo: ignorar preguntas,
exclamaciones o frases entrecomilladas en el texto original, o la
generación de mapas de calor en función de la importancia de las frases
incluidas en el resumen.

Sin embargo, los resúmenes están compuestos de frases literales
ordenadas cronológicamente en función de su importancia, por lo que la
cohesión entre las mismas puede ser frágil e incluso, con frecuencia, se
habla de personas o entidades que no han sido introducidas previamente
en el resumen, pudiendo dificultar la comprensión del mismo.

En su página *web* no se explicita el algoritmo concreto que se emplea,
pero prestando atención a la descripción del proceso proporcionada
[smmry]_, parecen emplear igualmente PageRank.

Se puede acceder a SMMRY en:
https://smmry.com.

Tabla comparativa
~~~~~~~~~~~~~~~~~

En la siguiente tabla, se recoge un análisis de las características que
ofrece JIZT en comparación con las opciones introducidas anteriormente.

[tabla:comparativa]

.. container::
   :name: table:comparativa

   .. rst-class:: align-cols
   .. table:: Comparativa de las características ofrecidas por las diferentes alternativas para la generación de resúmenes.

         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Características            | `JIZT <https://www.jizt.it/>`__ | `Bert Extractive Summarizer <https://github.com/dmmiller612/bert-extractive-summarizer>`__ | `ExplainToMe <https://github.com/jjangsangy/ExplainToMe>`__ | `SMMRY <https://smmry.com/>`__ |
         +============================+=================================+============================================================================================+=============================================================+================================+
         | Tipo de resumen\ [1]_      |           Abstractivo           |                                         Extractivo                                         |                          Extractivo                         |           Extractivo           |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Tiempo resumen corto\ [2]_ |             ~20 seg.            |                                           ~6 seg                                           |                           ~9 seg.                           |             ~3 seg.            |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Tiempo resumen largo\ [3]_ |             ~4 min.             |                                     No disponible\ [4]_                                    |                            Error                            |             ~5 seg.            |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Ajustes básicos            |                ✅               |                                              ✅                                            |                              ✅                             |                ✅              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Ajustes avanzados          |                ✅               |                                              ❌                                            |                              ❌                             |                ✅              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Entrada: texto plano       |                ✅               |                                              ✅                                            |                              ❌                             |                ✅              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Entrada: URL               |           Próximamente          |                                              ❌                                            |                              ✅                             |                ✅              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Entrada: fichero           |           Próximamente          |                                              ❌                                            |                              ❌                             |                ✅              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Entrada: imagen            |           Próximamente          |                                              ❌                                            |                              ❌                             |                ❌              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Soporte multi-modelo\ [5]_ |           Próximamente          |                                              ❌                                            |                              ❌                             |                ❌              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Soporte multi-tarea\ [6]_  |           Próximamente          |                                              ❌                                            |                              ❌                             |                ❌              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | API REST                   |                ✅               |                                              ✅                                            |                              ✅                             |                ✅              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Arquitectura               |          Microservicios         |                                         Monolítica                                         |                          Monolítica                         |                ?               |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Plataforma                 |       Multiplataforma\ [7]_     |                                             Web                                            |                             Web                             |               Web              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | *Open-source*              |                ✅               |                                              ✅                                            |                              ✅                             |                ❌              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Gratuito                   |                ✅               |                                          Limitado                                          |                              ✅                             |            Limitado            |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+
         | Proyecto activo            |                ✅               |                                              ✅                                            |                              ❌                             |                ✅              |
         +----------------------------+---------------------------------+--------------------------------------------------------------------------------------------+-------------------------------------------------------------+--------------------------------+

.. [1]
   En los resúmenes *abstractivos*, se toman las frases literales del texto original.
   En los *extractivos*, se añaden palabras o expresiones nuevas.

.. [2]
   Texto de entrada con ~6.500 caracteres.

.. [3]
   Texto de entrada con ~90.000 caracteres.

.. [4]
   Texto de entrada con ~90.000 caracteres.

.. [5]
   Capacidad de generar resúmenes utilizando diferentes modelos.

.. [6]
   Capacidad de realizar otras tareas de NLP diferentes a la generación de resúmenes.

.. [7]
   Soporte nativo para Android, iOS y web. Pronto, soporte para Linux, macOS y Windows.

.. [devlin19]
   Jacob Devlin y col. BERT: Pre-training of Deep Bidirectional Transformers for
   Language Understanding. 2019. arXiv: 1810.04805 [cs.CL].


.. [miller19]
   Derek Miller. “Leveraging BERT for Extractive Text Summarization
   on Lectures”. En: CoRR abs/1906.04165 (2019). arXiv: 1906.04165. URL:
   `<http://arxiv.org/abs/1906.04165>`__.
   Último acceso: 04/02/2021.

.. [mihalce04]
   Rada Mihalcea y Paul Tarau. “TextRank: Bringing Order into Text.”
   En: jul. de 2004.

.. [page99]
   Lawrence Page y col. The PageRank Citation Ranking: Bringing Order to the Web.
   Technical Report 1999-66. Previous number = SIDL-WP-1999-0120. Stanford InfoLab,
   nov. de 1999.

.. [smmry]
   Smmry Team. Smmry. 2021. URL:
   `<https://smmry.com/about>`__.
   Último acceso: 04/02/2021.
