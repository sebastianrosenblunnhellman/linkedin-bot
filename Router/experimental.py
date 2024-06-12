import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException,
    WebDriverException,
    ElementClickInterceptedException,
    NoSuchWindowException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

class LinkBot:
    def __init__(self, email, password, job_url):
        self.driver = None
        self.service = None
        self.email = email
        self.password = password
        self.job_url = job_url
        self.start_browser()
        self.login()
        self.apply_to_jobs()

    def start_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--start-maximized")

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver.implicitly_wait(10)

    def login(self):
        try:
            self.driver.get("https://www.linkedin.com/login")
            email_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_field = self.driver.find_element(By.ID, "password")

            email_field.send_keys(self.email)
            password_field.send_keys(self.password)

            login_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button.click()

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "global-nav-typeahead"))
            )

            print("Login successful")
        except (NoSuchWindowException, WebDriverException):
            print("WebDriverException during login, reconnecting...")
            self.reconnect()
        except Exception as e:
            print(f"Exception during login: {str(e)}")

    def apply_to_jobs(self):
        self.driver.get(self.job_url)
        
        while True:
            try:
                self.apply_easy_apply_filter()
                jobs = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//button[contains(@aria-label, "Solicitud sencilla")]'))
                )
                for job in jobs:
                    try:
                        self.driver.execute_script("arguments[0].scrollIntoView();", job)
                        ActionChains(self.driver).move_to_element(job).perform()

                        WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(job)
                        )
                        job.click()
                        time.sleep(random.uniform(3, 6))
                        self.fill_application_form()
                        self.review_and_submit_application()
                        print("Successfully applied to a job.")
                    except Exception as e:
                        print(f"Failed to apply to a job: {e}")
                        continue  # Continue with the next job in case of an error
            
                try:
                    next_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Siguiente"]'))
                    )
                    next_button.click()
                    time.sleep(random.uniform(3, 6))
                except TimeoutException:
                    print("No more pages to navigate.")
                    break
            except Exception as e:
                print(f"Error navigating job listings: {e}")
                break

    def apply_easy_apply_filter(self):
        try:
            # Find and click the "Solicitud sencilla" filter button
            easy_apply_filter = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Filtro «Solicitud sencilla»")]'))
            )
            if easy_apply_filter.get_attribute("aria-checked") == "false":
                easy_apply_filter.click()
                time.sleep(random.uniform(3, 6))
                print("Easy Apply filter applied.")
            else:
                print("Easy Apply filter already applied.")
        except TimeoutException:
            print("Easy Apply filter not found or already applied.")
        except Exception as e:
            print(f"Error applying Easy Apply filter: {e}")

    def reconnect(self):
        try:
            self.driver.quit()
        except:
            pass
        self.start_browser()
        self.login()

    def fill_application_form(self):
        def click_next_button():
            try:
                next_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="Siguiente"]/..'))
                )
                next_button.click()
                print("'Next' button clicked")
                time.sleep(random.uniform(3, 6))
            except ElementClickInterceptedException:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    self.driver.execute_script("arguments[0].click();", next_button)
                    print("'Next' button clicked using JavaScript")
                    time.sleep(random.uniform(3, 6))
                except Exception as e:
                    print(f"Error clicking 'Next' button using JavaScript: {str(e)}")
            except (WebDriverException, NoSuchElementException):
                print("WebDriverException or NoSuchElementException while clicking 'Next' button, reconnecting...")
                self.driver.save_screenshot("click_next_button_error.png")
                self.reconnect()

        click_next_button()
        click_next_button()

        form_groups = self.driver.find_elements(By.CLASS_NAME, 'jobs-easy-apply-form-section__grouping')
        for group in form_groups:
            questions = group.find_elements(By.XPATH, './/label')
            for question in questions:
                try:
                    label_text = question.text.lower()
                    input_element = group.find_element(By.ID, question.get_attribute("for"))
                    self.answer_question(label_text, input_element)
                    time.sleep(random.uniform(3, 6))
                except Exception as e:
                    print(f'Error processing question: {question.text}. Error: {str(e)}')

        print("Form filled according to the rules.")
        self.review_and_submit_application()

    def answer_question(self, label_text, input_element):
        input_type = input_element.get_attribute('type')
        try:
            if input_type == 'radio' or input_type == 'checkbox':
                if 'yes' in input_element.getAttribute('value').lower():
                    input_element.click()
                    print(f'Answered YES to: {label_text}')
            elif input_type == 'text' or input_type == 'number':
                if 'remuneración' in label_text or 'bruta' in label_text or 'pretendida' in label_text:
                    input_element.send_keys('500000')
                    print(f'Entered 500000 for: {label_text}')
                elif 'años' in label_text or 'experiencia' in label_text:
                    input_element.send_keys('2')
                    print(f'Entered 2 for: {label_text}')
                elif '1' in label_text and '5' in label_text:
                    input_element.send_keys('5')
                    print(f'Entered 5 for: {label_text}')
            elif input_element.tag_name == 'select':
                select = Select(input_element)  
                try:
                    select.select_by_visible_text('Yes')
                    print(f'Selected YES for: {label_text}')
                except:
                    print(f'No "Yes" option available for: {label_text}')
        except Exception as e:
            print(f'Error processing question: {label_text}. Error: {str(e)}')

    def review_and_submit_application(self):
        try:
            submit_button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()="Enviar solicitud"]/..'))
            )
            submit_button.click()
            print("Submit button clicked")
            time.sleep(random.uniform(3, 6))

            close_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Descartar"]'))
            )
            close_button.click()
            print("Close button clicked")
            time.sleep(random.uniform(3, 6))
        except NoSuchElementException:
            print("Close button not found")

if __name__ == "__main__":
    email = input("Por favor, ingresa tu correo electrónico: ")
    password = input("Por favor, ingresa tu contraseña: ")
    job_url = input("Por favor, ingresa la URL de búsqueda de empleos de LinkedIn: ")

    bot = LinkBot(email, password, job_url)
