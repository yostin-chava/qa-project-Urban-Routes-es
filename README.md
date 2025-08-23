# Proyecto Urban Routes - Automatización

**Autor**: Yostin Chavarría Castro

## 📝 Descripción del proyecto

Este proyecto consiste en la automatización de pruebas para la aplicación web **Urban Routes**, específicamente para el proceso de solicitud de un taxi.

El test automatizado cubre el ingreso de direcciones, selección de tarifa, número de teléfono, datos de tarjeta de crédito y otros requisitos adicionales del pedido. También se automatiza la visualización de la información del conductor una vez aceptado el viaje.

### 🧪 Pruebas incluidas

1. Configura la dirección de origen y destino.
2. Selecciona la tarifa del viaje.
3. Rellena el número de teléfono del usuario.
4. Ingresa los datos de la tarjeta de crédito.
5. Escribe un mensaje para el conductor.
6. Solicita una manta y pañuelos.
7. Pide dos helados.
8. Verifica el modal de búsqueda de conductor y, al aceptar el viaje, comprueba la información del conductor mostrada al finalizar el contador.

---

## ⚙️ Tecnologías utilizadas

- **Lenguaje**: Python 3.8 o superior
- **Framework de pruebas**: Pytest
- **Librería de automatización**: Selenium
- **WebDriver**: ChromeDriver 

---

## 🧰 Técnicas aplicadas

- Se aplicó el patrón **Page Object Model (POM)** para estructurar el código.
- La clase `UrbanRoutesPage` contiene los localizadores y elementos de la página.
- La clase `TestUrbanRoutes` agrupa las pruebas automatizadas.

### 🔍 Localizadores utilizados

- XPATH
- CSS Selector
- ID
- CLASS_NAME

---

## 📦 Requisitos del entorno

- Python 3.8 o superior
- Entorno virtual de Python (opcional, pero recomendado)
- Pytest
- Selenium
- WebDriver correspondiente (ej. ChromeDriver)

---

## ▶️ Pasos para ejecutar las pruebas

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/urban-grocers.git

2. Crear un entorno virtual (opcional, pero recomendado):

   ```bash
   python -m venv venv

3. Activar el entorno virtual:
   
   ```bash
   # En Windows:
   venv\Scripts\activate

   # En macOS/Linux:
   source venv/bin/activate

5. Instalar las dependencias necesarias:

   ```bash
   pip install selenium pytest

6. Ejecutar las pruebas:

   ```bash
   pytest main.py
