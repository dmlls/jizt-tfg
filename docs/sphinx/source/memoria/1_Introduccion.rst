.. _introduccion:

============
Introducción
============

El término Inteligencia Artificial (IA) fue acuñado por primera vez en
la Conferencia de Dartmouth [crevier95]_ hace ahora 65 años, esto es,
en 1956. Sin embargo, ha sido en los últimos tiempos cuando su presencia
e importancia en la sociedad han crecido de manera exponencial.

Uno de los campos históricos dentro de la AI es el Procesamiento del
Lenguaje Natural (NLP, por sus siglas en inglés), cuya significación se
hizo patente con la aparición del célebre Test de Turing [turing50]_, en
el cual un interrogador debe discernir entre un humano y una máquina
conversando con ambos por escrito a través de una terminal.

Hasta los años 80, la mayor parte de los sistemas de NLP estaban basados
en complejas reglas escritas a mano [mccorduck79]_, las cuales
conseguían generalmente modelos muy lentos, poco flexibles y con baja
precisión. A partir de esta década, como fruto de los avances en
Aprendizaje Automático (*Machine Learning*), fueron apareciendo modelos
estadísticos, consiguiendo notables avances en campos como el de la
traducción automática.

En la última década, el desarrollo ha sido aún mayor debido a factores
como el aumento masivo de datos de entrenamiento (principalmente
provenientes del contenido generado en la *web*), avances en la
capacidad de computación (GPU, TPU, ASIC...) y el progreso dentro del
área de la Algoritmia [rahmfeld19]_.

No obstante, ha sido desde la aparición del concepto de "atención" en
2015 [luong15]_ [bahdanau16]_ [vaswani17]_ cuando el campo del NLP ha
comenzado a lograr resultados cuanto menos sorprendentes [macaulay20]_
[wiggers21]_.

Con todo, la mayor parte de estos avances se han visto limitados al
ámbito académico y corporativo. Los modelos cuyo código ha sido
publicado, o bien no están entrenados, o bien requieren para ser usados
conocimientos avanzados de matemáticas o programación, o simplemente son
demasiado grandes para ser ejecutados en ordenadores convencionales.

Con esta idea en mente, el objetivo de JIZT se centra en acercar los
modelos NLP del estado del arte tanto a usuarios expertos, como no
expertos.

Para ello, JIZT proporciona:

-  Una plataforma en la nube que expone una API
   REST a través de la cual se puede solicitar la generación de
   resúmenes. Esta opción está dirigida a usuarios con conocimientos
   técnicos, a través de la cual se pueden llevar a cabo tareas de NLP.

-  Una aplicación multiplataforma que consume dicha API, y que
   proporciona una interfaz gráfica sencilla e intuitiva. Esta
   aplicación puede ser utilizada por el público general, aunque no deja
   de ofrecer opciones avanzadas para aquellos usuarios con mayores
   conocimientos en la materia.

En un principio, dado el alcance de un Trabajo de Final de Grado, la
única tarea de NLP implementada ha sido la de generación de resúmenes,
aunque la arquitectura está diseñada para permitir la adición de otras
tareas de NLP en un futuro. La motivación detrás de la elección de la
generación de resúmenes se ha fundamentado principalmente en la relativa
menor popularidad de esta área frente a otras como la traducción
automática, el análisis de sentimientos, o los modelos conversacionales.
Para estas últimas tareas existe actualmente una amplia oferta de
grandes compañías como Google [cloudNL]_, IBM [watson]_, Amazon
[comprehend]_, o Microsoft [textAnalytics]_, entre muchas otras. Nuestra
mayor limitación reside en que los modelos pre-entrenados que
utilizaremos para la generación de los resúmenes funcionan únicamente en
inglés. Esperamos que en un futuro próximo aparezcan modelos que admitan
otros idiomas.

En un mundo en el que en cinco años se producirán globalmente 463
exabytes de información al día [raconteur19]_, siendo mucha de esa
información textual, las generación de resúmenes aliviará en cierto modo
el tratamiento de esos datos.

Sin embargo, gran parte del esfuerzo de desarrollo de JIZT se ha centrado en el diseño
de su arquitectura, la cual se describirá con detalle en el capítulo de
:ref:`chapter:conceptos-teoricos`. Por ahora adelantaremos que ha sido concebida con el
objetivo de ofrecer la mayor escalabilidad y flexibilidad posible, manteniendo además,
como indicábamos anteriormente, la capacidad de poder añadir otras tareas de NLP
diferentes de la generación de resúmenes próximamente.

Por todo ello, el presente TFG conforma el punto de partida de un
proyecto ambicioso, desafiante, pero con la certeza de que,
independientemente de su recorrido más allá del TFG, habremos aprendido,
disfrutado, y ojalá ayudado a alguien por el camino.

.. [crevier95] Daniel Crevier (1995). AI: The tumultuous history of the search for
   artificial intelligence. NY: Basic Books, 1993. 432 pp. (Reviewed by Charles
   Fair)Journal of the History of the Behavioral Sciences, 31(3), 273-278.

.. [turing50] Turing, A. (1950). Computing Machinery and IntelligenceMind, LIX(236),
   433-460.

.. [mccorduck79] McCorduck, P. (1979). Machines Who Think. W. H. Freeman and Co.

.. [rahmfeld19] Joachim Rahmfeld (2019). Recent Advances in Natural Language
   Processing. URL:
   `<https://damapdx.org/2019/08/23/september-2019-recent-advances-in-natural-language-processing-some-theory-applications>`__.
   Último acceso: 26/01/2021.

.. [luong15] Luong, C. (2015). Effective Approaches to Attention-based Neural Machine
   Translation. In Proceedings of the 2015 Conference on Empirical Methods in Natural
   Language Processing (pp. 1412–1421). Association for Computational Linguistics.

.. [bahdanau16] Dzmitry Bahdanau, Kyunghyun Cho, & Yoshua Bengio. (2016). Neural
   Machine Translation by Jointly Learning to Align and Translate. 

.. [vaswani17] Ashish Vaswani and Noam Shazeer and Niki Parmar and Jakob Uszkoreit and
   Llion Jones and Aidan N. Gomez and Lukasz Kaiser and Illia Polosukhin (2017).
   Attention Is All You NeedCoRR, abs/1706.03762.

.. [macaulay20] Thomas Macaulay. Someone let a GPT-3 bot loose on Reddit — it
   didn’t end well. Oct. de 2020. URL:
   `<https://thenextweb.com/neural/2020/10/07/someone-let-a-gpt-3-bot-loose-on-reddit-it-didnt-end-well>`__.
   Último acceso: 26/01/2021.

.. [wiggers21] Kyle Wiggers. AI models from Microsoft and Google already surpass human
   performance on the SuperGLUE language benchmark. Ene. de 2021. URL:
   `<https://venturebeat.com/2021/01/06/ai-models-from-microsoft-and-google-already-surpass-human-performance-on-the-superglue-language-benchmark>`__.
   Último acceso: 26/01/2021.

.. [cloudNL] Google. Cloud Natural Language. URL:
   `<https://cloud.google.com/natural-language>`__.
   Último acceso: 26/01/2021.

.. [watson] IBM. Watson. URL:
   `<https://www.ibm.com/watson/about>`__.
   Último acceso: 26/01/2021.

.. [comprehend] Amazon. Comprehend. URL:
   `<https://aws.amazon.com/es/comprehend>`__.
   Último acceso: 26/01/2021.


.. [textAnalytics] Microsoft. Text Analytics. URL:
   `<https://azure.microsoft.com/es-es/services/cognitive-services/text-analytics>`__.
   Último acceso: 26/01/2021.

.. [raconteur19] Raconteur. A Day in Data. 2019.
   `<https://www.raconteur.net/infographics/a-day-in-data>`__.
   Último acceso: 26/01/2021.
