import time

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.remote.webdriver import WebDriver

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
    verify_class_filled = (By.XPATH, "//div[contains(@class, 'np-button') and contains(@class, 'filled')]")
    verify_add_phone = (By.XPATH, "//div[contains(@class, 'np-button') and contains(@class, 'filled')]//div[@class = 'np-text']")

    button_payment = (By.CLASS_NAME, "pp-button")
    button_add_card = (By.CSS_SELECTOR, ".pp-row.disabled")
    set_num_card = (By.ID, "number")
    set_cod_card = (By.XPATH, "//div[@class='card-code'][.//div[@class='card-code-label']]//input[contains(@id, 'code')]")
    out_card_click = (By.CLASS_NAME, "card-wrapper")
    button_add = (By.XPATH, "//button[contains(@class, 'button') and contains(text(), 'Agregar')]")
    button_close_card = (By.XPATH, "//div[contains(@class, 'section')][.//div[contains(@class, 'head') and contains(text(), 'Método de pago')]]//button[contains(@class, 'close-button')]")

    msg_driver = (By.ID, 'comment')
    verify_class_error = (By.XPATH, "// div[contains(@class, 'input-container') and contains(@class, 'error')][.//input[contains(@id, 'comment')]]")
    get_msg_error = (By.XPATH, "//div[@style]//div[@class = 'error' and contains(text(), 'Longitud máxima 24')]")

    check_blanket_scarves = (By.XPATH, "//div[@class='r-sw-container'][.//div[contains(text(), 'Manta y pañuelos')]]//span[contains(@class, 'slider') and contains(@class, 'round')]")
    see_verify_check_blanket_scarves = (By.XPATH, "//div[@class='r-sw-container'][.//div[contains(text(), 'Manta y pañuelos')]]//input[@type='checkbox' and contains(@class, 'switch-input')]")

    order_ice_cream = (By.XPATH, "//div[@class='r-counter-container'][.//div[contains(text(), 'Helado')]]//div[@class='counter-plus']")
    see_quantity_ice_cream = (By.XPATH, "//div[@class='r-counter-container'][.//div[contains(text(), 'Helado')]]//div[@class='counter-value']")

    button_blue_order_taxi = (By.CSS_SELECTOR, "button.smart-button")
    modal_popup = (By.CLASS_NAME, "order-header-title")

    modal_popup_driver = (By.XPATH, "//div[@class='order-header-title' and contains(text(), 'El conductor llegará en')]")
    number_order = (By.CLASS_NAME, "order-number")
    rating_driver = (By.CSS_SELECTOR, "div.order-btn-group div.order-button div.order-btn-rating")
    photo_driver = (By.CSS_SELECTOR, "div.order-btn-group div.order-button img")
    name_driver = (By.CSS_SELECTOR, "div.order-btn-group div:nth-child(2)")

    def __init__(self, driver):
        self.driver = driver

    ####################################################################################################################
    ####################################################################################################################
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

    #############################################
    # Metodo para seleccionar la tarifa confort #
    #############################################
    def select_tariff_comfort(self):
        self.button_personal_click() #Hace click el personal
        self.button_taxi_click() #Hace click en taxi
        self.button_order_taxi_click() #Hace click en pedir un taxi
        self.button_comfort_click() #Hace click en la tarifa comfort
    #############################################
    #############################################

    ####################################################################################################################
    ####################################################################################################################
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

    # Metodo que busca el contenedor que tiene el numero de telefono, el cual se agrega cuando aparece la clase filled
    def check_class_filled(self):
        class_filled = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.verify_class_filled))
        return class_filled.get_attribute("class")

    # Metodo para obtener el color del contenedor el cual es verde
    def get_border_color_add_phone_number(self):
        color_green = self.driver.find_element(*self.verify_class_filled)
        return color_green.value_of_css_property("border-color")

    # Metodo que obtiene el numero de teleno en el formulario de la tarifa
    def get_add_phone_number(self):
        phone_txt = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.verify_add_phone))
        return phone_txt.text

    ##############################################
    # Metodo para agregar el numero de telefono #
    ##############################################
    def set_write_phone_number(self, phone_number):
        self.button_phone_click() #Hace click en numero de telefono
        self.write_phone_number(phone_number) #Ingresa el numero de telefono

    ####################################################################################################################
    ####################################################################################################################
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

    # Metodo que obtiene true o false dependiendo de si el boton esta activo
    def enabled_button_add(self):
        enabled_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_add))
        return enabled_btn.is_enabled()

    # Metodo para hacer click en Agregar
    def button_add_card_click(self):
        btn_add = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_add))
        btn_add.click()

    # Metodo para hacer click en la X para cerrar la ventana de metodos de pago
    def button_close_card_click(self):
        btn_x = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_close_card))
        btn_x.click()

    ########################################################
    # Metodo de pasos para agregar los datos de la tarjeta #
    ########################################################
    def set_data_card (self, card_number, card_code):
        self.button_payment_method_click() #Hace click en metodo de pago
        self.button_text_add_card_click() #Hace click en agregar tarjeta
        self.set_number_card(card_number) #Ingresa el numero de la tarjeta
        self.set_code_card(card_code) #Ingresa el codigo de la tarjeta

    ####################################################################################################################
    ####################################################################################################################
    # Metodo que agrega el mensaje al conductor
    def set_msg_driver(self, msg):
        driver_msg = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.msg_driver))
        driver_msg.send_keys(msg)

    # Metodo que obtiene el valor o texto que ingresamos
    def get_msg_driver(self):
        return self.driver.find_element(*self.msg_driver).get_property('value')

    # Metodo que busca el contenedor que tiene el msj del conductor, el cual al agregar mas de 24 caracteres agrega la clase error
    def check_class_error(self):
        class_error = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.verify_class_error))
        return class_error.get_attribute("class")

    # Metodo para obtener el color del contenedor
    def get_border_color_class_error(self):
        color_red = self.driver.find_element(*self.verify_class_error)
        return color_red.value_of_css_property("border-color")

    # Metodo que obtiene el texto del mensaje de error
    def get_error_msg(self):
        error_msg = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.get_msg_error))
        return error_msg.text

    ####################################################################################################################
    ####################################################################################################################
    # Metodo para hacer click en la casilla de verificacion
    def check_blanket_scarves_click(self):
        check_click = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.check_blanket_scarves))
        check_click.click()

    # Metodo para verificar que la casilla se ha seleccionado
    def select_check_box(self):
        checkbox = self.driver.find_element(*self.see_verify_check_blanket_scarves)
        return checkbox.is_selected()

    ####################################################################################################################
    ####################################################################################################################
    # Metodo para hacer click en + para agregar un helado
    def order_an_ice_creams_plus_click(self):
        ice_cream_order = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.order_ice_cream))
        ice_cream_order.click()

    # Metodo que obtiene la cantidad de helados pedidos
    def get_quantity_ice_cream(self):
        return self.driver.find_element(*self.see_quantity_ice_cream).text

    ##########################################
    # Metodo de pasos para pedir dos helados #
    ##########################################
    def order_two_ice_creams(self):
        self.order_an_ice_creams_plus_click() #Hace click en el boton + para agregar un helado
        self.order_an_ice_creams_plus_click() #Hace click en el boton + para agregar un segundo helado

    ####################################################################################################################
    ####################################################################################################################
    # Metodo para hacer click en el boton azul de pedir el taxi
    def button_blue_order_taxi_click(self):
        btn_blue = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.button_blue_order_taxi))
        btn_blue.click()

    # Metodo que obtiene el texto de la ventana modal
    def get_modal_popup_looking_taxi(self):
        modal = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.modal_popup))
        return modal.text

    ####################################################################################################################
    ####################################################################################################################
    # Metodo que obtiene el texto El conductor llegará en
    def get_text_modal_popup_driver(self):
        popup_driver = WebDriverWait(self.driver, 40).until(EC.visibility_of_element_located(self.modal_popup_driver))
        return popup_driver.text

    # Metodo que obtiene el numero de la orden
    def get_text_number_order(self):
        num_order = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.number_order))
        return num_order.text

    # Metodo que obtiene el rating del conductor
    def get_text_rating_driver(self):
        rating = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.rating_driver))
        return rating.text

    # Metodo que obtiene el formato de la foto
    def get_format_photo_driver(self):
        img = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.photo_driver))
        return img.get_attribute("src")

    # Metodo que obtiene el nombre del conductor
    def get_text_name_driver(self):
        driver_name = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.name_driver))
        return driver_name.text

########################
########################
# Clase para los tests #
########################
########################
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
        self.urban = UrbanRoutesPage(self.driver)

    # Test punto 1
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        self.urban.set_route(data.address_from, data.address_to) # Se prueba las direcciones desde y hasta
        assert self.urban.get_from() == data.address_from  # Confirmacion que se ingreso los datos correctamente
        assert self.urban.get_to() == data.address_to  # Confirmacion que se ingreso los datos correctamente

    # Test punto 2
    def test_set_tariff_comfort(self):
        self.urban.select_tariff_comfort() # Se prueba seleccionar la tarifa confort
        # Verificamos que estemos entrando a la tarifa confort buscando el elemento que este
        # en requisitos del pedido "Manta y pañuelos" perteneciente unicamente a la tarifa confort
        assert "Manta y pañuelos" in self.urban.get_el_comfort()

    # Test punto 3
    def test_add_phone_number(self):
        self.urban.set_write_phone_number(data.phone_number) # Se prueba que se ingrese el numero de telefono
        assert self.urban.get_phone_number() == data.phone_number  # Verifica que se ingreso el numero de telefono correctamente
        self.urban.button_next_click()  # Hace click en el boton siguiente
        code = retrieve_phone_code(self.driver)  # Interceptamos el codigo de confirmacion que devuelve el servidor
        self.urban.set_code_number(code)  # Ingresa el codigo de confirmacion
        assert self.urban.get_code_number() == code  # Verifica que se ingreso el codigo de confirmacion correctamente
        self.urban.button_continue_click()  # Hace click en el boton continuar
        assert "filled" in self.urban.check_class_filled()  # Verifica que efectivamente la clase filled esta en el elemento
        assert self.urban.get_border_color_add_phone_number() in ["rgb(86, 184, 159)","rgba(86, 184, 159, 1)"]  # Verifica el color del borde "verde"
        assert data.phone_number in self.urban.get_add_phone_number()  # Verifica que el numero de telefono agregado aparezca bien escrito en el formulario

    # Test punto 4
    def test_add_card(self):
        self.urban.set_data_card(data.card_number, data.card_code) # Se prueba que se ingrese la tarjeta de credito
        assert self.urban.get_number_card() == data.card_number  # Verifica que se ingreso el numero de la tarjeta correctamente
        assert self.urban.get_code_card() == data.card_code  # Verifica que se ingreso el codigo de la tarjeta correctamente
        self.urban.out_click()  # Hace click en alguna parte de la pantalla
        assert self.urban.enabled_button_add() == True  # Verifica que el boton esta activado, si es true esta activado
        self.urban.button_add_card_click()  # Hace click en el boton agregar
        self.urban.button_close_card_click()  # Hace click en la X

    # Test punto 5
    def test_write_msg_driver(self):
        self.urban.set_msg_driver(data.message_for_driver)  # Ingresa el msg para el conductor
        assert self.urban.get_msg_driver() == data.message_for_driver  # Verifica que el msj se agrego correctamente
        assert "error" in self.urban.check_class_error()  # Verificaque efectivamente la clase error esta en el elemento
        assert self.urban.get_border_color_class_error() in ["rgb(252, 82, 48)", "rgba(252, 82, 48, 1)"]  # Verifica el color del borde
        assert "Longitud máxima 24" in self.urban.get_error_msg()  # Verifica que el msj de error sea el correcto

    # Test punto 6
    def test_check_box_blanket_scarves(self):
        self.urban.check_blanket_scarves_click()  # Hace click en la casilla de verificacion
        assert self.urban.select_check_box() == True  # Verifica que la casilla este seleccionada, si es true esta seleccionada

    # Test punto 7
    def test_order_two_ice_cream(self):
        self.urban.order_two_ice_creams() # Se prueba que se agreguen dos helados
        assert self.urban.get_quantity_ice_cream() == "2"  # Verifica que la cantidad de helados sea dos

    # Test punto 8
    def test_check_modal_wait_to_driver(self):
        self.urban.button_blue_order_taxi_click()
        assert self.urban.get_modal_popup_looking_taxi() == "Buscar automóvil"

    # Test punto 9
    def test_check_modal_info_driver(self):
        assert "El conductor llegará en" in self.urban.get_text_modal_popup_driver()  # Verifica el texto del conductor llegara en...
        assert self.urban.get_text_number_order() != ""  # Verifica que haya un numero de orden
        assert self.urban.get_text_rating_driver() != ""  # Verifica que haya un rating del conductor
        assert any(ext in self.urban.get_format_photo_driver() for ext in[".png", ".jpg", ".jpeg", ".svg"])  # Verifica que haya una imagen con algun formato
        assert self.urban.get_text_name_driver() != ""  # Verifica que haya un nombre de conductor

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

