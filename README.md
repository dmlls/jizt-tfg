<p align="center"><img width="400" src="https://github.com/dmlls/jizt/blob/main/img/readme/JIZT-logo.svg" alt="JIZT"></p>

<p align="center" display="inline-block">
  <a href="https://github.com/dmlls/jizt/actions?query=workflow%3A%22Deploy+to+GKE%22">
    <img src="https://github.com/dmlls/jizt/workflows/Deploy%20to%20GKE/badge.svg?branch=main" alt="Deploy to GKE">
  </a>
  <a href="https://docs.jizt.it">
    <img src="https://github.com/dmlls/jizt/actions/workflows/build-docs.yml/badge.svg" alt="Build & Publish docs">
  </a>
  <a href="https://deepsource.io/gh/dmlls/jizt/?ref=repository-badge">
    <img src="https://deepsource.io/gh/dmlls/jizt.svg/?label=active+issues" alt="Active Issues">
  </a>
  <a href="https://deepsource.io/gh/dmlls/jizt/?ref=repository-badge">
    <img src="https://deepsource.io/gh/dmlls/jizt.svg/?label=resolved+issues" alt="Resolved Issues">
  </a>
</p>

<h3 align="center">Servicio de Resumen de Textos con AI en la Nube</h3>
<br/> 

JIZT hace uso de los últimos avances en Lenguaje de Procesamiento Natural (NLP, por sus siglas en inglés), utilizando modelos de generación de lenguaje del estado del arte, como el modelo <a href="https://arxiv.org/abs/1910.10683">T5</a>, de Google, para proporcionar resúmenes precisos y completos.

## JIZT en 82 palabras

- JIZT genera resúmenes abstractivos, esto es, resúmenes que contienen palabras o expresiones que no aparecen en el texto original. Además, permite ajustar los parámetros del resumen, como por ejemplo su longitud o el método de generación a emplear.
- JIZT proporciona una API REST sustentada por un *backend* que implementa una arquitectura de microservicios dirigida por eventos (Kubernetes + Apache Kafka), a fin de proporcionar escalabilidad y alta disponibilidad. La documentación de la API REST es accesible a través de [docs.api.jizt.it](https://docs.api.jizt.it).
- Echa un vistazo a nuestra *app*. Disponible en [app.jizt.it](https://app.jizt.it) y a través de [Google Play](https://play.google.com/store/apps/details?id=it.jizt.app).

## Documentación del proyecto

Puedes acceder a la documentación del proyecto a través de [docs.jizt.it](https://docs.jizt.it).

## Contribuye

¿Quieres contribuir al proyecto? ¡Genial! En [CONTRIBUTING.md](https://github.com/dmlls/jizt/blob/main/CONTRIBUTING.md) encontrarás información de ayuda.

## ¿Y qué viene después?

En <a href="https://board.jizt.it/public/board/c08ea3322e2876652a0581e79d6430e2dc0c27720d8a06d7853e84c3cd2b">kanban.jizt.it</a> puedes encontrar información acerca de las tareas en las que estamos trabajando, y aquellas que se implementarán próximamente.

---

<div align="center">
  <span align="center"> <img width="150" class="center" src="https://github.com/dmlls/jizt/blob/main/img/readme/ministerio-logo.png" alt="Ministerio de Educación y Formación Profesional"></span>
  <p align="center" style="font-size:0.8em">Proyecto financiado gracias a la Beca de Colaboración del Ministerio de Educación y Formación Profesional</p>
</div>
