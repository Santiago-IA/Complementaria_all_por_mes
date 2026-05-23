# Proyecto de integracion SOFIA-LMS con python

**Version 4.2.3**

Esta version del Script esta diseñada en clases  y modularizada en función de los principios SOLID y CLEAN CODE, existe un archivo llamado script.py el cual sera encargado de inicializar el Orden de procesamiento y ejecutarlo actualmente funciona de a 1 registro, se debe indicar el indice de cambio del cual se va a iniciar a ejecutar, adicional se implemento la opcion de leer a partir de un archivo de excel para realizar el proceso de creación de las fichas este script migra procesos de un **programa de formación Complementaria Virtual y a Distancia enfocada especialmente en traer nuevos enrolamientos y crear las respectivas novedades corriendo por proceso interno o de manera descendente desde el ultimo indice de cambio**

## INFORMACIÓN DE EJECUCIÓN

Para poder que el script funcione se deben tener instaladas las librerias de

* cx_Oracle
* psycopg2
* openpyxl
* dotenv

se debe tener configurada la estructura en postgres con todo el esquema creado con sus respectivas foraneas que se encuentra en al carpeta estructuras db

### Para ejecutar el script se debe ejecutar de la siguiente forma:

En esta versión se cuenta con la opción de ejecutar el script desde INDICE_CAMBIO (SOFIA) o desde un documento XLSX para esto en la ejecución se debe tener en cuenta lo siguiente:

1. Si se quiere ejecutar el archivo de excel  (XLSX) se debe enviar solamente el parametro **--excel=s** sin más parametros.
2. Si se quiere ejecutar desde la tabla INDICE_CAMBIO (SOFIA) se deben enviar los siguientes parametros:

Este script tiene 3 versiones de ejecución:

* complementaria_va
* complementaria_va_update_aprendiz
* complementaria_va_update_instructor
* complementaria_va_excel

todos contienen lo mismo cambia es la forma de ejecutar cada uno ya que para enrolamiento se puede indicar si se desea recorrer los indices de cambio de sofia  solo se debe mandar **entity** o si se quiere traer los enrolamientos directos desde sofia correr con **internals** teniendo la forma de correr asi:

* complementaria_excel --excel=s
* complementaria_va_update_instructor --internal=s --entity=6
* complementaria_va_update_aprendiz --internal=s --entity=4
* complementaria_va_ficha --internal=s --entity=2

## ENTIDADES

**2** - Ficha de Caracterización (Curso)

**4** - Registro Académico (Curso - Usuario[aprendiz])

**6** - Intructor por ficha (Curso - Instructor[Funcionario])

## **REGISTROS QUE SE PROCESAN**

* Ficha Caracterización
* Registro Académico
* Instructores Por Ficha
* Resultados de Aprendizaje
* Competencias
* Competencias Por Program
* Persona
* Funcionario
* Línea Tecnológica
* Tecnologia de Red
* Nivel de Formación
* Instructor Responsable de Juicio
* Aprendiz por Detalle de Ruta

## CHANGELOG

### 4.2.3
Se adiciona mensaje de alerta para cuando la persona o funcionario no exista en oracle, tambien se elimina codigo repetido en instructor por ficha

### 4.2.2
Se ajusta las columnas de consulta de tiempo en internal process para que tome los tring de fecha como un date e incluya las fechas finales.

### 4.2.1
Se ajusta el logger de discord para que resuma todas las salidas del script a un archivo  txt  para posteriormente este ser enviando  a el chat de discord para su interpretación

### 4.2.0
Se adiciona logger de discord para que una vez los mensajes se impriman en pantalla estos sean enviados a un canal de discord

### 4.1.1
Se ajusta el error que salia en el metodo _update_enroll_record_if_need ya que no encontraba el registro academico y devolvia nulo  y no se interpreta como lista altraer su resultado

### 4.1.0

Se implementan las nuevas github actions para automatización y pruebas, se actualiza el registro academico e instructor por ficha para añadir una columna  con tipo de documento + numero de documento.

### 4.0.0

en esta versión del script se realizo una refactorización de código inicial, se crearon pruebas unitarias y análisis de código, tambien se implemento la nueva estructura de submodulos con el modulo BD leer readme del submodulo.

### 3.12.2

Se ajusta la consulta de fichas internas para que cuando se consulte por Aprendiz o instructor solo se incluyan las fichas en estado activo

### 3.12.1

Se adiciona nuevamente el metodo que verifica el enroll  para poder generar la novedad eliminado en la 3.11

### 3.12.0

Se crea servicio de migración del esquema temporal para las fichas que cuentan con aprendices en este esquema para que no se duplique

### 3.11.0

Se eliminan las funcionen de creacion enroll

### 3.10.1

Se añade parametro en consulta para en el InternalProcess traiga solo fichas en estados activos

### 3.10.0

Se elimina la entidad calificaciones ya que se trabaja en un script diferente, la clase RecordManager ahora extiende de QuerysDB para utilizar metodos de alli tambien y evitar inicializaciones innecesarias, adicional se realiza ajuste en todas las entidades para implementación del nuevo cambio

### 3.9.0

Se añade configuración de tiempo para espera para consultas iniciales del order process de 15 minutos y de select a oracle de 5 minutos en el QuerysDB

### 3.8.2

se añade configuración para que si el script ya se esta ejecutando no se ejecute nuevamente hasta que el primero no termine

### 3.8.1

Se cambia los queries en order process para que procesen desde el ultimo ICA_Id en sofia hasta la condición dada en el tiempo actualmente el 2023-10-1, se cambian los logging.info por print, se realiza ajuste en ficha, registro academico e instructor por ficha para realizar la respectiva novedad en caso de encontrarse, y si el registro es viable para el registro se adiciona.

### 3.8.0

Se realiza implementación de logger y traceback para hacer seguimiento a las diferentes excepciones, se implementa la logica de instructores para solo descargar los vigentes INF_ESTADO ='V', se realiza corrección de order_process ya que todos se ejecutan igual metiendolos en un diccionario, se cambia el nombre de la carpera  order a process

### 3.7.2

se realiza mejora en los enrolamientos, se añade novedad de enrolamiento de instructores, se realizan mejoras, se corrige problema del None en el apellido

### 3.7.1

Se realizo proceso de adicion de novedad de enrolamientos, para que cuando se traigan los registros de sofia se actualice el estado de acuerdo a lo procesado, debido a esto se añadio columna de visible para fichas y suspend para usuarios

### 3.6.2

Se mejoran las  excepciones para que guarden en histories, se crean variables de entorno para solo modificar un archivo, se ajusta el script para que baje solo titulada desde el 15 de marzo a partir de un ICA_ID especifico

### 3.6.1

Se creo una opccion adicional en el menu de excel (XLSX) para que descargue los resultados de aprendizaje de acuerdo al archivo de excel

### 3.6

Se creo un menu donde se indica si se debe ejecutar desde un archivo de excel (XLSX) o desde la tabla INDICE_CAMBIO (SOFIA).

### 3.5

Se crea funcion en order proces para traer un resultado por id, se crea menu en el order process para ejecutar el script con la entidad que se desee, se arreglan queries, se implementan las calificaciones en modulo independiente, se mejora tiempo de procesamiento pasando de  5:20m en 101 registros a 4:10m

### 3.4.1

Se refactorizo el codigo independizando la forma en como se extrae y se ingresan las calificaciones, permitiendo el ingreso de calificaciones desde la ficha o actualizando y creando la ficha desde indice de cambio

### 3.4

Se modifica nuevamente el archivo Order Process ya que estaba ejecuando muchos ciclos y se  paraba opr lo cual se decidio hacer una mezcla entre la version 2 del script y esta versión procesar solo fichas pero 1 a 1 mejor filtradas, se corrigen queries de diferentes consultar, se colocan diferentes print para saber en donde va el proceso,

### 3.3

Se modifica el archivo Order Process el cual se encarga de realizar el llamado 1 a 1 de los registros en la tabla indice de cmabio en Sofia, la mejora se realiza en pro de procesar mas cursos por proceso pasando a procesar por lotes de 50mil los registros que corresponden a las fichas

### 3.1

Se crean las clases de record manager, registro academico, e instructor por ficha para la creacion de todos los registros

### 3.0

Se creo un archivo de clase venia de trabajarse un archivo a punta de funciones
