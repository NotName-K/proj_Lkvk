class InfoGeneral:
    def __init__(self, data):
        self.id = data["id"]
        self.marca = data["marca"]
        self.modelo = data["modelo"]
        self.año = data["año"]
        self.tipo = data["tipo"]
        self.color = data["color"]
        self.precio = data["precio"]
        self.fallos_comunes = data["fallos_comunes"]

    def get_colores_lista(self):
        if self.color:
            return [c.strip() for c in self.color.split(",")]
        return []

    def get_fallos_lista(self):
        if self.fallos_comunes:
            return [f.strip() for f in self.fallos_comunes.split(",")]
        return []

    def to_dict(self):
        return {
            "Marca": self.marca,
            "Modelo": self.modelo,
            "Año": self.año,
            "Tipo": self.tipo.upper(),
            "Color": self.color or "N/A",
            "Precio": f"${self.precio:,.0f}" if self.precio else "N/A",
        }


class Motor:
    def __init__(self, data):
        self.cilindraje = data["cilindraje"]
        self.tiempos = data["tiempos"]
        self.cilindros = data["cilindros"]
        self.arbol_levas = data["arbol_levas"]
        self.refrigeracion = data["refrigeracion"]
        self.arranque = data["arranque"]
        self.embrague = data["embrague"]
        self.sliper_clutch = data["sliper_clutch"]
        self.inyeccion = data["inyeccion"]
        self.potencia = data["potencia"]
        self.torque = data["torque"]

    def es_valido(self):
        return self.cilindraje is not None

    def to_dict(self):
        if not self.es_valido():
            return {}

        info = {
            "Cilindraje": f"{self.cilindraje} cc",
            "Potencia": self.potencia or "N/A",
            "Torque": self.torque or "N/A",
        }

        if self.tiempos:
            info["Tiempos"] = self.tiempos
        if self.cilindros:
            info["Cilindros"] = self.cilindros
        if self.arbol_levas:
            info["Árbol levas"] = self.arbol_levas
        if self.refrigeracion:
            info["Refrigeración"] = self.refrigeracion
        if self.arranque:
            info["Arranque"] = self.arranque
        if self.embrague:
            info["Embrague"] = self.embrague
        if self.sliper_clutch:
            info["Sliper clutch"] = self.sliper_clutch
        if self.inyeccion:
            info["Inyección"] = self.inyeccion

        return info


class MotorElectrico:
    def __init__(self, data):
        self.bateria_capacidad = data["bateria_capacidad"]
        self.autonomia_electrica = data["autonomia_electrica"]
        self.tiempo_carga = data["tiempo_carga"]
        self.potencia = data["potencia"]
        self.torque = data["torque"]

    def es_valido(self):
        return self.bateria_capacidad is not None

    def to_dict(self):
        info = {}
        if self.potencia:
            info["Potencia"] = self.potencia
        if self.torque:
            info["Torque"] = self.torque
        if self.bateria_capacidad:
            info["Capacidad batería"] = f"{self.bateria_capacidad} kWh"
        if self.autonomia_electrica:
            info["Autonomía eléctrica"] = f"{self.autonomia_electrica} km"
        if self.tiempo_carga:
            info["Tiempo de carga"] = f"{self.tiempo_carga} h"
        return info


class Transmision:
    def __init__(self, data):
        self.tipo = data["transmision"]
        self.caja_cambios = data["caja_cambios"]

    def es_automatica(self):
        return self.tipo and "automática" in self.tipo.lower()

    def es_mecanica(self):
        return self.tipo and "mecánica" in self.tipo.lower()

    def to_dict(self):
        info = {"Transmisión": self.tipo or "N/A"}
        if self.caja_cambios:
            info["Caja cambios"] = self.caja_cambios
        return info


class Rendimiento:
    def __init__(self, data):
        self.consumo = data["consumo"]
        self.capacidad_tanque = data["capacidad_tanque"]
        self.vel_crucero = data["vel_crucero"]
        self.top_speed = data["top_speed"]

        if self.consumo and self.capacidad_tanque:
            self.autonomia = self.consumo * self.capacidad_tanque
        else:
            self.autonomia = None

    def to_dict(self):
        info = {}
        if self.consumo:
            info["Consumo"] = f"{self.consumo} km/l"
        if self.capacidad_tanque:
            info["Capacidad tanque"] = f"{self.capacidad_tanque} L"
        if self.autonomia:
            info["Autonomía"] = f"{self.autonomia:.0f} km"
        if self.vel_crucero:
            info["Velocidad crucero"] = f"{self.vel_crucero} km/h"
        if self.top_speed:
            info["Velocidad máxima"] = f"{self.top_speed} km/h"
        return info


class SistemaElectronico:
    def __init__(self, data):
        self.faros = data.get("faros")
        self.direccionales = data.get("direccionales")
        self.abs_sistema = data.get("abs_sistema")

    def tiene_abs(self):
        return self.abs_sistema is not None

    def to_dict(self):
        info = {}
        if self.faros:
            info["Faros"] = self.faros
        if self.direccionales:
            info["Direccionales"] = self.direccionales
        if self.abs_sistema:
            info["ABS"] = self.abs_sistema
        return info


class Chasis:
    def __init__(self, data):
        self.suspension_d = data["suspension_d"]
        self.suspension_t = data["suspension_t"]
        self.freno_d = data["freno_d"]
        self.freno_t = data["freno_t"]
        self.neumaticos = data["neumaticos"]

    def to_dict(self):
        info = {}
        if self.suspension_d:
            info["Suspensión delantera"] = self.suspension_d
        if self.suspension_t:
            info["Suspensión trasera"] = self.suspension_t
        if self.freno_d:
            info["Freno delantero"] = self.freno_d
        if self.freno_t:
            info["Freno trasero"] = self.freno_t
        if self.neumaticos:
            info["Neumáticos"] = self.neumaticos
        return info


class Dimensiones:
    def __init__(self, data):
        self.largo = data["largo"]
        self.ancho = data["ancho"]
        self.altura = data["altura"]
        self.distancia_ejes = data["distancia_ejes"]
        self.altura_asiento = data["altura_asiento"]
        self.peso = data["peso"]

    def get_dimensiones_str(self):
        if self.largo and self.ancho and self.altura:
            return f"{self.largo} x {self.ancho} x {self.altura} mm"
        return None

    def to_dict(self):
        info = {}
        dim_str = self.get_dimensiones_str()
        if dim_str:
            info["Dimensiones (LxAxH)"] = dim_str
        if self.distancia_ejes:
            info["Distancia ejes"] = f"{self.distancia_ejes} mm"
        if self.altura_asiento:
            info["Altura asiento"] = f"{self.altura_asiento} mm"
        if self.peso:
            info["Peso"] = f"{self.peso} kg"
        return info


class Atb_Sport:
    def __init__(self, data):
        self.aceleracion_0_100 = data.get("aceleracion_0_100")
        self.modos_manejo = data.get("modos_manejo")

    def to_dict(self):
        info = {}
        if self.aceleracion_0_100:
            info["Aceleración 0_100"] = f"{self.aceleracion_0_100} s"
        if self.modos_manejo:
            info["Modos conducción"] = self.modos_manejo
        return info


class Atb_Naked:
    def __init__(self, data):
        self.aceleracion_0_100 = data.get("aceleracion_0_100")

    def to_dict(self):
        info = {}
        if self.aceleracion_0_100:
            info["Aceleración 0_100"] = f"{self.aceleracion_0_100} s"
        return info


class Atb_Touring:
    def __init__(self, data):
        self.capacidad_maletas = data.get("capacidad_maletas")
        self.parabrisas_ajustable = data.get("parabrisas_ajustable")
        self.control_crucero = data.get("control_crucero")
        self.tanque_grande = data.get("tanque_grande")
        self.proteccion_motor = data.get("proteccion_motor")
        self.suspension_largo_recorrido = data.get("suspension_largo_recorrido")
        self.modos_manejo = data.get("modos_manejo")

    def to_dict(self):
        info = {}
        if self.capacidad_maletas:
            info["Capacidad maletas"] = f"{self.capacidad_maletas} L"
        if self.parabrisas_ajustable:
            info["Parabrisas ajustable"] = self.parabrisas_ajustable
        if self.control_crucero:
            info["Control crucero"] = self.control_crucero
        if self.tanque_grande:
            info["Tanque grande"] = self.tanque_grande
        if self.proteccion_motor:
            info["Protección motor"] = self.proteccion_motor
        if self.suspension_largo_recorrido:
            info["Recorrido suspensión"] = self.suspension_largo_recorrido
        if self.modos_manejo:
            info["Modos manejo"] = self.modos_manejo
        return info


class Atb_Scooter:
    def __init__(self, data):
        self.espacio_baul = data.get("espacio_baul")

    def to_dict(self):
        info = {}
        if self.espacio_baul:
            info["Espacio baúl"] = f"{self.espacio_baul} L"
        return info


class Atb_DoblePps:
    def __init__(self, data):
        self.suspension_largo_recorrido = data.get("suspension_largo_recorrido")
        self.proteccion_motor = data.get("proteccion_motor")
        self.tanque_grande = data.get("tanque_grande")

    def to_dict(self):
        info = {}
        if self.suspension_largo_recorrido:
            info["Recorrido suspensión"] = f"{self.suspension_largo_recorrido} mm"
        if self.proteccion_motor:
            info["Protección motor"] = self.proteccion_motor
        if self.tanque_grande:
            info["Tanque grande"] = self.tanque_grande
        return info


class Atb_Motocarro:
    def __init__(self, data):
        self.capacidad_pasajeros = data.get("capacidad_pasajeros")
        self.capacidad_carga = data.get("capacidad_carga")

    def to_dict(self):
        info = {}
        if self.capacidad_pasajeros:
            info["Capacidad pasajeros"] = self.capacidad_pasajeros
        if self.capacidad_carga:
            info["Capacidad carga"] = f"{self.capacidad_carga} kg"
        return info


class Moto:
    def __init__(self, moto_id, data):
        self.moto_id = moto_id
        self.data = data
        self.info = InfoGeneral(data)
        self.transmision = Transmision(data)
        self.electronica = SistemaElectronico(data)
        self.chasis = Chasis(data)
        self.dimensiones = Dimensiones(data)

        if self.es_electrica():
            self.motor = MotorElectrico(data)
            self.rendimiento = None
        else:
            self.motor = Motor(data)
            self.rendimiento = Rendimiento(data)

        self.atributos_especificos = self._crear_atributos_especificos()

    def obtener_criterios_comparacion(self):
        """Retorna dict con criterios relevantes para este tipo"""
        raise NotImplementedError

    def obtener_tags_busqueda(self):
        """Retorna lista de tags para búsqueda"""
        raise NotImplementedError

    def obtener_metricas_score(self):
        """Retorna dict con métricas que krono_score necesita"""
        raise NotImplementedError

    def _crear_atributos_especificos(self):
        tipo = self.info.tipo.lower()

        if tipo == "sport":
            return Atb_Sport(self.data)
        elif tipo == "touring":
            return Atb_Touring(self.data)
        elif tipo == "scooter":
            return Atb_Scooter(self.data)
        elif tipo == "doble pps":
            return Atb_DoblePps(self.data)
        elif tipo == "adventure":
            return Atb_Touring(self.data)
        elif tipo == "motocarro":
            return Atb_Motocarro(self.data)
        else:
            return None

    def es_electrica(self):
        return self.info.tipo.lower() == "electric"

    def es_combustion(self):
        return not self.es_electrica()

    def ficha_completa(self):
        ficha = {}

        ficha.update(self.info.to_dict())
        ficha.update(self.motor.to_dict())
        ficha.update(self.transmision.to_dict())

        if self.rendimiento:
            ficha.update(self.rendimiento.to_dict())

        ficha.update(self.electronica.to_dict())
        ficha.update(self.chasis.to_dict())
        ficha.update(self.dimensiones.to_dict())

        if self.atributos_especificos:
            ficha.update(self.atributos_especificos.to_dict())

        if self.info.fallos_comunes:
            ficha["Fallos comunes"] = self.info.fallos_comunes

        return ficha

    def mostrar_ficha(self):
        print("\n" + "=" * 70)
        titulo = f"{self.info.marca} {self.info.modelo} — {self.info.tipo.upper()}"
        print(titulo.center(70))
        print("=" * 70 + "\n")

        for clave, valor in self.ficha_completa().items():
            print(f"{clave:.<35} {valor}")

        print("\n" + "=" * 70 + "\n")

    def __str__(self):
        return f"{self.info.marca} {self.info.modelo} ({self.info.año})"

    def __repr__(self):
        return f"Moto(id='{self.info.id}', marca='{self.info.marca}', modelo='{self.info.modelo}')"


class MotoSport(Moto):
    def obtener_criterios_comparacion(self):
        return {
            "categoria": "rendimiento",
            "aceleracion": self.atributos_especificos.aceleracion_0_100,
            "potencia": self.motor.potencia,
            "cilindraje": self.motor.cilindraje,
            "peso": self.dimensiones.peso,
            "velocidad_maxima": self.rendimiento.top_speed
            if self.rendimiento
            else None,
            "peso_potencia_ratio": self._calcular_ratio_peso_potencia(),
        }

    def obtener_tags_busqueda(self):
        tags = ["deportiva", "sport"]
        if self.motor.cilindraje >= 1000:
            tags.extend(["superbike", "alta_cilindrada"])
        if self.motor.cilindraje <= 400:
            tags.extend(["sport_media", "principiante"])
        if (
            self.atributos_especificos.aceleracion_0_100
            and self.atributos_especificos.aceleracion_0_100 < 4
        ):
            tags.append("alto_rendimiento")
        if self.electronica.tiene_abs():
            tags.append("con_abs")
        return tags

    def obtener_metricas_score(self):
        return {
            "tipo": "sport",
            "aceleracion": self.atributos_especificos.aceleracion_0_100,
            "potencia_bruta": self._extraer_hp(self.motor.potencia),
            "cilindraje": self.motor.cilindraje,
            "peso": self.dimensiones.peso,
            "tiene_modos": self.atributos_especificos.modos_manejo is not None,
            "precio": self.info.precio,
        }

    def _calcular_ratio_peso_potencia(self):
        if not self.dimensiones.peso or not self.motor.potencia:
            return None
        hp = self._extraer_hp(self.motor.potencia)
        if hp:
            return self.dimensiones.peso / hp
        return None

    def _extraer_hp(self, potencia_str):
        if not potencia_str:
            return None
        import re

        match = re.search(r"(\d+\.?\d*)\s*hp", potencia_str.lower())
        if match:
            return float(match.group(1))
        return None


class MotoTouring(Moto):
    def obtener_criterios_comparacion(self):
        return {
            "categoria": "touring_adventure",
            "autonomia": self.rendimiento.autonomia if self.rendimiento else None,
            "capacidad_maletas": self.atributos_especificos.capacidad_maletas,
            "tiene_control_crucero": self.atributos_especificos.control_crucero == "Sí",
            "tiene_parabrisas_ajustable": self.atributos_especificos.parabrisas_ajustable
            == "Sí",
            "tiene_maletas_laterales": self.atributos_especificos.maletas_laterales
            == "Sí",
            "suspension_ajustable": self.atributos_especificos.suspension_ajustable
            == "Sí",
            "proteccion_motor": self.atributos_especificos.proteccion_motor == "Sí",
            "altura_asiento": self.dimensiones.altura_asiento,
            "precio": self.info.precio,
        }

    def obtener_tags_busqueda(self):
        tags = ["touring", "viaje", "carretera"]

        if (
            self.rendimiento
            and self.rendimiento.autonomia
            and self.rendimiento.autonomia > 400
        ):
            tags.append("larga_distancia")
        if (
            self.atributos_especificos.capacidad_maletas
            and self.atributos_especificos.capacidad_maletas > 30
        ):
            tags.append("gran_capacidad")
        if self.atributos_especificos.control_crucero == "Sí":
            tags.append("control_crucero")
        if self.dimensiones.altura_asiento and self.dimensiones.altura_asiento < 800:
            tags.append("asiento_bajo")

        # Tags tipo adventure
        if self.atributos_especificos.maletas_laterales == "Sí":
            tags.extend(["adventure", "equipada_viaje"])
        if self.atributos_especificos.suspension_ajustable == "Sí":
            tags.extend(["adventure", "suspension_premium"])
        if self.atributos_especificos.proteccion_motor == "Sí":
            tags.append("protegida")
        if self.atributos_especificos.modos_manejo:
            tags.extend(["adventure", "multimodo"])
        if self.motor.cilindraje and self.motor.cilindraje > 900:
            tags.append("gran_adventure")
        if self.atributos_especificos.tanque_grande == "Sí":
            tags.append("gran_autonomia")

        return tags

    def obtener_metricas_score(self):
        return {
            "tipo": "touring",
            "autonomia": self.rendimiento.autonomia if self.rendimiento else None,
            "confort_score": self._calcular_confort_basico(),
            "capacidad_aventura_score": self._calcular_capacidad_aventura(),
            "capacidad_carga": self.atributos_especificos.capacidad_maletas,
            "precio": self.info.precio,
        }

    def _calcular_confort_basico(self):
        score = 0
        if self.atributos_especificos.control_crucero == "Sí":
            score += 30
        if self.atributos_especificos.parabrisas_ajustable == "Sí":
            score += 30
        if self.dimensiones.altura_asiento and self.dimensiones.altura_asiento < 800:
            score += 20
        if (
            self.atributos_especificos.capacidad_maletas
            and self.atributos_especificos.capacidad_maletas > 30
        ):
            score += 20
        return score

    def _calcular_capacidad_aventura(self):
        score = 0
        if self.atributos_especificos.maletas_laterales == "Sí":
            score += 25
        if self.atributos_especificos.proteccion_motor == "Sí":
            score += 20
        if self.atributos_especificos.suspension_ajustable == "Sí":
            score += 30
        if self.atributos_especificos.modos_manejo:
            score += 25
        return score


class MotoScooter(Moto):
    def obtener_criterios_comparacion(self):
        return {
            "categoria": "urbano",
            "cilindraje": self.motor.cilindraje,
            "espacio_baul": self.atributos_especificos.espacio_baul,
            "consumo": self.rendimiento.consumo if self.rendimiento else None,
            "peso": self.dimensiones.peso,
            "precio": self.info.precio,
        }

    def obtener_tags_busqueda(self):
        tags = ["scooter", "automatica", "urbana"]
        if self.motor.cilindraje <= 125:
            tags.extend(["A1", "baja_cilindrada"])
        if self.motor.cilindraje >= 300:
            tags.extend(["maxiscooter", "carretera"])
        if (
            self.atributos_especificos.espacio_baul
            and self.atributos_especificos.espacio_baul >= 30
        ):
            tags.append("baul_grande")
        if (
            self.rendimiento
            and self.rendimiento.consumo
            and self.rendimiento.consumo > 40
        ):
            tags.append("economico")
        return tags

    def obtener_metricas_score(self):
        return {
            "tipo": "scooter",
            "cilindraje": self.motor.cilindraje,
            "practicidad_score": self._calcular_practicidad(),
            "consumo": self.rendimiento.consumo if self.rendimiento else None,
            "precio": self.info.precio,
        }

    def _calcular_practicidad(self):
        score = 0
        if self.atributos_especificos.espacio_baul:
            score += min(self.atributos_especificos.espacio_baul, 50)
        if self.dimensiones.altura_asiento and self.dimensiones.altura_asiento < 750:
            score += 25
        if self.dimensiones.peso and self.dimensiones.peso < 150:
            score += 25
        return score


class MotoElectric(Moto):
    def obtener_criterios_comparacion(self):
        return {
            "categoria": "electrica",
            "autonomia": self.motor.autonomia_electrica,
            "bateria": self.motor.bateria_capacidad,
            "tiempo_carga": self.motor.tiempo_carga,
            "precio": self.info.precio,
            "costo_km": self._calcular_costo_km(),
        }

    def obtener_tags_busqueda(self):
        tags = ["electrica", "cero_emisiones", "silenciosa"]
        if self.motor.autonomia_electrica and self.motor.autonomia_electrica < 100:
            tags.append("urbana_exclusiva")
        if self.motor.autonomia_electrica and self.motor.autonomia_electrica > 200:
            tags.append("larga_autonomia")
        if self.motor.tiempo_carga and self.motor.tiempo_carga < 2:
            tags.append("carga_rapida")
        return tags

    def obtener_metricas_score(self):
        return {
            "tipo": "electric",
            "autonomia": self.motor.autonomia_electrica,
            "eficiencia_score": self._calcular_eficiencia(),
            "bateria": self.motor.bateria_capacidad,
            "precio": self.info.precio,
        }

    def _calcular_costo_km(self, costo_kwh=500):
        if not self.motor.bateria_capacidad or not self.motor.autonomia_electrica:
            return None
        costo_carga = self.motor.bateria_capacidad * costo_kwh
        return costo_carga / self.motor.autonomia_electrica

    def _calcular_eficiencia(self):
        if not self.motor.bateria_capacidad or not self.motor.autonomia_electrica:
            return 0
        return (self.motor.autonomia_electrica / self.motor.bateria_capacidad) * 10


class MotoDoblePps(Moto):
    def obtener_criterios_comparacion(self):
        return {
            "categoria": "mixto",
            "recorrido_suspension": self.atributos_especificos.suspension_largo_recorrido,
            "tiene_proteccion": self.atributos_especificos.proteccion_motor == "Sí",
            "autonomia": self.rendimiento.autonomia if self.rendimiento else None,
            "altura_asiento": self.dimensiones.altura_asiento,
            "peso": self.dimensiones.peso,
            "precio": self.info.precio,
        }

    def obtener_tags_busqueda(self):
        tags = ["doble_proposito", "versatil", "trail"]
        if (
            self.atributos_especificos.suspension_largo_recorrido
            and self.atributos_especificos.suspension_largo_recorrido > 150
        ):
            tags.append("offroad_capable")
        if self.atributos_especificos.proteccion_motor == "Sí":
            tags.append("protegida")
        if (
            self.rendimiento
            and self.rendimiento.autonomia
            and self.rendimiento.autonomia > 350
        ):
            tags.append("gran_autonomia")
        return tags

    def obtener_metricas_score(self):
        return {
            "tipo": "doble_pps",
            "versatilidad_score": self._calcular_versatilidad(),
            "autonomia": self.rendimiento.autonomia if self.rendimiento else None,
            "precio": self.info.precio,
        }

    def _calcular_versatilidad(self):
        score = 0
        if self.atributos_especificos.suspension_largo_recorrido:
            score += min(self.atributos_especificos.suspension_largo_recorrido / 2, 50)
        if self.atributos_especificos.proteccion_motor == "Sí":
            score += 25
        if self.atributos_especificos.tanque_grande == "Sí":
            score += 25
        return score


class MotoMotocarro(Moto):
    def obtener_criterios_comparacion(self):
        return {
            "categoria": "utilitario",
            "capacidad_pasajeros": self.atributos_especificos.capacidad_pasajeros,
            "capacidad_carga": self.atributos_especificos.capacidad_carga,
            "consumo": self.rendimiento.consumo if self.rendimiento else None,
            "precio": self.info.precio,
        }

    def obtener_tags_busqueda(self):
        tags = ["motocarro", "utilitario", "trabajo"]
        if (
            self.atributos_especificos.capacidad_carga
            and self.atributos_especificos.capacidad_carga > 300
        ):
            tags.append("carga_pesada")
        if (
            self.atributos_especificos.capacidad_pasajeros
            and self.atributos_especificos.capacidad_pasajeros >= 3
        ):
            tags.append("transporte_pasajeros")
        return tags

    def obtener_metricas_score(self):
        return {
            "tipo": "motocarro",
            "utilidad_score": self._calcular_utilidad(),
            "precio": self.info.precio,
        }

    def _calcular_utilidad(self):
        score = 0
        if self.atributos_especificos.capacidad_carga:
            score += min(self.atributos_especificos.capacidad_carga / 5, 50)
        if self.atributos_especificos.capacidad_pasajeros:
            score += self.atributos_especificos.capacidad_pasajeros * 10
        return score


class MotoNaked(Moto):
    def obtener_criterios_comparacion(self):
        return {
            "categoria": "naked",
            "cilindraje": self.motor.cilindraje,
            "potencia": self.motor.potencia,
            "peso": self.dimensiones.peso,
            "altura_asiento": self.dimensiones.altura_asiento,
            "precio": self.info.precio,
        }

    def obtener_tags_busqueda(self):
        tags = ["naked", "roadster", "urbana"]
        if self.motor.cilindraje and self.motor.cilindraje <= 500:
            tags.append("media_cilindrada")
        if self.motor.cilindraje and self.motor.cilindraje > 700:
            tags.append("naked_deportiva")
        if self.dimensiones.altura_asiento and self.dimensiones.altura_asiento < 800:
            tags.append("accesible")
        return tags

    def obtener_metricas_score(self):
        return {
            "tipo": "naked",
            "versatilidad_urbana": self._calcular_versatilidad_urbana(),
            "cilindraje": self.motor.cilindraje,
            "precio": self.info.precio,
        }


class MotoStreet(Moto):
    def obtener_criterios_comparacion(self):
        return {
            "categoria": "street",
            "cilindraje": self.motor.cilindraje,
            "consumo": self.rendimiento.consumo if self.rendimiento else None,
            "peso": self.dimensiones.peso,
            "precio": self.info.precio,
        }

    def obtener_tags_busqueda(self):
        tags = ["street", "urbana", "economica"]
        if self.motor.cilindraje and self.motor.cilindraje <= 200:
            tags.extend(["principiante", "ciudad"])
        if (
            self.rendimiento
            and self.rendimiento.consumo
            and self.rendimiento.consumo > 40
        ):
            tags.append("muy_economica")
        return tags

    def obtener_metricas_score(self):
        return {
            "tipo": "street",
            "economia_score": self._calcular_economia(),
            "precio": self.info.precio,
        }

    def _calcular_economia(self):
        score = 0
        if self.rendimiento and self.rendimiento.consumo:
            score += min(self.rendimiento.consumo, 50)
        if self.info.precio and self.info.precio < 10000000:
            score += 50
        return score


def crear_moto(db, moto_id):
    data = db.get_moto(moto_id)
    if not data:
        return None

    tipos = {
        "naked": MotoNaked,
        "sport": MotoSport,
        "touring": MotoTouring,
        "adventure": MotoTouring,
        "scooter": MotoScooter,
        "street": MotoStreet,
        "doble pps": MotoDoblePps,
        "electric": MotoElectric,
        "motocarro": MotoMotocarro,
    }

    clase = tipos.get(data["tipo"].lower(), Moto)
    return clase(moto_id, data)
