from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
import time
import csv

class Crawler:
    
    def _setupDriver(self):
        print("Configurando el driver de Chrome...")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 20)
        print("Driver de Chrome configurado exitosamente.")

    def __init__(self):
        self._setupDriver()
        self.url = "https://www3.labanca.com.uy/resultados/quiniela"

    def navigateTo(self):
        print(f"Navegando a la URL: {self.url}")
        self.driver.get(self.url)
        print("Página cargada.")

    def _get_select_element(self):
        print("Buscando el elemento select...")
        select = Select(self.wait.until(EC.presence_of_element_located((By.ID, 'fecha_sorteo'))))
        print("Elemento select encontrado.")
        return select

    def _click_mostrar_button(self):
        for attempt in range(1, 4):  # Intentar hasta 3 veces
            try:
                print(f"Intento {attempt} de hacer clic en el botón 'Mostrar'...")
                self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'img[alt="Ajax-loader"]')))
                mostrar_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'botonMostrar')))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", mostrar_button)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", mostrar_button)
                print("Clic en 'Mostrar' exitoso.")
                return True
            except (ElementClickInterceptedException, TimeoutException, StaleElementReferenceException) as e:
                print(f"Error al hacer clic en el botón 'Mostrar': {e}")
                time.sleep(2)
        print("No se pudo hacer clic en 'Mostrar' después de 3 intentos.")
        return False

    def _get_numbers(self):
        print("Esperando a que los resultados se carguen...")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.results-column')))
        time.sleep(3)
        results_columns = self.driver.find_elements(By.CSS_SELECTOR, 'ul.results-column')
        numbers = []
        for column in results_columns:
            lis = column.find_elements(By.TAG_NAME, 'li')
            for li in lis:
                number = li.text.strip()
                numbers.append(number)
                print(f"Número agregado: {number}")
        return numbers

    def getQuinielaData(self):
        all_numbers = []
        
        for attempt in range(1, 4):  # Intentar hasta 3 veces
            try:
                print(f"Intento {attempt} de obtener datos de Quiniela...")
                select_element = self._get_select_element()
                for option in select_element.options:
                    try:
                        print(f"Procesando opción: {option.text}")
                        select_element.select_by_visible_text(option.text)
                        if not self._click_mostrar_button():
                            print(f"No se pudo hacer clic en 'Mostrar' para la opción {option.text}")
                            continue
                        numbers = self._get_numbers()
                        all_numbers.append({option.text: numbers})
                        print(f"Datos obtenidos para {option.text}")
                    except Exception as e:
                        print(f"Error al procesar opción {option.text}: {str(e)}")
                print("Todos los datos de Quiniela obtenidos exitosamente.")
                break  # Si llegamos aquí sin excepciones, salimos del bucle
            except StaleElementReferenceException:
                print("El elemento se volvió obsoleto. Reintentando...")
                self.driver.refresh()
                time.sleep(2)
        
        self._save_to_csv(all_numbers)

    def _save_to_csv(self, all_numbers):
        print("Guardando resultados en CSV...")
        with open('quiniela_results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Fecha', 'Numero']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in all_numbers:
                for date, numbers in result.items():
                    for number in numbers:
                        writer.writerow({'Fecha': date, 'Numero': number})
        print("Resultados guardados en 'quiniela_results.csv'")

    def __del__(self):
        if hasattr(self, 'driver'):
            print("Cerrando el driver de Chrome...")
            self.driver.quit()
            print("Driver cerrado.")