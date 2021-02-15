# Bienvenido a la documentación de JIZT

La documentación está disponible a través de [docs.jizt.it](https://docs.jizt.it). No
obstante, si quieres compilar la documentación en local, debes seguir los pasos
indicados a continuación.

## Prerrequisitos

Para compilar la documentación, primero tienes que instalar los módulos de Python
necesarios. Para ello, ejecuta el siguiente comando:

```bash
pip install -r requirements.txt
```

## Compilar la documentación

Una vez instalados todos los prerrequisitos, puedes compilar la documentación
ejecutando el siguiente comando en el directorio `/docs`:

```bash
make html
```

Se creará un directorio con el nombre `_build/html`. Puedes abrir el fichero
`_build/html/index.html` desde tu navegador para ver la documentación.

**NOTE**: Si quieres modificar la documentación, y vas a añadir/eliminar elementos del
toc-tree o de cualquier elemento estructural, se recomienda limpiar el directorio
`_build` antes de volver a compilar la documentación. Para ello, puedes ejectuar el
siguiente comando:

```bash
make clean && make html
```
