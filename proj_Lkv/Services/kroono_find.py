import os
from Core.moto import crear_moto
from Core.kroono_score import clasificar_krono


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


class KronoFind:
    def __init__(self, db, krono):
        self.db = db
        self.krono = krono

    def ejecutar(self):
        while True:
            limpiar()
            print("\n" + "=" * 70)
            print("         KRONOFIND - Encuentra tu moto ideal")
            print("=" * 70)
            print("Filtros disponibles:")
            print("1. Por presupuesto máximo")
            print("2. Por tipo de moto")
            print("3. Por cilindraje")
            print("4. Por uso recomendado")
            print("5. Por KronoScore")
            print("0. Volver al menú")

            op = input("\nElige una opción: ").strip()

            if op == "0":
                break
            elif op == "1":
                self.filtrar_por_presupuesto()
            elif op == "2":
                self.filtrar_por_tipo()
            elif op == "3":
                self.filtrar_por_cilindraje()
            elif op == "4":
                self.filtrar_por_uso()
            elif op == "5":
                self.mostrar_top_general()
            else:
                print("Opción no válida")
                input("ENTER...")

    def _calcular_y_ordenar(self, motos_lista):
        """Función auxiliar: calcula KronoScore y ordena"""
        if not motos_lista:
            return []

        # Precio promedio de las motos que sí tienen precio
        precios = [
            m.info.precio for m in motos_lista if m.info.precio and m.info.precio > 0
        ]
        precio_prom = sum(precios) / len(precios) if precios else 15000000

        resultados = self.krono.comparar_motos(motos_lista, precio_prom)
        # Ordenamos por KronoPrecio (mejor primero)
        resultados.sort(key=lambda x: x["scores"]["krono_precio"], reverse=True)
        return resultados

    def mostrar_resultados(self, resultados, titulo):
        limpiar()
        print(f"\n{titulo}")
        print("=" * 90)

        if not resultados:
            print("   No se encontraron motos con esos filtros")
        else:
            print(
                f"{'Pos':<4} {'Moto':<40} {'Precio':>14} {'KronoPrecio':>12}  Clasificación"
            )
            print("-" * 90)
            for i, res in enumerate(resultados[:10], 1):  # solo las 10 mejores
                m = res["moto"]
                s = res["scores"]
                precio_texto = (
                    f"${m.info.precio:,.0f}"
                    if m.info.precio and m.info.precio > 0
                    else "Consultar"
                )
                clasif = clasificar_krono(s["krono_precio"])
                nombre = f"{m.info.marca} {m.info.modelo} ({m.info.año})"
                print(
                    f"{i:<4} {nombre:<40} {precio_texto:>14} {s['krono_precio']:>10.1f}    {clasif}"
                )

        input("Presiona ENTER para continuar")

    def filtrar_por_presupuesto(self):
        try:
            presupuesto = int(
                input("\nPresupuesto máximo (solo números): ").replace(".", "")
            )
        except:
            print("Valor inválido")
            input()
            return

        motos = []
        for row in self.db.listar_motos():
            if row["precio"] and row["precio"] <= presupuesto and row["precio"] > 0:
                moto = crear_moto(self.db, row["id"])
                if moto:
                    motos.append(moto)

        resultados = self._calcular_y_ordenar(motos)
        self.mostrar_resultados(resultados, f"MEJORES MOTOS HASTA ${presupuesto:,}")

    def filtrar_por_tipo(self):
        tipos = [
            "naked",
            "sport",
            "touring",
            "adventure",
            "scooter",
            "street",
            "doble pps",
            "electric",
            "motocarro",
        ]
        print("\nTipos de moto:")
        for i, t in enumerate(tipos, 1):
            print(f"{i}. {t.title()}")
        try:
            idx = int(input("\nNúmero: ")) - 1
            tipo_elegido = tipos[idx]
        except:
            print("Inválido")
            input()
            return

        motos = []
        for row in self.db.listar_motos():
            if row["tipo"].lower() == tipo_elegido:
                moto = crear_moto(self.db, row["id"])
                if moto:
                    motos.append(moto)

        resultados = self._calcular_y_ordenar(motos)
        self.mostrar_resultados(
            resultados, f"MEJORES MOTOS TIPO: {tipo_elegido.upper()}"
        )

    def filtrar_por_cilindraje(self):
        print("Rangos de cilindraje:")
        print("1. Hasta 200 cc")
        print("2. 201 – 500 cc")
        print("3. 501 – 800 cc")
        print("4. Más de 800 cc")
        try:
            op = input("\nElige: ")
            limites = {
                "1": (0, 200),
                "2": (201, 500),
                "3": (501, 800),
                "4": (801, 9999),
            }[op]
        except:
            print("Opción inválida")
            input()
            return

        motos = []
        for row in self.db.listar_motos():
            moto = crear_moto(self.db, row["id"])
            if moto and moto.motor.cilindraje:
                if limites[0] <= moto.motor.cilindraje <= limites[1]:
                    motos.append(moto)

        resultados = self._calcular_y_ordenar(motos)
        self.mostrar_resultados(
            resultados, f"MEJORES MOTOS {limites[0]}–{limites[1]} cc"
        )

    def filtrar_por_uso(self):
        print("\nUso recomendado:")
        print("1. Ciudad / diario")
        print("2. Viajes largos")
        print("3. Off-road / aventura")
        print("4. Trabajo / carga")
        try:
            op = input("\nElige: ")
            usos = {
                "1": ["street", "scooter", "naked"],
                "2": ["touring", "adventure"],
                "3": ["doble pps", "adventure"],
                "4": ["motocarro"],
            }[op]
        except:
            print("Opción inválida")
            input()
            return

        motos = []
        for row in self.db.listar_motos():
            if row["tipo"] in usos:
                moto = crear_moto(self.db, row["id"])
                if moto:
                    motos.append(moto)

        resultados = self._calcular_y_ordenar(motos)
        titulo = {"1": "CIUDAD", "2": "VIAJES LARGOS", "3": "OFF-ROAD", "4": "TRABAJO"}[
            op
        ]
        self.mostrar_resultados(resultados, f"MEJORES MOTOS PARA {titulo}")

    def mostrar_top_general(self):
        motos = []
        for row in self.db.listar_motos():
            moto = crear_moto(self.db, row["id"])
            if moto:
                motos.append(moto)

        resultados = self._calcular_y_ordenar(motos)
        self.mostrar_resultados(
            resultados, "TOP 10 GENERAL – MEJORES MOTOS SEGÚN KRONOSCORE"
        )
