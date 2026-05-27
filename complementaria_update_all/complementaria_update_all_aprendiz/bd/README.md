# **Modulo BD:**

**Version 1.0.0**

Este es el modulo de BD utilizados a lo largo de los diferentes scripts de base de datos como lo son rectificación de fichas, titulada_va, complementatia etc, debido a que se utiliza en tantos proyectos se establece como modulo para ser importado y que todos los scripts hereden de este para que todos los cambios se apliquen independientemente del script.

## Requisitos Previos:

Para poder que el script funcione se deben tener instaladas las librerias de
cx_Oracle
psycopg2
openpyxl
dotenv

## IMPLEMENTACIÓN

Este documento proporciona instrucciones para implementar el módulo de base de datos, permitiendo la conexión a la base de datos y la ejecución de consultas. Sigue los pasos a continuación al inicializar cada proyecto o al realizar cambios en el submódulo:

### Integración del módulo

Para integrar el módulo de base de datos en tu proyecto, ejecuta el siguiente comando:

`git submodule add git@github.com:CrisCano11/bd.git`

### **Actualización del módulo**

Para actualizar el submódulo a la versión más reciente, utiliza el siguiente comando:

`git submodule update --remote`

### Estructura de Importaciones

Al realizar importaciones, asegúrate de seguir la siguiente estructura:

* bd/db/`<nombre archivo>`

### Ajustes en `script.py`

En el archivo inicial de algunos proyectos (`script.py`), es necesario añadir la siguiente línea para cargar todas las carpetas del submódulo y que Python las reconozca:

```
import sys
import os
sys.path.append(os.path.join(os.path.dirname(file), 'bd'))
```

### Ajustes en `queries.py`

El archivo `queries.py` del módulo importa consultas de la siguiente dirección, que debe estar en la raíz del proyecto:

`sql/queries.py`

Para mayor claridad y evitar confusiones, todas las funciones importadas de `queries.py` serán referenciadas desde:

`bd/db/queries.py`

Nota: todo esto generara un archivo en la raiz del proyecto llamada .gitmodules, si en la carpeta bd  no se encuentra ningun archivo se debe ejecutar los siguientes comando para que se actualicen los respectivos archivos.

```
git submodule init
git submodule update
```

## Changelog

### 1.1.0

Se cambia el archivo de queries para que realice importación de un archivo de cada proyecto, adicional se ajustan las pruebas automaticas

### 1.0.0

Se separa de los script y se vuelve un modulo para importarse en todos los scripts.
