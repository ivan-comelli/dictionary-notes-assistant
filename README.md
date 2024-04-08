# Script de Poblacion para Entrenamiento y Desarrollo de Asistente Personal de Inteligencia Artificial

## Tecnologia
Esto usando particularmente SQLALCHEMY como ORM por la necesidad de manejar una relacion entre modelos que, si bien no era ultra necesario me sirve para que sea escalable y evitar queries en codigo que afecten la facil comprension.
Tambien se planteo el uso de anotaciones estaticas para evitar fallas, ya que la ORM y Dash me estan reportando bastante problemas con incongruencia de datos.

## Estructura
    MODELOS: DOMAIN - ASPECT - SPRINTWORK - NOTE
    CONEXION y MIGRACION
    SYNC CSV DATA
    MERGE TABLES FOR DICTIONARY DATATABLE
    APP DASH LAYOUT
    CALLBACK MANAGEDATA

## Callback ManageData
    Por problemas de duplicados de outputs esto centrando todas las acciones en un solo callback para dash. Ademas de que es una pagina donde los cambios se guardan con un submit y no automaticamente. Lo veo eficaz pero poco practico en cuanto escalabilidad

    PROPS: ADDSPRINT - ADDNOTE - SAVE - SPRINTDATA - NOTEDATA - PREVSPRINTDATA - PREVNOTEDATA
    FORMAT TO DATAFRAMES
    UPDATE ALL DATA
    CHECK DELETED ROWS
    SERIAL TRIGGER: ADDSPRINT - ADDNOTE - SAVE

Se hizo un formateo de los datos para hacer mas sencillo el acondicionamiento de las salidas por la naturaleza dinamica de python

## Prompt de Generacion de CSV para el Diccionario Ontologico 
Tengo que indicar el Proposito el formato de los datos y la descripcion de cada columna

Primero que nada voy a usar git para manejar versiones del diccionario, por lo que tengo en mente el resultado de todo el modelo es un arbol jerarquico con atributos al final de las ramas.

La poblacion de este modelo es todo un reto porque su fuente proviene de una charla con un gpt y este devuelve csv que no se sabe si se repite o transgirveza la informacion. Por eso lo idea seria que nos manejemos con cierto contexto como para evitar los menores conflictos posibles. Basicamente una construccion estructurada, si bien al inicio podemos solicitar algo mas profundo y variado, ya para el afinamiento esto no es una opcion.
En cuanto al siguiente problema esta que tengo que buscar con el modulo a hacer merge contra el main que similitudes existen para evitar usar los mismos datos. Porque no puedo proveer de todos los datos del main a gpt para que intente no repetir, aunque aun asi falla por eso busco la manera de tener un roadmap como para evitar tener que usar tanto contexto sino mas bien algo estructurado en cuanto metadatos. En cuanto los conflictos no se van a encontrar textual por eso voy a buscar con un modelo NLP comparar los modelos a mergear e identificar quienes pueden ser un conflicto para solucionarlo.
Tambien me pongo pensar que voy a usar, modulos csv bien atomizado. Lo cual lo hace correcto usar git. O una base de datos con alguna funcion de versiones que debe de existir 

## Layout
Side Bar Navigation
    Dynamically Rendered Tab Content: Grafo - Commits "Muestra Id de Commit Actual posiblemente fecha" - Branch "Muestra Checkout actual" - Dictionary
        DataTable Dictionary & Input CSV Text with Submit Buttom -> Action drop Modal for Create and push commit
        DataTable Commits & Buttom RollBack to Commit
        DataTable Branch & Buttom Create Branch & Buttom Checkout Branch & Archive Branch
        Grafo Networkx
    Datatable Sprint Full edited and autosave - !Por el momento el sprint va se de un unico scrum
        Input Note with Submit
        !Esta seccion esta orientada a entender el contexto productivo y documentacion de notas
    DataTable Note Full edited and autosave - !Enfocado mas a la exploracion y Consulta



