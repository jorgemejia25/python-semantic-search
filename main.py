import streamlit as st
from io import StringIO
from vector_search import *
import qa
from utils import *


def main():
    """
    Función principal que se encarga de la interfaz de usuario y el procesamiento de consultas
    Muestra una página web donde el usuario puede elegir entre seleccionar un documento o hacer una pregunta.
    Si el usuario elige seleccionar un documento, se le solicita ingresar la URL del documento y se actualiza el corpus.
    Si el usuario elige hacer una pregunta, se le solicita ingresar la pregunta y se muestra la respuesta.
    Returns:
        None
    """
    st.header("Búsqueda semántica - Detectives Salvajes")
    url = False
    query = False
    options = st.radio(
        'Elije una opción',
        ('Hacer una pregunta', 'Seleccionar documento'))

    if 'Seleccionar documento' in options:
        url = st.text_input("Ingresa la URL del documento")

    if 'Hacer una pregunta' in options:
        query = st.text_input("Ingrese la pregunta")

    button = st.button("Enviar")

    if button and (url or query):
        if 'Seleccionar documento' in options:
            with st.spinner("Actualizando documento..."):
                corpusData = scrape_text_from_url(url)
                addData(corpusData, url)
                st.success("Documento actualizado")
        if 'Hacer una pregunta' in options:
            with st.spinner("Buscando respuesta..."):
                urls, res = find_match(query, 2)
                context = "\n\n".join(res)
                st.expander("Contexto").write(context)
                prompt = qa.create_prompt(context, query)
                answer = qa.generate_answer(prompt)
                st.success("Respuesta: "+answer)


main()
