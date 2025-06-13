# Proyecto Urban Routes

Proyecto realizado por: Yostin Chavarria Castro

Grupo: 29

Descripcion del proyecto:

    El proyecto abarca un test que se realizo a la aplicacion de Urban routes, el cual se automatizo para que se ingresaran direcciones para pedir un taxi, ademas se ingresaba la tarifa, numero de telefono, tarjeta de credito y algunos requisitos del pedido adicionales, adicionalmente se agrego la informacion del conductor a la hora de pedir el taxi y se aceptara el viaje.

    La prueba 1 configura la direccion.
    La prueba 2 selecciona la tarifa.
    La prueba 3 Rellena el numero de telefono.
    La prueba 4 Agrega la tarjeta de credito.
    La prueba 5 Escribe un mensaje al conductor.
    La prueba 6 Pide una manta y pañuelos.
    La prueba 7 Pide dos helados.
    La prueba 8 Verifica el modal de busqueda de conductor y cuando se acepta el viaje que es cuando termina el contador verifica la informacion del conductor.

Descripcion de las tecnologia

    Se utilizo la libreria selenium junto con el driver webdriver, el script automatizado se realizo en python y las pruebas se corrieron en pytest

Tecnicas utilizadas

    Se utilizo el modelo de objetos de pagina o page object model (POM) para organizar las pruebas, se creo la clase UrbanRoutesPage que contiene los objetos o localizadores de la pagina web y la clase TestUrbanRoutes la cual contiene todas las pruebas que se realizaron.

    Para localizar los objetos se utilizaron localizadores XPATH y CSS selector, ademas se utilizaron funciones como busqueda de localizadores por ID y CLASS_NAME que la libreria selenium posee. 

Requisitos 

    Python version 3.8 o superior
    Entorno virtual
    Pytest
    Libreria Selenium
    Driver WebDriver

Pasos para ejecutar las pruebas:

    Para ejecutar las pruebas se necesita correr el archivo main.py. Adicionalmente se necesita agregar un entorno virtual de python, instalar la libreria selenium e instalar el driver WebDriver.

    1. Clonar el repositorio utilizando el comando git clone https://github.com/tu_usuario/urban-grocers.git en la terminal
    2. Crear el entorno virtual utilizando el comando python -m venv venv en la terminal
    2. Instalar la libreria selenium utilizando el comando pip install selenium en la terminal.
    3. Instalar la libreria pytest utilizando el comando pip install pytest.
    4. Para ejecutar las pruebas se utiliza el comando pytest main.py en la terminal.
