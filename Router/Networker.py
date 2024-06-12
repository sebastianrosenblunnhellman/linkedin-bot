# Importación de las bibliotecas necesarias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import csv
from datetime import datetime
import os


class Networker:
    def __init__(self):
        # Inicializa el servicio para ChromeDriver
        self.service = Service(executable_path=ChromeDriverManager().install())
        # Inicializa el controlador de Chrome
        self.driver = webdriver.Chrome(service=self.service)
        # Genera un número aleatorio de conexiones objetivo entre 25 y 50
        self.target_connections = random.randint(25, 50)
        self.connections_made = 0  # Contador de conexiones realizadas

    def login(self, email, password):
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

        print("Login successful")

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
                            print(f"Error al hacer clic en conectar o enviar sin nota: {e}")
                except Exception as e:
                    print(f"Error al buscar botones de conectar: {e}")
                # Hacer clic en el botón "Siguiente" si no se han realizado el número objetivo de conexiones
                if self.connections_made < self.target_connections:
                    try:
                        next_button = WebDriverWait(self.driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Siguiente"]'))
                        )
                        next_button.click()
                    except Exception as e:
                        print(f"Error al hacer clic en el botón Siguiente: {e}")
                        break
            print(f"Conexiones solicitadas: {self.connections_made}")

    def save_results(self):
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

        print(f"Results saved to {file_path}")

def run_networker(email, password, url):
    # Crea una instancia de la clase Networker
    bot = Networker()
    # Inicia sesión en LinkedIn
    bot.login(email, password)
    # Realiza la red de conexiones
    bot.networking([url])
    # Guarda los resultados
    bot.save_results()