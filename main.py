import data
from selenium import webdriver
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage
#from selenium.webdriver.remote.webdriver import WebDriver

########################
# Clase para los tests #
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

