import streamlit as st
from groq import Groq

st.set_page_config(page_title = "mi chat de ia", page_icon = ".v.")

st.title("mi primera aplicacion con streamlit")

nombre = st.text_input("decime tu nombre")

if st.button("saludar") :
    st.write(f"Hola {nombre}, bienvenido")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
      model=modelo,
      messages=[{"role": "user", "content": mensajeDeEntrada}],
      stream=True
)
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def configurar_pagina():
    # Agregamos un título principal a nuestra página
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración de la IA") # Creamos un sidebar con un título.
    elegirModelo =  st.sidebar.selectbox('Elegí un Modelo', options= MODELO, index=0)
    return elegirModelo

def actualizar_historial(rol, contenido, avatar) : 
    st.session_state.mensajes.append(
        {"role" : rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial() :
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat() :
    contenedorDelChat = st.container(height= 400, border= True)
    with contenedorDelChat :
        mostrar_historial()

def generar_respuesta(chat_completo):
      respuesta_completa = ""
      for frase in chat_completo:
          if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
      return respuesta_completa
def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()

    inicializar_estado()
    mensaje = st.chat_input("Escribí tu mensaje: ")
    area_chat()
    
    if mensaje:
        actualizar_historial("user", mensaje, "🧑‍💻")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

    if chat_completo:
        with st.chat_message("assistant"):
            respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
            actualizar_historial("assistant", respuesta_completa,"🤖")

    st.rerun()

if __name__ == "__main__":
    main()
    


# py -m streamlit run proyecto.py  
#  Local URL: http://localhost:8501
# Network URL: http://192.168.1.8:8501
#https://www.youtube.com/watch?v=XMvIAKcOJ_w
#python --version
#python -m pip install streamlit