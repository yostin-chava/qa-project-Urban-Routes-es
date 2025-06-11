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

######################################################################
# Clase de los elementos como parametros y su interaccion como metodos
######################################################################
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

    button_payment = (By.CLASS_NAME, "pp-button")
    button_add_card = (By.CSS_SELECTOR, ".pp-row.disabled")
    set_num_card = (By.ID, "number")
    set_cod_card = (By.XPATH, "//div[@class='card-code'][.//div[@class='card-code-label']]//input[contains(@id, 'code')]")
    out_card_click = (By.CLASS_NAME, "card-wrapper")
    button_add = (By.XPATH, "//button[contains(@class, 'button') and contains(text(), 'Agregar')]")
    button_close_card = (By.XPATH, "//div[contains(@class, 'section')][.//div[contains(@class, 'head') and contains(text(), 'Método de pago')]]//button[contains(@class, 'close-button')]")

    msg_driver = (By.ID, 'comment')

    check_blanket_scarves = (By.XPATH, "//div[@class='r-sw-container'][.//div[contains(text(), 'Manta y pañuelos')]]//span[contains(@class, 'slider') and contains(@class, 'round')]")
    see_verify_check_blanket_scarves = (By.XPATH, "//div[@class='r-sw-container'][.//div[contains(text(), 'Manta y pañuelos')]]//input[@type='checkbox' and contains(@class, 'switch-input')]")

    order_ice_cream = (By.XPATH, "//div[@class='r-counter-container'][.//div[contains(text(), 'Helado')]]//div[@class='counter-plus']")
    see_quantity_ice_cream = (By.XPATH, "//div[@class='r-counter-container'][.//div[contains(text(), 'Helado')]]//div[@class='counter-value']")


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

    ######################################################
    # Metodo para ingresar las direcciones hasta y desde #
    ######################################################
    def set_route(self, from_address, to_address):
        self.set_from(from_address) # Ingresamos la direccion desde pasandele el parametro de la direccion
        self.set_to(to_address) # Ingresamos la direccion hasta pasandele el parametro de la direccion
        assert self.get_from() == from_address # Confirmacion que se ingreso los datos correctamente
        assert self.get_to() == to_address # Confirmacion que se ingreso los datos correctamente
    ######################################################
    ######################################################

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

    ##############################################
    # Metodo para seleccionar la tarifa confort #
    #############################################
    def select_tariff_comfort(self):
        self.button_personal_click() #Hace click el personal
        self.button_taxi_click() #Hace click en taxi
        self.button_order_taxi_click() #Hace click en pedir un taxi
        self.button_comfort_click() #Hace click en la tarifa comfort
        # Verificamos que estemos entrando a la tarifa confort buscando el elemento que este
        # en requisitos del pedido "Manta y pañuelos" perteneciente unicamente a la tarifa confort
        assert "Manta y pañuelos" in self.get_el_comfort()
    #############################################
    #############################################

    # Metodo para hacer click en numero de telefono
    def button_phone_click(self):
        button_number = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.set_phone_number))
        button_number.click()

    # Metodo para escribir el numero de telefono
    def write_phone_number(self, phone_number):
        phone_num = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.write_phone_n))
        phone_num.send_keys(phone_number)

    # Metodo para hacer click en el boton siguiente
    def button_next_click(self):
        button_nex = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_next))
        button_nex.click()

    # Metodo para obtener el valor que ingresamos en el numero de telefono
    def get_phone_number(self):
        return self.driver.find_element(*self.write_phone_n).get_property('value')

    # Metodo para escribir el codigo de confirmacion
    def set_code_number(self, code):
        code_num = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.introduce_code))
        code_num.send_keys(code)

    # Metodo para obtener el valor que ingresamos en el codigo de confirmacion
    def get_code_number(self):
        return self.driver.find_element(*self.introduce_code).get_property('value')

    # Metodo para hacer click en el boton continuar
    def button_continue_click(self):
        btn_continue = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_continue))
        btn_continue.click()

    ##############################################
    # Metodo para agregar el numero de telefono #
    ##############################################
    def set_write_phone_number(self, phone_number,driver):
        self.button_phone_click() #Hace click en numero de telefono
        self.write_phone_number(phone_number) #Ingresa el numero de telefono
        assert self.get_phone_number() == phone_number #Verifica que se ingreso el numero de telefono correctamente
        self.button_next_click() #Hace click en el boton siguiente
        code = retrieve_phone_code(driver) #Interceptamos el codigo de confirmacion que devuelve el servidor
        self.set_code_number(code) #Ingresa el codigo de confirmacion
        assert self.get_code_number() == code #Verifica que se ingreso el codigo de confirmacion correctamente
        self.button_continue_click() #Hace click en el boton continuar
    ###############################################
    ###############################################

    # Metodo para hacer click en metodo de pago
    def button_payment_method_click(self):
        btn_payment = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_payment))
        btn_payment.click()

    # Metodo para hacer click en Agregar tarjeta
    def button_text_add_card_click(self):
        btn_add_card = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_add_card))
        btn_add_card.click()

    # Metodo para escribir el numero de la tarjeta
    def set_number_card(self, number_card):
        num_card = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.set_num_card))
        num_card.clear()
        num_card.send_keys(number_card)

    # Metodo para escribir el codigo de la tarjeta
    def set_code_card(self, code_card):
        cod_card = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.set_cod_card))
        cod_card.clear()
        cod_card.send_keys(code_card)

    # Metodo para obtener el valor que ingresamos en el numero de la tarjeta
    def get_number_card(self):
        return self.driver.find_element(*self.set_num_card).get_property('value')

    # Metodo para obtener el valor que ingresamos en el codigo de la atrjeta
    def get_code_card(self):
        return self.driver.find_element(*self.set_cod_card).get_property('value')

    # Metodo para hacer click en algun lugar de la pantalla
    def out_click(self):
        out = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.out_card_click))
        out.click()

    # Metodo para hacer click en Agregar
    def button_add_card_click(self):
        btn_add = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_add))
        btn_add.click()

    # Metodo para hacer click en la X para cerrar la ventana de metodos de pago
    def button_close_card_click(self):
        btn_x = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_close_card))
        btn_x.click()

    ##################################
    # Metodo para agregar la tarjeta #
    ##################################
    def select_and_add_card (self, card_number, card_code):
        self.button_payment_method_click() #Hace click en metodo de pago
        self.button_text_add_card_click() #Hace click en agregar tarjeta
        self.set_number_card(card_number) #Ingresa el numero de la tarjeta
        self.set_code_card(card_code) #Ingresa el codigo de la tarjeta
        assert self.get_number_card() == card_number #Verifica que se ingreso el numero de la tarjeta correctamente
        assert self.get_code_card() == card_code #Verifica que se ingreso el codigo de la tarjeta correctamente
        self.out_click() #Hace click en alguna parte de la pantalla
        self.button_add_card_click() #Hace click en el boton agregar
        self.button_close_card_click() #Hace click en la X
    ##################################
    ##################################

    # Metodo que agrega el mensaje al conductor
    def set_msg_driver(self, msg):
        driver_msg = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.msg_driver))
        driver_msg.send_keys(msg)

    # Metodo que obtiene el valor o texto que ingresamos
    def get_msg_driver(self):
        return self.driver.find_element(*self.msg_driver).get_property('value')

    ####################################################
    # Metodo para agregar el mensaje para el conductor #
    ####################################################
    def add_msg_driver(self, msg):
        self.set_msg_driver(msg) #Ingresa el msg para el conductor
        assert self.get_msg_driver() == msg # Verifica que el msj se agrego correctamente
    ####################################################
    ####################################################

    # Metodo para hacer click en la casilla de verificacion
    def check_blanket_scarves_click(self):
        check_click = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.check_blanket_scarves))
        #self.driver.execute_script("arguments[0].click();", check_click)
        check_click.click()

    # Metodo para verificar que la casilla se ha seleccionado
    def select_check_box(self):
        checkbox = self.driver.find_element(*self.see_verify_check_blanket_scarves)
        assert checkbox.is_selected()

    #########################################################################
    # Metodo para seleccionar casilla de verificacion para Manta y pañuelos #
    #########################################################################
    def check_box_blanket_scarves(self):
        self.check_blanket_scarves_click() #Hace lc}}click en la casilla de verificacion
        self.select_check_box() #Verifica que la casilla este seleccionada
    #########################################################################
    #########################################################################

    # Metodo para hacer click en + para agregar un helado
    def order_an_ice_creams_plus_click(self):
        ice_cream_order = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.order_ice_cream))
        ice_cream_order.click()

    # Metodo que obtiene la cantidad de helados pedidos
    def get_quantity_ice_cream(self):
        return self.driver.find_element(*self.see_quantity_ice_cream).text

    #################################
    # Metodo para pedir dos helados #
    #################################
    def order_two_ice_creams(self):
        self.order_an_ice_creams_plus_click() #Hace click en el boton + para agregar un helado
        self.order_an_ice_creams_plus_click() #Hace click en el boton + para agregar un segundo helado
        assert self.get_quantity_ice_cream() == "2" #Verifica que la cantidad de helados sea dos

    #################################
    #################################



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

    def test_add_phone_number(self):
        self.urban.set_route(data.address_from, data.address_to)
        self.urban.select_tariff_comfort()
        self.urban.set_write_phone_number(data.phone_number, self.driver)

    def test_add_card(self):
        self.urban.set_route(data.address_from, data.address_to)
        self.urban.select_tariff_comfort()
        #self.urban.set_write_phone_number(data.phone_number, self.driver)
        self.urban.select_and_add_card(data.card_number, data.card_code)

    def test_write_msg_driver(self):
        self.urban.set_route(data.address_from, data.address_to)
        self.urban.select_tariff_comfort()
        #self.urban.set_write_phone_number(data.phone_number, self.driver)
        #self.urban.select_and_add_card(data.card_number, data.card_code)
        self.urban.add_msg_driver(data.message_for_driver)

    def test_check_box_blanket_scarves(self):
        self.urban.set_route(data.address_from, data.address_to)
        self.urban.select_tariff_comfort()
        #self.urban.set_write_phone_number(data.phone_number, self.driver)
        #self.urban.select_and_add_card(data.card_number, data.card_code)
        #self.urban.add_msg_driver(data.message_for_driver)
        self.urban.check_box_blanket_scarves()

    def test_order_two_ice_cream(self):
        self.urban.set_route(data.address_from, data.address_to)
        self.urban.select_tariff_comfort()
        #self.urban.set_write_phone_number(data.phone_number, self.driver)
        #self.urban.select_and_add_card(data.card_number, data.card_code)
        #self.urban.add_msg_driver(data.message_for_driver)
        #self.urban.check_box_blanket_scarves()
        self.urban.order_two_ice_creams()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
