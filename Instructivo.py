# Importar librerías
import streamlit as st

# Crear página
st.set_page_config(page_title="Inicio", page_icon=":globe_with_meridians:")

# Agregar un encabezado y un subencabezado a la página web
st.title("¡Bienvenido a LinkedIn-Bot 1.0!")
st.subheader("Aquí encontrarás un instructivo detallado de las funcionalidades de nuestra app")

# Descripción de funcionalidades

## Auto Networking
st.header("Auto Networking")
st.write("""
La función de auto networking permite enviar solicitudes de conexión automáticamente a personas en LinkedIn. 
El bot envía aleatoriamente entre 25 y 50 solicitudes de conexión, y en cada acción automática que realiza, 
espera de manera aleatoria entre 3 y 9 segundos. Por lo tanto, el bot puede tardar algunos minutos en realizar 
todas las solicitudes de conexión. Esto se lleva a cabo de esta forma para asegurarnos de que LinkedIn no detecte 
esta actividad como realizada por un bot.

### Requisitos
1. Tener Google Chrome instalado y configurado en idioma español.
2. Al colocar la URL solicitada, debe ser producto de ir a la barra de búsqueda de LinkedIn, buscar el tipo de personas 
que se desea agregar (ejemplo: analista de datos), luego ir al filtro que se despliega en la sección superior, seleccionar 
"Personas" y finalmente copiar y pegar la URL.
""")

# Mostrar la imagen EJEMPLO
st.image('./assets/screenshot.png')


## Auto Recomendaciones
st.header("Auto Recomendaciones")
st.write("""
La función de auto recomendaciones permite realizar recomendaciones automáticas (el equivalente a un "Like") a publicaciones 
y comentarios del feed en LinkedIn. El bot solo solicita las credenciales de acceso y comienza automáticamente.

### Descarga y Ejecución
Si por motivos de seguridad deseas descargar y ejecutar en tu propia máquina el código fuente de la app, puedes hacerlo desde 
el siguiente enlace: [LinkedIn-Bot](https://github.com/sebastianrosenblunnhellman/linkedin-bot)

### Colaboraciones y Mejoras
El proyecto está abierto a colaboraciones y mejoras. Las próximas mejoras que vamos a realizar al código incluirán la 
posibilidad de guardar en el propio navegador la actividad del bot y poder visualizarla a través de un dashboard.
""")
