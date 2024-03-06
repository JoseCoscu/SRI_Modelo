from collections import defaultdict
import numpy as np
import os
import spacy
import nltk


def load_files():
    # Ruta al directorio que contiene los archivos de texto
    directorio = "../../data"

    # Lista para almacenar el contenido de los archivos
    files = []

    # Itera sobre cada archivo en el directorio
    for archivo in os.listdir(directorio):
        if archivo.endswith(".txt"):  # Asegúrate de que sea un archivo de texto
            ruta_archivo = os.path.join(directorio, archivo)
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
                files.append(contenido.lower())
    return files


def process_docs(docs, use_lemmatization=True):
    nlp = spacy.load("es_core_news_sm")  # Lenguaje
    docs_tokens = [[token for token in nlp(doc)] for doc in docs]  # Tokenizacion
    docs_tokens = [[token for token in doc if token.is_alpha] for doc in docs_tokens]
    stopwords = spacy.lang.es.stop_words.STOP_WORDS
    docs_tokens = [[token for token in doc if token.text not in stopwords] for doc in docs_tokens]
    stemmer = nltk.stem.PorterStemmer()
    docs_tokens = [[token.lemma_ if use_lemmatization else stemmer.stem(token.text) for token in doc] for doc in
                   docs_tokens]

    return docs_tokens


def construir_matriz_termino_documento(lista_documentos):
    # Paso 1: Crear un vocabulario único
    vocabulario = set()
    for documento in lista_documentos:
        vocabulario.update(documento)

    # Paso 2: Asignar un índice a cada palabra en el vocabulario
    vocabulario_dict = {palabra: indice for indice, palabra in enumerate(vocabulario)}

    # Paso 3: Crear la matriz término-documento
    matriz_td = np.zeros((len(vocabulario), len(lista_documentos)), dtype=int)

    # Paso 4: Contar la frecuencia de términos en cada documento
    for indice_doc, documento in enumerate(lista_documentos):
        frecuencia_palabras = defaultdict(int)
        for palabra in documento:
            frecuencia_palabras[palabra] += 1
        for palabra, frecuencia in frecuencia_palabras.items():
            matriz_td[vocabulario_dict[palabra], indice_doc] = frecuencia

    return matriz_td, vocabulario_dict


def aplicar_SVD(matriz_td, k):
    """
    Aplica la descomposición en valores singulares (SVD) a una matriz términos-documentos.

    Parámetros:
        - matriz_td: La matriz términos-documentos.
        - k: El número de dimensiones a mantener después de la reducción.

    Retorna:
        - U_red: La matriz U reducida.
        - S_red: Los valores singulares reducidos.
        - VT_red: La matriz VT reducida.
    """
    U, S, VT = np.linalg.svd(matriz_td, full_matrices=False)

    # Reducir la dimensionalidad
    U_red = U[:, :k]
    S_red = np.diag(S[:k])
    VT_red = VT[:k, :]

    return U_red, S_red, VT_red


def procesar_consulta(consulta, U_red, S_red, VT_red, vocabulario_dict, lista_documentos, num_documentos_a_recuperar=5):
    """
    Procesa una consulta utilizando la descomposición SVD de la matriz término-documento.

    Parámetros:
        - consulta: La consulta como una lista de palabras.
        - U_red: La matriz U reducida obtenida de la descomposición SVD.
        - S_red: La matriz S reducida obtenida de la descomposición SVD.
        - VT_red: La matriz VT reducida obtenida de la descomposición SVD.
        - vocabulario_dict: El diccionario que asigna un índice a cada palabra en el vocabulario.
        - lista_documentos: La lista de documentos originales.
        - num_documentos_a_recuperar: El número de documentos más relevantes a recuperar.

    Retorna:
        - documentos_relevantes: Los documentos más relevantes para la consulta.
    """
    # Representar la consulta en el espacio reducido
    consulta_vector = np.zeros(len(vocabulario_dict))
    for palabra in consulta[0]:
        if palabra in vocabulario_dict:
            consulta_vector[vocabulario_dict[palabra]] += 1
    consulta_proyectada = np.dot(np.dot(U_red.T, consulta_vector), np.linalg.inv(S_red))

    # Calcular similitud con cada documento en el espacio reducido
    similitudes = np.dot(consulta_proyectada, VT_red)

    # Ordenar los documentos por relevancia
    indices_documentos_ordenados = np.argsort(similitudes)[::-1]

    # Recuperar los documentos más relevantes
    documentos_relevantes = [i for i in indices_documentos_ordenados[:num_documentos_a_recuperar]]

    return documentos_relevantes


# Ejemplo de uso

consulta = 'Naturaleza bella divina y amplia'

consulta = process_docs([consulta])

k = 20

docs = load_files()
t_docs = process_docs(docs)
matriz_td, vocabulario_dict = construir_matriz_termino_documento(t_docs)

U_red, S_red, VT_red = aplicar_SVD(matriz_td, k)

documentos_relevantes = procesar_consulta(consulta, U_red, S_red, VT_red, vocabulario_dict, docs, 4)

for i in documentos_relevantes:
    print(f"Documento {i + 1}")
    print(docs[i][0:100] + '...')

