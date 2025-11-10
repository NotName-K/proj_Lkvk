# proj_LVK
## Logo del grupo
![Logo](https://github.com/NotName-K/POO-R2/blob/main/Screenshot%202025-09-23%20110719.png?raw=true)

## Comparador y Análisis de Motocicletas en Python.
![Logo](https://github.com/NotName-K/proj_Lkvk/blob/main/Logo.jpg)

Look_Vike es una proyecto especializado en análisis y evaluación comparativa de motocicletas, diseñada para ayudar a compradores a tomar decisiones informadas basadas en datos técnicos y criterios objetivos.

Este programa implementa las bases de la POO, tratando que cada sección integre clases, metodos y objetos, junto con las herramientas que hacen parte de esta forma de programación.

Este repositorio muestra una versión preliminar del proyecto.
#### Integrantes
  - Lucas García
  - Kevin Castellanos
  - Vladimir Camargo
## Objetivos
### General
- Simplificar el proceso de selección de motocicletas mediante herramientas de comparación y análisis que permitan al usuario identificar la mejor opción según sus necesidades específicas, presupuesto y preferencias de manejo.
### Especificos
- Implementar una arquitectura POO sólida con clases especializadas para diferentes tipos de motocicletas
- Desarrollar algoritmos de evaluación que calculen scores basados en múltiples criterios técnicos.
- Construir una base de datos estructurada de motocicletas con especificaciones técnicas completas
- Simplificar información técnica compleja para hacerla accesible a usuarios no expertos.
- Proporcionar recomendaciones personalizadas basadas en necesidades específicas del usuario.
- Implementar Webscrapping, contando asi información actualizada de cada motocicleta y Fabricante.

## Motivo
Este proyecto surge para solucionar un problema que algunos vivimos: buscar moto y mas sin tener experienca puede ser un caos. En un país con un mercado tan grande de dos ruedas, actualmente uno se puede perder en mil páginas o confiar en opiniones de redes sociales, por tanto, se necesita una herramienta que haga mas práctica esta tarea.
Con las herramientas aprendidas en el curso POO, identificamos que es posible crear algo cercano a dicha herramienta, ya que se pueden adaptar muchos conceptos del motociclismo a las bases del POO: Clases y Objetos.

## Funcionamiento
### Clase Principal: Moto
Representa cada motocicleta con sus características técnicas y capacidades de evaluación, con herencias de los tipos de motos que hay en el mercado con sus caracteristicas especiales, además de estar complementada por clases que manejan la búsqueda, comparación, y lógica de Score, todo esto se guarda en la base de datos.
```mermaid
classDiagram
    %% ===== CLASE PRINCIPAL =====
    class Moto {
        - marca : string
        - modelo : string
        - cilindraje : int
        - suspension : string
        - peso : float
        - precio : float
        - vel_crucero : float
        - lanzamiento : date
        - seguridad : List~string~
        - accesorios : List~string~
        - transmision : string
        - iluminacion : string
        - relacionPP : float
        - topSpeed : float
        - caracteristicaDestacada : string
        - fallosComunes : List~string~
        + calcularScore() float
        + mostrarFicha() void
    }

   
    class MotoNaked {
        
    }

    class MotoDeportiva {
        
    }

    class MotoTouring {
        
    }

    class MotoScooter {
        
    }

    
    class Buscador {
       
    }

    class Comparador {
        
    }

    class KroonoScore {
       
    }

    class DB {
        
    }

 
    Moto <|-- MotoNaked
    Moto <|-- MotoDeportiva
    Moto <|-- MotoTouring
    Moto <|-- MotoScooter

     DB --> Moto : gestiona
    Buscador --> DB : usa
    Comparador --> DB : usa
    KroonoScore --> Moto : evalúa
```
### Base de Datos
Gestiona toda la persistencia de datos del sistema mediante archivos CSV. Actúa como el intermediario entre la aplicación y el almacenamiento permanente.
```mermaid
classDiagram
    class DB {
        - archivo_motos: string
        - archivo_marcas: string
        + cargar_motos() List~Moto~
        + guardar_moto(moto: Moto) void
        + buscar_por_marca(marca: string) List~Moto~
        + actualizar_precio(modelo: string, nuevo_precio: float) void
    }
    
    class Moto {
        
    }
    
    class Buscador {
       
    }
    
    class Comparador {
        
    }
    
    %% RELACIONES
    DB --> Moto : gestiona
    Buscador --> DB : consulta
    Comparador --> DB : consulta
```
### Análisis de Motos
Realiza búsquedas inteligentes sobre el catálogo de motocicletas, a partir de los filtros que seleccione el usuario.
```mermaid
classDiagram
    class Buscador {
        - criteriosAvanzados : Map~string, any~
        - resultados : List~Moto~
        - ordenActual : string
        + buscarModelo(nombre : string) List~Moto~
        + filtrarPorTipo(tipo : string) List~Moto~
        + filtrarPorPrecio(min : float, max : float) List~Moto~
        + ordenarPor(criterio : string) void
        + mostrarResultados() void
        + limpiarBusqueda() void
    }

    class DB {
        %% Gestor de base de datos
    }

    class Moto {
        %% Entidad principal
    }

    Buscador --> DB : consulta
    Buscador --> Moto : procesa
```
### KroonoScore
Calcula puntuaciones objetivas y estandarizadas para cada motocicleta, basadas en los componentes y el precio, dimensionando 5 apartados y dando una nota final de 1 al 10.
```mermaid
classDiagram
    class KroonoScore {
        - rendimiento : float
        - consumoYAutonomia : float
        - viajesYComodidad : float
        - disenoYMateriales : float
        - confiabilidad : float
        + calcularScore() float
    }

    class Moto {
        %% Entidad principal
    }

    class Comparador {
        %% Sistema de comparación
    }

    KroonoScore --> Moto : evalúa
    Comparador --> KroonoScore : utiliza
```
### Calculo de la calificación

## Comparativa
Permite contrastar múltiples motocicletas simultáneamente, mostrando diferencias técnicas y generando visualizaciones para facilitar la decisión final del usuario.
```mermaid
classDiagram
    class Comparador {
        - listaMotos : List~Moto~
        - motosSeleccionadas : List~Moto~
        - resultadoComparacion : Map~string, Moto~
        + agregarMoto(moto : Moto) void
        + mostrarComparacion() void
        + graficaComparacion(formato : ) void
        + limpiarComparador() void
    }

    class Moto {
        %% Entidad principal
    }

    class KroonoScore {
        %% Sistema de scoring
    }

    Comparador --> Moto : compara
    Comparador --> KroonoScore : integra
```
## General
Aqui se muestra el funcionamiento de las clases antes descritas:
```mermaid
classDiagram
    %% ===== Clases principales =====
    class Marca {
        - nombre : string
        - pais : string
        - motos : List~Moto~
        + agregarMoto(moto : Moto) void
        + mostrarModelos() void
    }

    class Moto {
        - marca : string
        - modelo : string
        - cilindraje : int
        - suspension : string
        - peso : float
        - precio : float
        - vel_crucero : float
        - lanzamiento : date
        - seguridad : List~string~
        - accesorios : List~string~
        - transmision : string
        - iluminacion : string
        - relacionPP : float
        - topSpeed : float
        - caracteristicaDestacada : string
        - fallosComunes : List~string~
        + calcularScore() float
        + mostrarFicha() void
    }

    class KroonoScore {
        - rendimiento : float
        - consumoYAutonomia : float
        - viajesYComodidad : float
        - disenoYMateriales : float
        - confiabilidad : float
        + calcularScore() float
    }

    class Concesionario {
        - nombre : string
        - nivelPostventa : int
        - añosGarantia : int
    }

    class Comparador {
    - listaMotos : List~Moto~
    - motosSeleccionadas : List~Moto~
    - resultadoComparacion : Map~string, Moto~
    + agregarMoto(moto : Moto) void
    + mostrarComparacion() void
    + graficaComparacion(formato : ) void
    + limpiarComparador() void
}


    class Buscador {
    - criteriosAvanzados : Map~string, any~
    - resultados : List~Moto~
    - ordenActual : string
    + buscarModelo(nombre : string) List~Moto~
    + filtrarPorTipo(tipo : string) List~Moto~
    + filtrarPorPrecio(min : float, max : float) List~Moto~
    + ordenarPor(criterio : string) void
    + mostrarResultados() void
    + limpiarBusqueda() void
}


    class EvaluadorSegundaMano {
        - moto : Moto
        - kmActual : int
        - precio: float
        - precio_prom : float
        - añoCompra : int
        - condiciones : Map~string, int~
        - promedioCondicion : float
        - scoreFinal : float
        - recomendacion : string
        + solicitarDatosUsuario() void
        + verificarKilometraje() bool
        + calcularCondicionPromedio() float
        + calcularScoreFinal() float
        + generarRecomendacion() string
        + mostrarInforme() void
    }

 class DB {
        - archivo_motos: string
        - archivo_marcas: string
        + cargar_motos() List~Moto~
        + guardar_moto(moto: Moto) void
        + buscar_por_marca(marca: string) List~Moto~
        + actualizar_precio(modelo: string, nuevo_precio: float) void
}
DB  --> "many" Moto : gestiona
    Buscador --> DB : usa
    Comparador --> DB : usa
    Marca "1" --> "many" Moto : contiene
    
    

    class MotoNaked {
        + estiloDeConduccion() string
    }

    class MotoDeportiva {
        + modoDeConduccion() string
    }

    class MotoMultiproposito {
        + tipoDeTerreno() string
    }

    class MotoTouring {
        + capacidadDeCarga() float
    }

    class MotoScooter {
        + tipoDeTransmision() string
    }

    %% ===== Relaciones =====
    Marca "1" --> "many" Moto : contiene >
    Moto "1" --> "1" KroonoScore : calcula >
    Comparador "1" --> "many" Moto : compara >
    Buscador "1" --> "many" Moto : filtra >
    Concesionario "1" --> "many" Moto : vende >
    EvaluadorSegundaMano --> Moto : evalúa >
    Comparador --> EvaluadorSegundaMano : usa >


    %% ===== Herencias =====
    Moto <|-- MotoNaked
    Moto <|-- MotoDeportiva
    Moto <|-- MotoMultiproposito
    Moto <|-- MotoTouring
    Moto <|-- MotoScooter

```
## Estructura del code
```
look_vike/
│
├── __init__.py             
├── main.py                     
│
├── core/                      
│   ├── __init__.py
│   └── moto.py                
│
├── data/                       
│   ├── __init__.py
│   ├── database.py             
│   ├── motos.csv               
│   └── marcas.csv              
│
└── services/                   
    ├── __init__.py
    ├── buscador.py
    ├── comparador.py
    └── scoring.py              
```
## Apartado Gráfico y Menús
Se utilizan prints en la consola donde el usuario ingresa números para escoger ciertas opciones.
```python
bandera : bool = True
    I1 : str = """
        Bienvenido a Look_Vike, comparador de motocicletas \n
            |        Menú Principal       |
            |  1  |  Buscador             |
            |  2  |  Comparador           |
            |  3  |  Cerrar el programa   |
        """
    I2 : str = """
            Opciones de Buscador:
            |    Seleccione una opción    |
            |  1  |    Buscar modelos     |
            |  2  |      Filtrar          |
            |  3  |      Ordenar          |
            |  4  |  Limpiar búsqueda     |
            |  5  |       Atrás           |
        """
    I3 : str = """
            Opciones de Comparación:
            |    Seleccione una opción    |
            |  1  | Agregar moto          |
            |  2  | Comparación           |
            |  3  | Lista ordenada        |
            |  4  | Limpiar comparador    |
            |  5  |       Atrás           |
        """
        # Se guardan las interfaces en un diccionario para facilitar su transporte entre funciones
    Interfaces: dict = {"General": I1,"Buscador":I2, "Comparador": I3}
        
        # Se llama a la función del menú y se ingresan las interfaces junto con la bandera
    menu(Interfaces, bandera)
```
De manera general, para cada menu se utiliza un ciclo while para ingresar la opción, añadiendo un caso de Except si hay un ValueError, y luego se utiliza la estructura mathc-case para derivar al usuario a la función que controla la opción seleccionada, por ejemplo terminar el programa.
```python
def menu(Interfaces: dict, bandera: bool):
    while bandera == True:
        # Mostrar el menú
        print(Interfaces["General"])
        # Se elige una opción de la interfaz mostrada
        try:
            a = int(input("Seleccione una opción: "))
        except ValueError:
            print("Por favor, ingrese un número entero válido.")
            continue
            
        # Ejecutar la opción seleccionada
        match a: # Se redirige a la función deseada por el usuario
            case 1:
                buscador(Interfaces)
            case 2:
                comparador(Interfaces)
            case 3:
                print("Fin del programa")
                bandera = False # Se actualiza la bandera para dar fin al bucle y al programa
            case _:
                print("Opción no válida. Por favor, ingrese un número entre 1 y 3.")
```
## Líneas de mejoramiento
Como parte del desarrollo del programa, se tienen pensados ciertos tipos de mejoras que amplian el funcionamiento del proyecto y que entregan resultados más completos a los usuarios, dentro de estas encontramos:
### Webscrapping
La idea básica del proyecto es tener una base de datos completa que pueda entregarle la información necesaria al usuario, de cualquier motocicleta que desee, sin embargo, el hacer una base de datos propia con tantos modelos puede ser muy extenso, con lo cual el equipo plante la posibilidad de utilizar la metodología "WebScrapping" para obtener datos de forma automatizada y tener una base de datos mucho más amplia.
### Más Vehículos
A pesar de que el pilar del proyecto es facilitar la elección de motocicletas para los usuarios, ya que este mercado es muy diverso para gente sin conocimientos previos, lo cierto es que, también se puede aplicar el mismo enfoque a automoviles, por ejemplo, que a pesar de no tener la misma demanda local, hay personas que pueden llegar a interesarse más por esta función que por la de motos, y así, el equipo considera la posibilidad de añadir otros vehículos al sistema.
### Gráficas de estrella
A la hora de presentar resultados siempre se busca que sean lo más "digeribles" posible para el usuario, así, entregarle un conjunto de datos numéricos o booleanos realmente no ayudaría a la gruesa parte de la población sin tantos conocimientos técnicos sobre el tema, por tanto el equipo considera que lo ideal sería poder representar las características de las motocicletas en una especie de "Diagramas de Estrella" que puedan mostrar que tanto se especializa o es buena una determinada moto en un ambito, por ejemplo ahorro de gasolina.

Un ejemplo de cómo se vería este tipo de gráfico:
[![image.png](https://i.postimg.cc/d3NK6yTG/image.png)](https://postimg.cc/30G6JW1w)

## Web Scraping

Para la creación de la base de datos que se requiere para el proyecto, se realiza un codigo que realice web scrapping a paginas que vendan motos. Se utliza principalmente las bibliotecas de Selenium y el modulo BeautifulSoup de la libreria bs4.

El codigo primero tiene una configuración para que el codigo pueda acceder a la pagina, luego hay un condicional que busca y guarda en una lista, los links de las marcas de motos que se encuentran es la pagina. Despues se tiene principalmente dos funciones, la primera obtiene los links de todas las motos que aparecen en la pagina y los guarda en una lista y la segunda función obtiene la información requerida de la moto.

A continuación, con un for se van accediendo a cada uno de los links de las motos y se van guardando los datos en una lista. Para finalizar con la libreria Pandas se convierte esta lista en un archivo .cvs.

```python
#instalar selenium, pandas,beautifulsoup4, y obtener algo de chrome https://sites.google.com/chromium.org/driver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import pandas as pd
import re #para obtener solo los numeros de un str


options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.galgo.com/co/motos")
wait = WebDriverWait(driver, 10)

carousel = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.ui-core-carousel-renderer div.slick-list"))
)

anchors = carousel.find_elements(By.CSS_SELECTOR, "div.slick-slide a")

#encuentra los links de las marcas de las motos
lista_links = []
for a in anchors:
    href = a.get_attribute("href")
    try:
        img = a.find_element(By.CSS_SELECTOR, "img.ui-core-picture__image")
        alt = img.get_attribute("alt")
    except:
        alt = "desconocido"
    if href:
        lista_links.append(href)

lista_links_final = list(set(lista_links))


#función que encuentra los links de las motos
def links_motos(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    service = Service("chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(6)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    enlaces = soup.select("a.ui-core-action.ui-core-action--link[href]")

    links_motos = [a["href"] for a in enlaces if a["href"].startswith("/co/motos/CO")]
    links_motos_final = ["https://www.galgo.com" + link for link in dict.fromkeys(links_motos)]

    driver.quit()
    return links_motos_final

def limpiar_numeros(texto): #filtra los digitos de un str
    return ''.join(re.findall(r'[\d.,]+', texto))

#función que obtiene toda la información relevante de las motos
def scraping_inf_motos(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    service = Service("chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.ui-core-typography--xxlarge"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    nombre_tag = soup.find("span", class_="ui-core-breadcrumb__item")
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Modelo no encontrado"

    marca_tag = soup.find("ol", class_="ui-core-breadcrumb")
    marca_list = (
        [a.get_text(strip=True) for a in marca_tag.find_all("a")]
        if marca_tag else ["Breadcrumb no encontrado"]
    )
    marca = marca_list[2]

    frenos_del_tag = soup.select_one("div.ui-core-typography--small")
    frenos_delanteros = frenos_del_tag.get_text(strip=True) if frenos_del_tag else "Frenos delanteros no encontrados"

    frenos_tras_list = soup.select("div.ui-core-typography.ui-core-typography--small")
    frenos_traseros = frenos_tras_list[-1].get_text(strip=True) if frenos_tras_list else "Frenos traseros no encontrados"

    peso_tag = soup.select_one(
        "div.ui-core-typography.ui-core-composed-text__typography.ui-core-typography--small"
    )
    peso = peso_tag.get_text(strip=True) if peso_tag else "Peso no encontrado"

    transmision_tag = soup.select_one(
        "div.ui-core-typography.ui-core-composed-text__typography.ui-core-typography--small"
    )
    transmision = transmision_tag.get_text(strip=True) if transmision_tag else "Transmisión no encontrada"

    torque_tag = soup.select_one("div.ui-core-typography.ui-core-typography--small.ui-core-typography--neutral-900")
    torque = torque_tag.get_text(strip=True) if torque_tag else "Torque no encontrado"

    potencia_tag = soup.select_one("div.ui-core-typography.ui-core-typography--small.ui-core-typography--neutral-900")
    potencia = potencia_tag.get_text(strip=True) if potencia_tag else "Potencia no encontrada"

    capacidad_tanque_tag = soup.select_one(
        "div.ui-core-typography.ui-core-typography--small.ui-core-typography--neutral-900"
    )
    capacidad_tanque = capacidad_tanque_tag.get_text(strip=True) if capacidad_tanque_tag else "Capacidad no encontrada"

    garantia_tag = soup.find("div",
                             class_="ui-core-typography ui-core-composed-text__typography ui-core-typography--center ui-core-typography--small ui-core-typography--normal ui-core-typography--neutral-900")
    garantia = garantia_tag.get_text(strip=True) if garantia_tag else "Garantía no encontrada"

    precio_tag = soup.select_one(
        "div.ui-core-typography.ui-core-columns__typography.ui-core-typography--right.ui-core-typography--xlarge"
    )
    precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no encontrado"
    precio = limpiar_numeros(precio)

    driver.quit()

    return {
        "nombre": nombre,
        "marca": marca,
        "peso": peso,
        "transmision": transmision,
        "torque": torque,
        "potencia": potencia,
        "tipos de frenos delanteros": frenos_delanteros,
        "tipos de frenos traseros": frenos_traseros,
        "capacidad del tanque": capacidad_tanque,
        "garantia": garantia,
        "precio": precio
    }


#lol = scraping_inf_motos("https://www.galgo.com/co/motos/CO731-tvs-raider-125?sku=109702006")

#print(lol)

datos = []

for i in lista_links_final:
    print(i)
    links = links_motos(i)
    for j in links:
        info_motos = scraping_inf_motos(j)
        datos.append(info_motos)
        time.sleep(random.uniform(2, 5))

print(datos)
#df = pd.DataFrame(datos)
#df.to_csv("motos.csv", index=False, encoding="utf-8-sig")

driver.quit()
```
