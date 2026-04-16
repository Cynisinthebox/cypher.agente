import streamlit as st
from langfuse import Langfuse
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="Cypher - AI Agent", page_icon="🕵️‍♂️")

# Inicializar Langfuse y OpenAI (Se configuran en Streamlit Cloud más tarde)
langfuse = Langfuse()
client = OpenAI()

st.title("🕵️‍♂️ Cypher: Tu Agente de Ciberseguridad")
st.write("*Amable, experto y con un humor... cuestionable.*")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Crear traza en Langfuse para el reto
    trace = langfuse.trace(name="cypher_chat", user_id="cynthia_user")

    with st.chat_message("assistant"):
        # Instrucciones de personalidad
        system_prompt = (
            "Eres Cypher, un experto en ciberseguridad amable y servicial. "
            "Hablas perfectamente el idioma en el que se te hable (español, inglés, etc.). "
            "Siempre cuentas un chiste malo de tecnología al final de tus respuestas. "
            "Eres profesional pero muy bromista."
        )
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ]
        )
        
        full_response = response.choices[0].message.content
        st.markdown(full_response)
        
        # Guardar en Langfuse
        trace.generation(
            name="cypher_response",
            input=prompt,
            output=full_response
        )

    st.session_state.messages.append({"role": "assistant", "content": full_response})

