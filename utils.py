import requests
from bs4 import BeautifulSoup


def get_html_content(url):
    """
    Esta función recibe una URL como parámetro y realiza una petición GET a esa URL utilizando la biblioteca
    requests de Python. Luego, devuelve el contenido HTML de la respuesta.

    :param url: una cadena que contiene la URL a la que se realizará la petición GET
    :return: el contenido HTML de la respuesta a la petición GET
    """
    # se realiza una petición GET a la URL dada
    response = requests.get(url)

    # se devuelve el contenido HTML de la respuesta
    return response.content


def get_plain_text(html_content):
    """
    Esta función recibe el contenido HTML de una página web como parámetro y devuelve el texto plano que se puede
    extraer de ella utilizando la biblioteca BeautifulSoup de Python. La función también elimina todos los elementos
    <script> del contenido HTML antes de extraer el texto.

    :param html_content: el contenido HTML de una página web
    :return: el texto plano extraído de la página web
    """
    # se utiliza BeautifulSoup para extraer el texto plano de la página web
    soup = BeautifulSoup(html_content, 'html.parser')
    for script in soup(["script"]):
        script.extract()
    # se devuelve el texto plano extraído
    return soup.get_text()


def split_text_into_chunks(plain_text, max_chars=2000):
    """
    Esta función recibe una cadena de texto como parámetro y la divide en trozos de longitud máxima dada por max_chars
    (2000 por defecto). La función devuelve una lista de cadenas que representan los trozos.

    :param plain_text: una cadena de texto que se dividirá en trozos
    :param max_chars: un entero que representa la longitud máxima de cada trozo (2000 por defecto)
    :return: una lista de cadenas que representan los trozos de la cadena de entrada
    """

    # se divide el texto en trozos de longitud máxima dada por max_chars
    text_chunks = []
    # se inicializa el trozo actual
    current_chunk = ""
    # se divide el texto en líneas
    # se recorre cada línea
    for line in plain_text.split("\n"):
        # si la longitud del trozo actual más la longitud de la línea más 1 es menor o igual que max_chars
        if len(current_chunk) + len(line) + 1 <= max_chars:
            # se añade la línea al trozo actual
            current_chunk += line + " "
        # si no
        else:
            # se añade el trozo actual a la lista de trozos
            text_chunks.append(current_chunk.strip())
            # se inicializa el trozo actual
            current_chunk = line + " "
    # se añade el trozo actual a la lista de trozos
    if current_chunk:
        # se añade el trozo actual a la lista de trozos
        text_chunks.append(current_chunk.strip())
    # se devuelve la lista de trozos
    return text_chunks


def scrape_text_from_url(url, max_chars=2000):
    """
    Esta función recibe una URL como parámetro y devuelve una lista de cadenas que representan el contenido de la
    página web correspondiente. La función utiliza las funciones get_html_content, get_plain_text y
    split_text_into_chunks para obtener el contenido de la página web, extraer el texto plano y dividirlo en trozos.

    :param url: una cadena que contiene la URL de la página web que se va a raspar
    :param max_chars: un entero que representa la longitud máxima de cada trozo de texto (2000 por defecto)
    :return: una lista de cadenas que representan el contenido de la página web dividido en trozos de longitud máxima
    """
    # se obtiene el contenido HTML de la página web
    html_content = get_html_content(url)
    # se obtiene el texto plano de la página web
    plain_text = get_plain_text(html_content)
    # se divide el texto en trozos de longitud máxima dada por max_chars
    text_chunks = split_text_into_chunks(plain_text, max_chars)
    # se devuelve la lista de trozos
    return text_chunks
