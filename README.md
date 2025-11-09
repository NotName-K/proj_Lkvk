# proj_LVK
Comparador y Análisis de Motocicletas en Python.
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
```mermaid
classDiagram
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
        + estiloDeConduccion() string
    }

    class MotoDeportiva {
        + modoDeConduccion() string
    }


    class MotoTouring {
        + capacidadDeCarga() float
    }

    class MotoScooter {
        + tipoDeTransmision() string
    }

Moto <|-- MotoNaked
    Moto <|-- MotoDeportiva
    Moto <|-- MotoTouring
    Moto <|-- MotoScooter
```
### Base de Datos
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
```
### Análisis de Motos
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
```
### KronoScore
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
```

## Comparativa
```mermaid
    class Comparador {
    - listaMotos : List~Moto~
    - motosSeleccionadas : List~Moto~
    - resultadoComparacion : Map~string, Moto~
    + agregarMoto(moto : Moto) void
    + mostrarComparacion() void
    + graficaComparacion(formato : ) void
    + limpiarComparador() void
}
```
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
