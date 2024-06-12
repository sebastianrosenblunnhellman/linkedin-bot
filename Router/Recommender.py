import random
import time
import os
from datetime import datetime
import csv

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Recommender:
    def __init__(self):
        self.service = Service(executable_path=ChromeDriverManager().install())
        self.driver = WebDriver(service=self.service)
        self.connections_made = 0  # Contador de conexiones realizadas

    def login(self, email, password):
        self.driver.get("https://www.linkedin.com/login")
        self.driver.implicitly_wait(10)

        email_field = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = self.driver.find_element(By.ID, "password")

        email_field.send_keys(email)
        password_field.send_keys(password)

        login_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()

        # Espera a que el login sea exitoso
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "global-nav-typeahead"))
        )

        print("Login successful")

    def recommend(self):
        # Navegar a la página del feed de LinkedIn
        self.driver.get("https://www.linkedin.com/feed/")
        time.sleep(5)  # Esperar a que la página del feed se cargue completamente

        while True:
            try:
                # Hacer scroll hacia abajo para cargar más contenido
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(2)  # Esperar a que se cargue el contenido

                # Obtener todos los botones de recomendar en el contenido recién cargado
                recommend_buttons = self.driver.find_elements(By.XPATH, '//span[text()="Recomendar"]/..')

                # Si no hay nuevos botones de recomendar, terminar el bucle
                if len(recommend_buttons) == 0:
                    break

                # Hacer clic en todos los botones de recomendar
                for button in recommend_buttons:
                    try:
                        button.click()
                        self.connections_made += 1
                        print("Recomendado")
                        time.sleep(random.randint(3, 9))  # Esperar un tiempo aleatorio entre 3 y 9 segundos
                    except Exception as e:
                        print(f"Error al recomendar: {e}")
            except Exception as e:
                print(f"Error al hacer scroll: {e}")
                break

        self.save_results()

    def save_results(self):
        data_dir = './data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        results = [timestamp, self.connections_made]

        file_path = os.path.join(data_dir, 'recommendation_results.csv')

        file_exists = os.path.exists(file_path)

        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['timestamp', 'recommendations_made'])  # Escribir encabezado si el archivo no existe
            writer.writerow(results)

        print(f"Results saved: {results}")

def run_recommender(email, password):
    bot = Recommender()
    bot.login(email, password)
    bot.recommend()


