class MotorSpecs:
    def __init__(self, ciclos, cilindros, arbol_levas, refrigeracion, arranque, 
                 cilindraje, potencia, torque, combustible, embrague, sliper_clutch, inyeccion):
        self.ciclos = ciclos
        self.cilindros = cilindros
        self.arbol_levas = arbol_levas
        self.refrigeracion = refrigeracion
        self.arranque = arranque
        self.cilindraje = cilindraje
        self.potencia = potencia
        self.torque = torque
        self.combustible = combustible
        self.embrague = embrague
        self.sliper_clutch = sliper_clutch
        self.inyeccion = inyeccion

    def motor_db(db, moto_id):
        data = db.get_moto(moto_id)
        if data:
            return MotorSpecs(
                "4 tiempos",
                data['tipo'],
                "DOHC",
                "Líquido",
                "Eléctrico",
                data['cilindraje'],
                data['potencia'],
                data['torque'],
                "Gasolina",
                data['transmision'],
                False,
                "Electrónica"
            )
        return None


class Motor:
    def __init__(self, specs):
        self.ciclos = specs.ciclos
        self.cilindros = specs.cilindros
        self.arbol_levas = specs.arbol_levas
        self.refrigeracion = specs.refrigeracion
        self.arranque = specs.arranque
        self.cilindraje = specs.cilindraje
        self.potencia = specs.potencia
        self.torque = specs.torque
        self.combustible = specs.combustible
        self.embrague = specs.embrague
        self.sliper_clutch = specs.sliper_clutch
        self.inyeccion = specs.inyeccion


class SistemaElectronicoSpecs:
    def __init__(self, bateria, faros, direccionales, tablero):
        self.bateria = bateria
        self.faros = faros
        self.direccionales = direccionales
        self.tablero = tablero

    def se_db(db, moto_id):
        data = db.get_moto(moto_id)
        if data:
            return SistemaElectronicoSpecs(
                "12V",
                data['iluminacion'],
                "LED",
                5
            )
        return None


class SistemaElectronico:
    def __init__(self, specs):
        self.bateria = specs.bateria
        self.faros = specs.faros
        self.direccionales = specs.direccionales
        self.tablero = specs.tablero


class ChasisSpecs:
    def __init__(self, tipo, suspension_d, suspension_t, freno_d, freno_t, neumaticos, abs_sistema):
        self.tipo = tipo
        self.suspension_d = suspension_d
        self.suspension_t = suspension_t
        self.freno_d = freno_d
        self.freno_t = freno_t
        self.neumaticos = neumaticos
        self.abs = abs_sistema

    def desde_db(db, moto_id):
        data = db.get_moto(moto_id)
        if data:
            susp = data['suspension'].split(',')
            susp_d = susp[0].replace('Delantera:', '').strip() if len(susp) > 0 else ""
            susp_t = susp[1].replace('Trasera:', '').strip() if len(susp) > 1 else ""
            
            return ChasisSpecs(
                data['tipo'],
                susp_d,
                susp_t,
                data['frenos_delanteros'],
                data['frenos_traseros'],
                data['neumaticos'],
                data['seguridad']
            )
        return None


class Chasis:
    def __init__(self, specs):
        self.tipo = specs.tipo
        self.suspension_d = specs.suspension_d
        self.suspension_t = specs.suspension_t
        self.freno_d = specs.freno_d
        self.freno_t = specs.freno_t
        self.neumaticos = specs.neumaticos
        self.abs = specs.abs


class DimensionesSpecs:
    def __init__(self, largo, ancho, altura, altura_asiento, distancia_ejes, peso, capacidad_tanque):
        self.largo = largo
        self.ancho = ancho
        self.altura = altura
        self.altura_asiento = altura_asiento
        self.distancia_ejes = distancia_ejes
        self.peso = peso
        self.capacidad_tanque = capacidad_tanque

    def desde_db(db, moto_id):
        data = db.get_moto(moto_id)
        if data:
            return DimensionesSpecs(
                2100,
                800,
                1100,
                805,
                1400,
                data['peso'],
                data['capacidad_tanque']
            )
        return None


class Dimensiones:
    def __init__(self, specs):
        self.largo = specs.largo
        self.ancho = specs.ancho
        self.altura = specs.altura
        self.altura_asiento = specs.altura_asiento
        self.distancia_ejes = specs.distancia_ejes
        self.peso = specs.peso
        self.capacidad_tanque = specs.capacidad_tanque


class RendimientoSpecs:
    def __init__(self, consumo_medio, autonomia, vel_crucero, top_speed):
        self.consumo = consumo_medio
        self.autonomia = autonomia
        self.vel_crucero = vel_crucero
        self.top_speed = top_speed

    def desde_db(db, moto_id):
        data = db.get_moto(moto_id)
        if data:
            consumo = data['consumo']
            tanque = data['capacidad_tanque']
            autonomia = consumo * tanque if consumo and tanque else 0
            
            return RendimientoSpecs(
                consumo,
                autonomia,
                data['vel_crucero'],
                data['top_speed']
            )
        return None


class Rendimiento:
    def __init__(self, specs):
        self.consumo_medio = specs.consumo_medio
        self.autonomia = specs.autonomia
        self.vel_crucero = specs.vel_crucero
        self.top_speed = specs.top_speed


class InfoGeneralSpecs:
    def __init__(self, marca, modelo, año, precio, colores, accesorios, fallos):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.precio = precio
        self.colores = colores
        self.accesorios = accesorios
        self.fallos = fallos

    def desde_db(db, moto_id):
        data = db.get_moto(moto_id)
        if data:
            colores = data['color'].split(',') if data['color'] else []
            accesorios = data['accesorios'].split(',') if data['accesorios'] else []
            fallos = data['fallos_comunes'].split(',') if data['fallos_comunes'] else []
            
            return InfoGeneralSpecs(
                data['marca'],
                data['modelo'],
                2024,
                data['precio'],
                colores,
                accesorios,
                fallos
            )
        return None


class InfoGeneral:
    def __init__(self, specs):
        self.marca = specs.marca
        self.modelo = specs.modelo
        self.año = specs.año
        self.precio = specs.precio
        self.colores = specs.colores
        self.accesorios = specs.accesorios
        self.fallos = specs.fallos
