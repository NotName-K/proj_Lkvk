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

def buscador(Interfaces: dict):
    while True:
        print(Interfaces["Buscador"])
        try:
            a = int(input("Seleccione una opción: "))
        except ValueError:
            print("Por favor, ingrese un número entero válido.")
            continue
                
        # Ejecutar la opción seleccionada
        match a: # Se redirige a la función deseada por el usuario
            case 1:
                buscar(Interfaces)
            case 2:
                filtros(Interfaces)
            case 3:
                orden(Interfaces)
            case 4:
                limpiar_busc(Interfaces)
            case 5:
                break
            case _:
                print("Opción no válida. Por favor, ingrese un número entre 1 y 5.")

def buscar(Interfaces):
    pass
def filtros(Interfaces):
    pass
def orden(Interfaces):
    pass
def limpiar_busc(Interfaces):
    pass

def comparador(Interfaces: dict):
    while True:
        print(Interfaces["Comparador"])
        try:
            a = int(input("Seleccione una opción: "))
        except ValueError:
            print("Por favor, ingrese un número entero válido.")
            continue
                
        # Ejecutar la opción seleccionada
        match a: # Se redirige a la función deseada por el usuario
            case 1:
                agregar_moto()
            case 2:
                comparacion()
            case 3:
                lista_orden()
            case 4:
                limpiar_comp()
            case 5:
                break
            case _:
                print("Opción no válida. Por favor, ingrese un número entre 1 y 5.")

def agregar_moto():
    pass

def comparacion():
    pass

def lista_orden():
    pass

def limpiar_comp():
    pass

if __name__ == "__main__":
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