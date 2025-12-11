from datetime import date
from Core.moto import crear_moto
from data import db
import sqlite3
from pathlib import Path
from datetime import date
import sqlite3
from data.db import DB, init_db
from data.db_scores import DBScores


class KronoScore:
    def __init__(self, db_scores):
        self.db_scores = db_scores
        self.db_file = db_scores.db_file

    def calcular(self, moto, precio_promedio_categoria=10000000):
        m = self.db_scores.extraer_metricas_moto(moto)

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
            n_rend * 0.35
            + n_cons * 0.15
            + n_viaje * 0.20
            + n_disen * 0.10
            + n_confi * 0.20
        )

        krono_precio = self._ajuste_precio(
            krono_calidad, m.get("precio", 10000000), precio_promedio_categoria
        )

        return {
            "rendimiento": round(n_rend, 1),
            "consumoYAutonomia": round(n_cons, 1),
            "viajesYComodidad": round(n_viaje, 1),
            "disenoYMateriales": round(n_disen, 1),
            "confiabilidad": round(n_confi, 1),
            "krono_calidad": round(krono_calidad, 1),
            "krono_precio": round(krono_precio, 1),
        }

    def _score_rendimiento(self, m):
        score = 0
        score += self.db_scores.get_score("hp", m.get("hp_rango"))
        score += self.db_scores.get_score("hp_rpm", m.get("hp_rpm_rango"))
        score += self.db_scores.get_score("torque", m.get("torque_rango"))
        score += self.db_scores.get_score("torque_rpm", m.get("torque_rpm_rango"))
        score += self.db_scores.get_score("cilindrada", m.get("cilindraje_rango"))
        score += self.db_scores.get_score("top_speed", m.get("top_speed_rango"))
        score += self.db_scores.get_score("freno_del", m.get("freno_del"))
        score += self.db_scores.get_score("freno_tras", m.get("freno_tras"))
        score += self.db_scores.get_score("abs", m.get("abs"))
        score += self.db_scores.get_score("transmision", m.get("transmision"))
        score += self.db_scores.get_score("caja", m.get("tipo_caja"))
        return score

    def _score_consumo(self, m):
        score = 0
        score += self.db_scores.get_score("consumo", m.get("consumo_rango"))
        score += self.db_scores.get_score("tanque", m.get("tanque_rango"))
        return score

    def _score_viajes(self, m):
        score = 0
        score += self.db_scores.get_score("susp_del", m.get("susp_del"))
        score += self.db_scores.get_score("susp_tras", m.get("susp_tras"))
        score += self.db_scores.get_score("asiento", m.get("altura_asiento_rango"))
        score += self.db_scores.get_score("parabrisas", m.get("parabrisas"))
        score += self.db_scores.get_score("peso", m.get("peso_rango"))
        score += self.db_scores.get_score("vel_crucero", m.get("vel_crucero_rango"))
        score += self.db_scores.get_score("modos", m.get("modos_rango"))
        return score

    def _score_diseno(self, m):
        score = 0
        score += self.db_scores.get_score("faro", m.get("iluminacion"))
        score += self.db_scores.get_score("pantalla", m.get("pantalla"))
        score += self.db_scores.get_score("neumaticos", m.get("neumaticos"))
        return score

    def _score_confiabilidad(self, m):
        marca = m.get("marca", "").lower()
        puntaje_marca = self.db_scores.get_marca_score(marca)

        fallos = m.get("fallos_lista", [])
        penalizacion_total = sum(
            abs(self.db_scores.get_penalizacion(f)) for f in fallos
        )

        return max(0, puntaje_marca - penalizacion_total)

    def _norm(self, valor, maximo):
        if valor <= 0:
            return 0
        if valor >= maximo:
            return 100
        return (valor / maximo) * 100

    def _ajuste_precio(self, calidad, precio, promedio):
        if precio <= 0 or promedio <= 0:
            return calidad

        ratio = precio / promedio

        return max(0, min(100, calidad / ratio))

    def comparar_motos(self, motos, precio_promedio_categoria=10000000):
        resultados = []

        for moto in motos:
            scores = self.calcular(moto, precio_promedio_categoria)
            resultados.append({"moto": moto, "scores": scores})

        resultados.sort(key=lambda x: x["scores"]["krono_precio"], reverse=True)

        return resultados

    def analizar_categoria(self, motos_categoria, precio_promedio=None):
        if not motos_categoria:
            return None

        if precio_promedio is None:
            precios = [m.info.precio for m in motos_categoria if m.info.precio]
            precio_promedio = sum(precios) / len(precios) if precios else 10000000

        scores_list = []
        for moto in motos_categoria:
            scores = self.calcular(moto, precio_promedio)
            scores_list.append({"moto": moto, "scores": scores})

        avg_calidad = sum(s["scores"]["krono_calidad"] for s in scores_list) / len(
            scores_list
        )
        avg_precio_score = sum(s["scores"]["krono_precio"] for s in scores_list) / len(
            scores_list
        )

        mejor = max(scores_list, key=lambda x: x["scores"]["krono_precio"])
        peor = min(scores_list, key=lambda x: x["scores"]["krono_precio"])

        return {
            "total_motos": len(motos_categoria),
            "precio_promedio": precio_promedio,
            "krono_calidad_promedio": round(avg_calidad, 1),
            "krono_precio_promedio": round(avg_precio_score, 1),
            "mejor_moto": {
                "info": mejor["moto"].info.to_dict(),
                "scores": mejor["scores"],
            },
            "peor_moto": {
                "info": peor["moto"].info.to_dict(),
                "scores": peor["scores"],
            },
            "todas_motos": scores_list,
        }

    def recomendar_por_presupuesto(self, motos, presupuesto_max, top_n=5):
        en_presupuesto = [
            m for m in motos if m.info.precio and m.info.precio <= presupuesto_max
        ]

        if not en_presupuesto:
            return []

        precios = [m.info.precio for m in en_presupuesto]
        precio_prom = sum(precios) / len(precios)

        resultados = self.comparar_motos(en_presupuesto, precio_prom)

        return resultados[:top_n]

    def actualizar_promedios_mercado(self):
        """Actualiza los promedios de mercado por tipo de moto"""
        from collections import defaultdict
        from data.db import DB
        from Core.moto import crear_moto

        db = DB()

        try:
            motos = []
            for row in db.listar_motos():
                moto = crear_moto(db, row["id"])
                if moto and moto.info.precio and moto.info.precio > 0:
                    motos.append(moto)

            if not motos:
                print("No hay motos en la base de datos")
                return

            precio_promedio_general = sum(m.info.precio for m in motos) / len(motos)

            stats = defaultdict(list)

            for moto in motos:
                scores = self.calcular(
                    moto, precio_promedio_categoria=precio_promedio_general
                )
                tipo = moto.info.tipo.lower()
                stats[tipo].append(
                    {
                        "precio": moto.info.precio,
                        "calidad": scores["krono_calidad"],
                        "precio_score": scores["krono_precio"],
                    }
                )

            cur = db.conn.cursor()

            for tipo, lista in stats.items():
                if not lista:
                    continue

                avg_precio = sum(x["precio"] for x in lista) / len(lista)
                avg_calidad = sum(x["calidad"] for x in lista) / len(lista)
                avg_krono = sum(x["precio_score"] for x in lista) / len(lista)

                cur.execute(
                    """
                INSERT OR REPLACE INTO promedios_mercado 
                (tipo, precio_promedio, krono_calidad_promedio, krono_precio_promedio, cantidad_motos, ultima_actualizacion)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                    (
                        tipo,
                        avg_precio,
                        avg_calidad,
                        avg_krono,
                        len(lista),
                        date.today(),
                    ),
                )

            db.conn.commit()

        finally:
            db.cerrar()

    def vs_mercado(self, moto, scores):
        """Compara el Krono Precio con el promedio del segmento
        y ACTUALIZA los promedios automáticamente si hace falta
        """
        db = DB()
        db_scores = DBScores()
        krono = KronoScore(db_scores)
        krono.actualizar_promedios_mercado()
        db.cerrar()

        try:
            import sqlite3
            from pathlib import Path
            from datetime import date

            moto_db_path = Path(self.db_file).parent / "moto.db"
            conn = sqlite3.connect(moto_db_path)
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS promedios_mercado (
                    tipo TEXT PRIMARY KEY,
                    precio_promedio REAL,
                    krono_calidad_promedio REAL,
                    krono_precio_promedio REAL,
                    cantidad_motos INTEGER,
                    ultima_actualizacion DATE
                )
                """)

            tipo_moto = moto.info.tipo.lower()

            motos_del_tipo = []
            for row in conn.execute("SELECT id FROM moto WHERE tipo = ?", (tipo_moto,)):
                try:
                    m = crear_moto(conn, row[0])
                    if m and m.info.precio and m.info.precio > 0:
                        s = self.calcular(m, precio_promedio_categoria=m.info.precio)
                        motos_del_tipo.append(
                            {
                                "precio": m.info.precio,
                                "calidad": s["krono_calidad"],
                                "krono_precio": s["krono_precio"],
                            }
                        )
                except:
                    continue

            if motos_del_tipo:
                avg_precio = sum(m["precio"] for m in motos_del_tipo) / len(
                    motos_del_tipo
                )
                avg_calidad = sum(m["calidad"] for m in motos_del_tipo) / len(
                    motos_del_tipo
                )
                avg_krono = sum(m["krono_precio"] for m in motos_del_tipo) / len(
                    motos_del_tipo
                )

                cur.execute(
                    """
                    INSERT OR REPLACE INTO promedios_mercado
                    (tipo, precio_promedio, krono_calidad_promedio, krono_precio_promedio, cantidad_motos, ultima_actualizacion)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        tipo_moto,
                        avg_precio,
                        avg_calidad,
                        avg_krono,
                        len(motos_del_tipo),
                        date.today(),
                    ),
                )

            cur.execute(
                "SELECT krono_precio_promedio FROM promedios_mercado WHERE tipo = ?",
                (tipo_moto,),
            )
            row = cur.fetchone()
            conn.commit()
            conn.close()

            if not row or row[0] is None:
                return "Vs Mercado: Sin datos del segmento"

            diff = scores["krono_precio"] - row[0]
            if abs(diff) <= 5:
                return f"Vs Mercado: {diff:+.1f} pts vs promedio"
            elif diff > 0:
                return f"Vs Mercado: +{diff:.1f} pts sobre el promedio"
            else:
                return f"Vs Mercado: {diff:.1f} pts bajo el promedio"

        except Exception as e:
            return "Vs Mercado: Actualizando datos..."


def calcular_precio_promedio_categoria(db, tipo_moto):
    motos = db.listar_motos()
    motos_tipo = [m for m in motos if m["tipo"].lower() == tipo_moto.lower()]

    precios = []
    for moto_data in motos_tipo:
        moto = crear_moto(db, moto_data["id"])
        if moto and moto.info.precio:
            precios.append(moto.info.precio)

    if precios:
        return sum(precios) / len(precios)
    else:
        return 10000000


def clasificar_krono(score):
    if score >= 85:
        return "EXCEPCIONAL - Premium en su categoría"
    elif score >= 75:
        return " EXCELENTE - Muy recomendada"
    elif score >= 65:
        return " BUENA - Relación calidad-precio equilibrada"
    elif score >= 50:
        return " ACEPTABLE - Cumple expectativas básicas"
    else:
        return " LIMITADA - Considerar otras opciones"
