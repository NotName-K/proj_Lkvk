class KronoScore:

    def __init__(self, db_scores):
        self.db = db_scores

    def _score_rendimiento(self, m):
        return (
            self.db.get_score("hp", m.get("hp_rango")) +
            self.db.get_score("hp_rpm", m.get("hp_rpm_rango")) +
            self.db.get_score("torque", m.get("torque_rango")) +
            self.db.get_score("torque_rpm", m.get("torque_rpm_rango")) +
            self.db.get_score("cilindrada", m.get("cilindraje_rango")) +
            self.db.get_score("top_speed", m.get("top_speed_rango")) +
            self.db.get_score("freno_del", m.get("freno_del")) +
            self.db.get_score("freno_tras", m.get("freno_tras")) +
            self.db.get_score("abs", m.get("abs")) +
            self.db.get_score("transmision", m.get("transmision")) +
            self.db.get_score("caja", m.get("tipo_caja"))
        )

    def _score_consumo(self, m):
        return (
            self.db.get_score("consumo", m.get("consumo_rango")) +
            self.db.get_score("tanque", m.get("tanque_rango"))
        )

    def _score_viajes(self, m):
        return (
            self.db.get_score("susp_del", m.get("susp_del")) +
            self.db.get_score("susp_tras", m.get("susp_tras")) +
            self.db.get_score("asiento", m.get("altura_asiento_rango")) +
            self.db.get_score("parabrisas", m.get("parabrisas")) +
            self.db.get_score("peso", m.get("peso_rango")) +
            self.db.get_score("vel_crucero", m.get("vel_crucero_rango")) +
            self.db.get_score("modos", m.get("modos_rango"))
        )

    def _score_diseno(self, m):
        return (
            self.db.get_score("faro", m.get("iluminacion")) +
            self.db.get_score("pantalla", m.get("pantalla")) +
            self.db.get_score("neumaticos", m.get("neumaticos"))
        )

    def _score_confiabilidad(self, m):
        marca = m.get("marca", "").lower()
        puntaje_marca = self.db.get_marca_score(marca)
        fallos = m.get("fallos_lista", [])
        penalizacion_total = sum(abs(self.db.get_penalizacion(f)) for f in fallos)
        return max(0, puntaje_marca - penalizacion_total)

    def _norm(self, valor, maximo):
        if valor <= 0:
            return 0
        if valor >= maximo:
            return 100
        return (valor / maximo) * 100

    def _ajuste_precio(self, calidad, precio, promedio):
        ratio = precio / promedio
        return max(0, min(100, calidad / ratio))

    def calcular(self, moto, precio_promedio_categoria=10000000):
        m = moto.obtener_metricas_score()

        rend = self._score_rendimiento(m)
        cons = self._score_consumo(m)
        viaje = self._score_viajes(m)
        disen = self._score_diseno(m)
        confi = self._score_confiabilidad(m)

        n_rend = self._norm(rend, 120)
        n_cons = self._norm(cons, 40)
        n_viaje = self._norm(viaje, 60)
        n_disen = self._norm(disen, 30)
        n_confi = self._norm(confi, 60)

        krono_calidad = (
            n_rend * 0.35 +
            n_cons * 0.15 +
            n_viaje * 0.20 +
            n_disen * 0.10 +
            n_confi * 0.20
        )

        krono_precio = self._ajuste_precio(
            krono_calidad,
            m.get("precio"),
            precio_promedio_categoria
        )

        return {
            "rendimiento": n_rend,
            "consumoYAutonomia": n_cons,
            "viajesYComodidad": n_viaje,
            "disenoYMateriales": n_disen,
            "confiabilidad": n_confi,
            "krono_calidad": krono_calidad,
            "krono_precio": krono_precio
        }
