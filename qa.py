# Description: Este archivo contiene las funciones que se utilizan para generar respuestas a las consultas de los usuarios.
import openai
# Configuración de la API de OpenAI
openai.api_key = "<<API_KEY>>"


def create_prompt(context, query):
    """
    Esta función recibe un contexto y una consulta como cadenas y devuelve una cadena que puede ser utilizada como
    entrada para la función generate_answer. La cadena de salida incluye el contexto y la consulta, y un encabezado
    que indica al usuario cómo responder a la consulta.

    :param context: una cadena que representa el contexto en el que se basa la consulta
    :param query: una cadena que representa la consulta que se va a responder
    :return: una cadena que se puede utilizar como entrada para la función generate_answer
    """

    # encabezado que se muestra al usuario para indicarle cómo responder a la consulta
    header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    return header + context + "\n\n" + query + "\n"


def generate_answer(prompt):
    """
    Esta función recibe una cadena como entrada y utiliza la API de OpenAI para generar una respuesta en función del
    contenido de la cadena de entrada. La función devuelve la respuesta generada como una cadena.

    :param prompt: una cadena que se utilizará para generar la respuesta utilizando la API de OpenAI
    :return: una cadena que representa la respuesta generada por la API de OpenAI
    """

    # se utiliza la API de OpenAI para generar una respuesta
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[' END']
    )
    # se devuelve la respuesta generada
    return (response.choices[0].text).strip()
