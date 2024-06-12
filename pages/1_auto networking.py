import streamlit as st
from Router.Networker import run_networker

# Crear la interfaz de usuario con Streamlit
st.title('LinkedIn Networker Bot')
st.write('Por favor, ingresa tus credenciales de LinkedIn y la URL de búsqueda.')

email = st.text_input('Correo electrónico')
password = st.text_input('Contraseña', type='password')
url = st.text_input('URL de LinkedIn')

if st.button('Iniciar Bot'):
    if email and password and url:
        run_networker(email, password, url)
        st.success('Proceso completado y resultados guardados.')
    else:
        st.error('Por favor, completa todos los campos.')
