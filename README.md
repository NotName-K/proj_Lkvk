# proj_LVK
## Logo del grupo
![Logo](https://github.com/NotName-K/POO-R2/blob/main/Screenshot%202025-09-23%20110719.png?raw=true)

## Comparador y Análisis de Motocicletas en Python.
[Logo]

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
