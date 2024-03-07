#### Autores
Ovidio Navarro Pazos   
Jesus Armando Padron  
Juan Jose Muñoz Noda  

#### Definicion del modelo
Se desarrolló el ``Modelo de Indexación de Semántica Latente``(ISL) que es un método de indexación y recuperación que utiliza un método numérico llamado descomposición en valores singulares (SVD) para identificar patrones en las relaciones entre los términos contenidos en una colección de textos no estructurados



#### Explicación de la solucion desarrollada
Primero se realiza el prepocesamiento de los documentos extrallendo los documentos, eliminado las stop-words, se realiza el stemming dejando las palabras a su raiz o forma básica.   
Se crea la Matriz término-documento donde los terminos del vocabulario conforman las columnas y los documentos las filas ,asignandole un peso a cada termino en cada documento, se tomó  como peso la frecuencia del termino el en documento  
Después se realiza la descomposicón en valores singulares(principal objetivo de ISL)
descomponiendo la matriz C (matriz término-documento) en C=USV^t donde :  

- U: es una matriz cuyas columnas son vectores propios ortogonales de CC^T . Representa los términos en el espacio de términos.
- V:  es una matriz cuyas columnas son vectores propios ortogonales de C^tC. Representa los documentos en el espacio de documentos.
- S: matriz diagonal que posee los valores singulares que son numeros que representan la importancia de cada concepto latente
  
Al igual que los documentos , se le hace el mmismo preposesamiento y se representa la consulta en el espacio de características latente. Esto se logra multiplicando el vector de la consulta por la traspuesta de la matriz U y después el resultado se multiplica por la inversa de la matriz S

Se realiza la similitud del coseno por ada documento y se extraen los 4 mejores