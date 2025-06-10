from selenium.webdriver.common import by

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    '''
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code
    '''
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                                {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
                if code:
                    return code
        except WebDriverException:
            time.sleep(1)
            continue
        time.sleep(1)  # esperar antes de siguiente intento
    raise Exception("No se encontró el código de confirmación del teléfono.")

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    set_personal = (By.CSS_SELECTOR, '.mode:nth-child(3)')
    set_taxi_mode = (By.CSS_SELECTOR, '.type:nth-child(3)')
    set_order_taxi = (By.CSS_SELECTOR, '.button.round')
    set_comfort = (By.XPATH, '//div[contains(@class, "tcard")][.//div[contains(@class, "tcard-title") and contains(text(), "Comfort")]]')
    get_element_comfort = (By.XPATH, '//div[contains(@class,"r-sw-label") and contains(text(), "Manta y pañuelos")]')
    set_phone_number = (By.CLASS_NAME, 'np-button')
    write_phone_n = (By.ID, "phone")
    button_next = (By.XPATH, "//button[contains(@class, 'button') and contains(text(), 'Siguiente')]")
    introduce_code = (By.ID, "code")
    button_continue = (By.XPATH, "//button[contains(@class, 'button') and contains(text(), 'Confirmar')]")

    def __init__(self, driver):
        self.driver = driver

    # Metodo para rellenar el campo desde
    def set_from(self, from_address):
        from_a = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.from_field))
        from_a.send_keys(from_address)

    # Metodo para rellenar el campo hasta
    def set_to(self, to_address):
        to_a = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.to_field))
        to_a.send_keys(to_address)

    # Metodo para Obtener el valor que tiene ingresado el elemento desde
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    # Metodo para Obtener el valor que tiene ingresado el elemento hasta
    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    #######################################
    # Rellenamos los campos Desde y Hasta #
    #######################################
    def set_route(self, from_address, to_address):

        self.set_from(from_address)
        self.set_to(to_address)

        assert self.get_from() == from_address
        assert self.get_to() == to_address

    # Metodo para dar clic en personal
    def button_personal_click(self):
        personal_clic = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.set_personal))
        personal_clic.click()

    # Metodo para dar clic en Taxi
    def button_taxi_click(self):
        taxi_select = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.set_taxi_mode))
        taxi_select.click()

    # Metodo para dar clic en pedir un taxi
    def button_order_taxi_click(self):
        order_taxi_clic = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.set_order_taxi))
        order_taxi_clic.click()

    # Metodo para dar clic en la tafica confort
    def button_comfort_click(self):
        comfort_clic = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.set_comfort))
        comfort_clic.click()

    # Metodo para Obtener un elemento de la tarifa confort
    def get_el_comfort(self):
        return WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.get_element_comfort)).text

    ################################################################################
    # Clickamos en el siguiente orden, personal, taxi, ordenar taxi y tarifa confort
    ################################################################################
    def select_tariff_comfort(self):
        self.button_personal_click()
        self.button_taxi_click()
        self.button_order_taxi_click()
        self.button_comfort_click()
        # Verificamos que estemos entrando a la tarifa confort buscando el elemento que este
        # en requisitos del pedido "Manta y pañuelos" perteneciente unicamente a la tarifa confort
        assert "Manta y pañuelos" in self.get_el_comfort()

    def button_phone_click(self):
        button_number = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.set_phone_number))
        button_number.click()

    def write_phone_number(self, phone_number):
        phone_num = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.write_phone_n))
        phone_num.send_keys(phone_number)

    def button_next_click(self):
        button_nex = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_next))
        button_nex.click()

    # Metodo para Obtener el valor que tiene ingresado el elemento hasta
    def get_phone_number(self):
        return self.driver.find_element(*self.write_phone_n).get_property('value')

    def set_code_number(self, code):
        code_num = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.introduce_code))
        code_num.send_keys(code)

    def get_code_number(self):
        return self.driver.find_element(*self.introduce_code).get_property('value')

    def button_continue_click(self):
        button_continu = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_continue))
        button_continu.click()


    ###############################################
    #
    ###############################################
    def set_write_phone_number(self, phone_number,driver):
        self.button_phone_click()
        self.write_phone_number(phone_number)
        assert self.get_phone_number() == phone_number
        self.button_next_click()
        code = retrieve_phone_code(driver)
        self.set_code_number(code)
        assert self.get_code_number() == code
        self.button_continue_click()

########################################################################################################################
class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver.chrome.options import Options #from selenium.webdriver import DesiredCapabilities
        options = Options() #capabilities = DesiredCapabilities.CHROME
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"}) #capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(options=options) #cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.urban = UrbanRoutesPage(self.driver)

    def test_set_route(self):
        self.urban.set_route(data.address_from, data.address_to)

    def test_set_tariff_comfort(self):
        self.urban.set_route(data.address_from, data.address_to)
        self.urban.select_tariff_comfort()

    def test_numero(self):
        self.urban.set_route(data.address_from, data.address_to)
        self.urban.select_tariff_comfort()
        self.urban.set_write_phone_number(data.phone_number, self.driver)


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
