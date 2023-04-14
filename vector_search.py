import pinecone
from sentence_transformers import SentenceTransformer, util

# Inicializar el modelo SentenceTransformer
# En este caso, se utiliza el modelo "all-MiniLM-L6-v2"
model = SentenceTransformer('all-MiniLM-L6-v2')

# Inicializar la API de Pinecone con una clave de API válida
# y especificar el entorno de Pinecone (en este caso, "asia-southeast1-gcp")
pinecone.init(api_key="ff0dd7c3-f502-4a2b-bfaa-c92a814cd0d2",
              environment="asia-southeast1-gcp")

# Crear un índice en Pinecone llamado "demo-tei"
index = pinecone.Index("demo-tei")


def addData(corpusData, url):
    """
    Agregar nuevos datos al índice Pinecone.

    Parameters
    ----------
    corpusData : list of str
        Lista de cadenas de texto que representan el contenido que se agregará al índice.
    url : str
        Cadena de texto que representa la URL de donde proviene el contenido.

    Returns
    -------
    None
    """
    # Obtener el número total de vectores ya presentes en el índice.
    # Esto se utiliza para asignar un ID único a cada nueva entrada.
    id = index.describe_index_stats()['total_vector_count']

    # Iterar a través de cada elemento en corpusData.
    for i in range(len(corpusData)):
        # Obtener el contenido actual.
        chunk = corpusData[i]

        # Crear una tupla que contenga el ID único, la codificación del modelo,
        # y los metadatos (título, contexto y URL).
        chunkInfo = (str(id+i),
                     model.encode(chunk).tolist(),
                     {'title': url, 'context': chunk})

        # Agregar la tupla al índice Pinecone.
        index.upsert(vectors=[chunkInfo])


def find_match(query, k):
    """
    Realizar una búsqueda en el índice Pinecone.

    Parameters
    ----------
    query : str
        Cadena de texto que representa la consulta de búsqueda.
    k : int
        Número máximo de resultados que se devolverán.

    Returns
    -------
    titles : list of str
        Lista de títulos que corresponden a los vectores más cercanos encontrados en el índice.
    contexts : list of str
        Lista de contextos que corresponden a los vectores más cercanos encontrados en el índice.
    """
    # Codificar la consulta utilizando el modelo SentenceTransformer.
    query_em = model.encode(query).tolist()

    # Realizar una búsqueda en el índice Pinecone para encontrar los vectores más cercanos.
    result = index.query(query_em, top_k=k, includeMetadata=True)

    # Extraer los títulos y contextos de los vectores más cercanos encontrados en el índice.
    titles = [result['matches'][i]['metadata']['title'] for i in range(k)]
    contexts = [result['matches'][i]['metadata']['context'] for i in range(k)]

    # Devolver los resultados.
    return titles, contexts
