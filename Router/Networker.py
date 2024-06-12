import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import random
import time
import csv
from datetime import datetime
import os
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Networker:
    def __init__(self):
        try:
            # Opciones para el modo sin cabeza
            firefox_options = Options()
            firefox_options.add_argument("--headless")
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-dev-shm-usage")
            firefox_options.add_argument("--disable-gpu")
            firefox_options.add_argument("--window-size=1920,1080")
            
            # Inicializa el servicio para GeckoDriver
            self.service = Service(executable_path=GeckoDriverManager().install())
            # Inicializa el controlador de Firefox
            self.driver = webdriver.Firefox(service=self.service, options=firefox_options)
            # Genera un número aleatorio de conexiones objetivo entre 25 y 50
            self.target_connections = random.randint(25, 50)
            self.connections_made = 0  # Contador de conexiones realizadas
        except Exception as e:
            logging.error(f"Error al iniciar el controlador de Firefox: {e}")
            raise

    def login(self, email, password):
        try:
            # Navega a la página de inicio de sesión de LinkedIn
            self.driver.get("https://www.linkedin.com/login")
            self.driver.implicitly_wait(10)

            # Espera hasta que el campo de correo electrónico esté presente
            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            # Encuentra el campo de la contraseña
            password_field = self.driver.find_element(By.ID, "password")

            # Introduce las credenciales de inicio de sesión
            email_field.send_keys(email)
            password_field.send_keys(password)

            # Encuentra y hace clic en el botón de inicio de sesión
            login_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button.click()

            # Espera a que el login sea exitoso
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "global-nav-typeahead"))
            )

            logging.info("Login successful")
        except Exception as e:
            logging.error(f"Error al iniciar sesión en LinkedIn: {e}")
            self.driver.quit()
            raise

    def networking(self, urls):
        for url in urls:
            if self.connections_made >= self.target_connections:
                break
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            while self.connections_made < self.target_connections:
                try:
                    # Esperar hasta que los botones de conectar estén presentes
                    connect_buttons = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//button[contains(@aria-label, "conectar")]'))
                    )
                    # Intentar encontrar y hacer clic en un botón de conectar
                    for button in connect_buttons:
                        if self.connections_made >= self.target_connections:
                            break
                        try:
                            button.click()
                            # Espera hasta que el botón "Enviar sin nota" aparezca y haz clic en él
                            send_without_note_button = WebDriverWait(self.driver, 20).until(
                                EC.element_to_be_clickable((By.XPATH, '//span[text()="Enviar sin nota"]/..'))
                            )
                            send_without_note_button.click()
                            self.connections_made += 1  # Incrementar contador de conexiones realizadas
                            # Espera de un tiempo aleatorio entre 3 y 9 segundos entre cada acción de conexión
                            time.sleep(random.randint(3, 9))
                        except Exception as e:
                            logging.warning(f"Error al hacer clic en conectar o enviar sin nota: {e}")
                except Exception as e:
                    logging.warning(f"Error al buscar botones de conectar: {e}")
                # Hacer clic en el botón "Siguiente" si no se han realizado el número objetivo de conexiones
                if self.connections_made < self.target_connections:
                    try:
                        next_button = WebDriverWait(self.driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Siguiente"]'))
                        )
                        next_button.click()
                    except Exception as e:
                        logging.warning(f"Error al hacer clic en el botón Siguiente: {e}")
                        break
            logging.info(f"Conexiones solicitadas: {self.connections_made}")

    def save_results(self):
        try:
            # Obtiene la fecha y hora actual
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = [timestamp, self.connections_made]
            # Define el directorio de salida
            output_dir = './data'
            os.makedirs(output_dir, exist_ok=True)
            # Define la ruta del archivo de resultados
            file_path = os.path.join(output_dir, 'networking_results.csv')

            # Guarda los resultados en un archivo CSV
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Connections Made"])
                writer.writerow(data)

            logging.info(f"Results saved to {file_path}")
        except Exception as e:
            logging.error(f"Error al guardar los resultados: {e}")
            raise

def run_networker(email, password, url):
    try:
        # Crea una instancia de la clase Networker
        bot = Networker()
        # Inicia sesión en LinkedIn
        bot.login(email, password)
        # Realiza la red de conexiones
        bot.networking([url])
        # Guarda los resultados
        bot.save_results()
    except Exception as e:
        logging.error(f"Error al ejecutar el Networker: {e}")

# Interfaz de Streamlit
st.title("LinkedIn Networker Bot")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
url = st.text_input("URL de búsqueda de LinkedIn")

if st.button("Iniciar Bot"):
    if email, password, url:
        run_networker(email, password, url)
        st.success("Proceso completado y resultados guardados.")
    else:
        st.error("Por favor, completa todos los campos.")
