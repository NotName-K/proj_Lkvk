import moto_parts 
class Moto:
    def __init__(self, db, moto_id):
        motor_specs = MotorSpecs.desde_db(db, moto_id)
        se_specs = SistemaElectronicoSpecs.desde_db(db, moto_id)
        chasis_specs = ChasisSpecs.desde_db(db, moto_id)
        dim_specs = DimensionesSpecs.desde_db(db, moto_id)
        rend_specs = RendimientoSpecs.desde_db(db, moto_id)
        info_specs = InfoGeneralSpecs.desde_db(db, moto_id)
        
        
        self.motor = Motor(motor_specs)
        self.sistema_electronico = SistemaElectronico(se_specs)
        self.chasis = Chasis(chasis_specs)
        self.dimensiones = Dimensiones(dim_specs)
        self.rendimiento = Rendimiento(rend_specs)
        self.info = InfoGeneral(info_specs)
        
        self.marca = self.info.marca
        self.modelo = self.info.modelo
        self.año = self.info.año
        self.cilindrada = self.motor.cilindraje
        self.potencia = self.motor.potencia
        self.par_motor = self.motor.torque
        self.peso = self.dimensiones.peso
        self.tipo_combustible = self.motor.combustible
        self.consumo_medio = self.rendimiento.consumo_medio
        self.capacidad_deposito = self.dimensiones.capacidad_tanque
        self.autonomia = self.rendimiento.autonomia
        self.tipo_transmision = self.motor.embrague
        self.numero_marchas = 6
        self.suspension_delantera = self.chasis.suspension_d
        self.suspension_trasera = self.chasis.suspension_t
        self.freno_delantero = self.chasis.freno_d
        self.freno_trasero = self.chasis.freno_t
        self.neumatico_delantero = self.chasis.neumaticos
        self.neumatico_trasero = self.chasis.neumaticos
        self.altura_asiento = self.dimensiones.altura_asiento
        self.distancia_ejes = self.dimensiones.distancia_ejes
        self.tipo_chasis = self.chasis.tipo
        self.precio_base = self.info.precio
        self.color_disponible = self.info.colores

    def calcular_score(self):
        score = 0
        return score



class Moto_naked(Moto):
    def __init__(self, db, moto_id):
        super().__init__(db, moto_id)
        self.manillar_ancho = "Ancho"
        self.posicion_conduccion = "Erguida"
        self.versatilidad_urbana = 9
        
    def ficha_tecnica(self):
        pass
    

class Moto_sport(Moto):
    def __init__(self, db, moto_id):
        super().__init__(db, moto_id)
        self.carenado = "Completo"
        self.velocidad_maxima = self.rendimiento.top_speed
        self.aceleracion_0a100 = 3.5
        self.modos_conduccion = ["Sport", "Rain", "Road"]
        
    def ficha_tecnica(self):
        pass
    


class Moto_touring(Moto):
    def __init__(self, db, moto_id):
        super().__init__(db, moto_id)
        self.capacidad_maletas = 60
        self.control_crucero = True
        self.protection_bajas = "Alta"

    def ficha_tecnica(self):
        pass
    

class Moto_scooter(Moto):
    def __init__(self, db, moto_id):
        super().__init__(db, moto_id)
        self.espacio_baul = 25
        self.porta_casco = True
        self.gancho_transporte = True

    def ficha_tecnica(self):
        pass

class Moto_street(Moto):
    pass

class Moto_cross(Moto):
    pass

class Moto_quad(Moto):
    pass

class Moto_electric(Moto):
    pass

class Moto_enduro(Moto):
    pass

class Moto_chopper(Moto):
    pass

class moto_cruiser(Moto):
    pass

class moto_custom(Moto):
    pass

class moto_dps(Moto):
    pass

class Moto_carro(Moto):
    pass

class moto_trial(Moto):
    pass
