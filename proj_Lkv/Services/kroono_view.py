import os
import sys
import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.db import DB
from Core.moto import crear_moto
from data.db_scores import DBScores
from Core.kroono_score import KronoScore, clasificar_krono


class ReviewModule:
    def __init__(self, db, db_scores, krono):
        self.db = db
        self.db_scores = db_scores
        self.krono = krono

        self.precios_promedio = {
            "naked": 12000000,
            "sport": 18000000,
            "touring": 35000000,
            "adventure": 40000000,
            "scooter": 8000000,
            "street": 6000000,
            "doble proposito": 15000000,
            "electric": 25000000,
            "motocarro": 10000000,
        }

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola"""
        os.system("cls" if os.name == "nt" else "clear")

    def pausar(self):
        """Pausa y espera que el usuario presione Enter"""
        input("\n Presiona ENTER para continuar...")

    def ejecutar(self):
        """Punto de entrada principal del módulo Review"""
        self.limpiar_pantalla()
        print("\n" + "=" * 70)
        print(" REVIEW - CONSULTA DE MOTOCICLETAS".center(70))
        print("=" * 70 + "\n")

        marca = self.seleccionar_marca()
        if not marca:
            return

        moto = self.seleccionar_modelo(marca)
        if not moto:
            return

        self.mostrar_review_completo(moto)

    def seleccionar_marca(self):
        marcas_validas = self.db_scores.get_valores_validos("marca")
        marcas = sorted([m[0] for m in marcas_validas])

        print(" MARCAS DISPONIBLES:")
        print("-" * 70)

        for i in range(0, len(marcas), 3):
            fila = marcas[i : i + 3]
            print("  ".join(f"{m:<20}" for m in fila))

        print("-" * 70)
        marca = input("\n Ingresa la marca (o '0' para cancelar): ").strip().lower()

        if marca == "0":
            return None

        if marca not in marcas:
            print(f" Marca '{marca}' no válida")
            self.pausar()
            return None

        return marca

    def seleccionar_modelo(self, marca):
        modelos_marca = self.db.obtener_modelos_por_marca(marca)

        if not modelos_marca:
            print(f" No hay modelos disponibles para la marca '{marca}'")
            self.pausar()
            return None

        items_por_pagina = 10
        total_paginas = (len(modelos_marca) + items_por_pagina - 1) // items_por_pagina
        pagina_actual = 0

        while True:
            self.limpiar_pantalla()
            print(f"\n MODELOS DE {marca.upper()}")
            print("-" * 70)

            inicio = pagina_actual * items_por_pagina
            fin = min(inicio + items_por_pagina, len(modelos_marca))

            for i, modelo in enumerate(modelos_marca[inicio:fin], inicio + 1):
                print(
                    f"{i:2d}. {modelo['modelo']:<30} {modelo['tipo']:<15} ({modelo['año']})"
                )

            print("-" * 70)
            print(f"Página {pagina_actual + 1}/{total_paginas}")
            print("\n[N] Siguiente página  [A] Página anterior  [0] Cancelar")

            opcion = (
                input("\n Selecciona el índice del modelo o navega: ").strip().lower()
            )

            if opcion == "0":
                return None
            elif opcion == "n" and pagina_actual < total_paginas - 1:
                pagina_actual += 1
            elif opcion == "a" and pagina_actual > 0:
                pagina_actual -= 1
            elif opcion.isdigit():
                idx = int(opcion) - 1
                if 0 <= idx < len(modelos_marca):
                    moto_id = modelos_marca[idx]["id"]
                    return crear_moto(self.db, moto_id)
                else:
                    print(" Índice inválido")
                    self.pausar()
            else:
                print(" Opción inválida")
                self.pausar()

    def mostrar_review_completo(self, moto):
        """
        Muestra el review completo de una moto con opciones

        Args:
            moto: Instancia de Moto
        """
        while True:
            self.limpiar_pantalla()

            precio_prom = self.precios_promedio.get(moto.info.tipo.lower(), 10000000)
            scores = self.krono.calcular(moto, precio_promedio_categoria=precio_prom)

            print("\n" + "=" * 70)
            print(f"  {moto.info.marca.upper()} {moto.info.modelo.upper()}".center(70))
            print("=" * 70 + "\n")

            print(f" Tipo:           {moto.info.tipo.upper()}")
            print(f" Año:            {moto.info.año}")
            print(
                f" Precio:         ${moto.info.precio:,.0f}"
                if moto.info.precio
                else " Precio:         N/A"
            )
            vs = self.krono.vs_mercado(moto, scores)
            if vs:
                print(f" {vs}")
            print(f" Colores:        {moto.info.color or 'N/A'}")

            print("\n" + "-" * 70)
            print(" INFORMACIÓN DESTACADA")
            print("-" * 70)
            self.mostrar_info_especifica(moto)

            print("\n" + "=" * 70)
            print(" PUNTUACIONES KRONO")
            print("=" * 70)
            print(
                f"\n Krono Calidad:        {scores['krono_calidad']:.1f}/100  {self.barra_visual(scores['krono_calidad'])}"
            )
            print(
                f" Krono Precio:         {scores['krono_precio']:.1f}/100  {self.barra_visual(scores['krono_precio'])}"
            )
            print(f"\n Clasificación: {clasificar_krono(scores['krono_precio'])}")

            print("\n" + "=" * 70)
            print(" OPCIONES")
            print("-" * 70)
            print("1.  Más detalles (Ficha completa)")
            print("2.  KronoScore Review (Desglose + Gráfico)")
            print("0.  Volver")
            print("-" * 70)

            opcion = input("\n Selecciona una opción: ").strip()

            if opcion == "1":
                self.mostrar_detalles_completos(moto)
            elif opcion == "2":
                self.kronoscore_review(moto, scores)
            elif opcion == "0":
                break
            else:
                print(" Opción inválida")
                self.pausar()

    def mostrar_info_especifica(self, moto):
        """
        Muestra información específica según el tipo de moto

        Args:
            moto: Instancia de Moto
        """
        tipo = moto.info.tipo.lower()

        if hasattr(moto, "motor") and hasattr(moto.motor, "cilindraje"):
            if moto.motor.cilindraje:
                print(f" Cilindraje:     {moto.motor.cilindraje} cc")
            if moto.motor.potencia:
                print(f" Potencia:       {moto.motor.potencia}")
            if moto.motor.torque:
                print(f" Torque:         {moto.motor.torque}")

        if (
            tipo == "sport"
            and hasattr(moto, "atributos_especificos")
            and moto.atributos_especificos
        ):
            if moto.atributos_especificos.aceleracion_0_100:
                print(
                    f" 0-100 km/h:     {moto.atributos_especificos.aceleracion_0_100} s"
                )
            if moto.atributos_especificos.modos_manejo:
                print(f" Modos:          {moto.atributos_especificos.modos_manejo}")

        elif (
            tipo == "naked"
            and hasattr(moto, "atributos_especificos")
            and moto.atributos_especificos
        ):
            if moto.atributos_especificos.aceleracion_0_100:
                print(
                    f" 0-100 km/h:     {moto.atributos_especificos.aceleracion_0_100} s"
                )

        elif (
            tipo in ["touring", "adventure"]
            and hasattr(moto, "atributos_especificos")
            and moto.atributos_especificos
        ):
            if moto.rendimiento and moto.rendimiento.autonomia:
                print(f" Autonomía:      {moto.rendimiento.autonomia:.0f} km")
            if moto.atributos_especificos.capacidad_maletas:
                print(
                    f" Maletas:        {moto.atributos_especificos.capacidad_maletas} L"
                )
            if moto.atributos_especificos.control_crucero:
                print(f" Control crucero: {moto.atributos_especificos.control_crucero}")
            if tipo == "adventure":
                if (
                    hasattr(moto.atributos_especificos, "maletas_laterales")
                    and moto.atributos_especificos.maletas_laterales
                ):
                    print(
                        f" Maletas lat.:   {moto.atributos_especificos.maletas_laterales}"
                    )
                if (
                    hasattr(moto.atributos_especificos, "suspension_ajustable")
                    and moto.atributos_especificos.suspension_ajustable
                ):
                    print(
                        f" Susp. ajust.:   {moto.atributos_especificos.suspension_ajustable}"
                    )

        elif (
            tipo == "scooter"
            and hasattr(moto, "atributos_especificos")
            and moto.atributos_especificos
        ):
            if moto.atributos_especificos.espacio_baul:
                print(f" Baúl:           {moto.atributos_especificos.espacio_baul} L")
            if moto.rendimiento and moto.rendimiento.consumo:
                print(f" Consumo:        {moto.rendimiento.consumo} km/l")

        elif tipo == "electric":
            if (
                hasattr(moto.motor, "bateria_capacidad")
                and moto.motor.bateria_capacidad
            ):
                print(f" Batería:        {moto.motor.bateria_capacidad} kWh")
            if (
                hasattr(moto.motor, "autonomia_electrica")
                and moto.motor.autonomia_electrica
            ):
                print(f" Autonomía:      {moto.motor.autonomia_electrica} km")
            if hasattr(moto.motor, "tiempo_carga") and moto.motor.tiempo_carga:
                print(f" Tiempo carga:   {moto.motor.tiempo_carga} h")

        elif (
            tipo in ["doble proposito", "doble pps"]
            and hasattr(moto, "atributos_especificos")
            and moto.atributos_especificos
        ):
            if moto.atributos_especificos.suspension_largo_recorrido:
                print(
                    f" Susp. recorr.:  {moto.atributos_especificos.suspension_largo_recorrido}"
                )
            if moto.atributos_especificos.proteccion_motor:
                print(
                    f" Protección:     {moto.atributos_especificos.proteccion_motor}"
                )

        elif (
            tipo == "motocarro"
            and hasattr(moto, "atributos_especificos")
            and moto.atributos_especificos
        ):
            if moto.atributos_especificos.capacidad_pasajeros:
                print(
                    f" Pasajeros:      {moto.atributos_especificos.capacidad_pasajeros}"
                )
            if moto.atributos_especificos.capacidad_carga:
                print(
                    f" Carga:          {moto.atributos_especificos.capacidad_carga} kg"
                )

        if moto.dimensiones.altura_asiento:
            print(f" Altura asiento: {moto.dimensiones.altura_asiento} mm")
        if moto.dimensiones.peso:
            print(f" Peso:           {moto.dimensiones.peso} kg")

    def mostrar_detalles_completos(self, moto):
        self.limpiar_pantalla()
        print("\n" + "=" * 70)
        print(" FICHA TÉCNICA COMPLETA".center(70))
        print("=" * 70 + "\n")

        ficha = moto.ficha_completa()
        for clave, valor in ficha.items():
            print(f"{clave:.<35} {valor}")

        self.pausar()

    def kronoscore_review(self, moto, scores):
        self.limpiar_pantalla()
        print("\n" + "=" * 70)
        print(" KRONOSCORE REVIEW - ANÁLISIS DETALLADO".center(70))
        print("=" * 70 + "\n")

        print(f"  {moto.info.marca.upper()} {moto.info.modelo.upper()}\n")

        categorias = [
            (" Rendimiento y Potencia", scores["rendimiento"]),
            (" Consumo y Autonomía", scores["consumoYAutonomia"]),
            (" Viajes y Comodidad", scores["viajesYComodidad"]),
            (" Diseño y Materiales", scores["disenoYMateriales"]),
            (" Confiabilidad", scores["confiabilidad"]),
        ]

        print("-" * 70)
        for categoria, score in categorias:
            print(f"{categoria:<30} {score:>5.1f}/100  {self.barra_visual(score)}")
        print("-" * 70)

        print(f"\n{' KRONO CALIDAD':<30} {scores['krono_calidad']:>5.1f}/100")
        print(f"{' KRONO PRECIO':<30} {scores['krono_precio']:>5.1f}/100")

        print("\n" + "=" * 70)
        respuesta = input("\n ¿Deseas ver el gráfico de radar? (s/n): ").strip().lower()

        if respuesta == "s":
            print("\n Generando gráfico...")
            self.generar_grafico_radar(moto, categorias, scores)

        self.pausar()

    def generar_grafico_radar(self, moto, categorias, scores):
        labels = [cat[0].split(" ", 1)[1] for cat in categorias]
        valores = [cat[1] for cat in categorias]

        num_vars = len(labels)

        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        valores += valores[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))

        ax.plot(angles, valores, "o-", linewidth=2, color="black")
        ax.fill(angles, valores, alpha=0.25, color="blue")

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, size=10)

        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(["20", "40", "60", "80", "100"], size=8)
        ax.grid(True, linestyle="--", alpha=0.7)

        titulo = (
            f"{moto.info.marca.upper()} {moto.info.modelo.upper()} - KronoScore Review"
        )
        plt.title(titulo, size=14, weight="bold", pad=20)

        texto_scores = f"Krono Calidad: {scores['krono_calidad']:.1f}/100  |  Krono Precio: {scores['krono_precio']:.1f}/100"
        plt.figtext(0.5, 0.02, texto_scores, ha="center", size=11, weight="bold")

        plt.tight_layout()
        plt.show()

    def barra_visual(self, valor):
        """
        Genera una barra visual de progreso

        Args:
            valor: Valor entre 0 y 100

        Returns:
            str: Barra visual
        """
        ancho = 20
        lleno = int((valor / 100) * ancho)
        vacio = ancho - lleno

        return f"[{'█' * lleno}{'░' * vacio}]"
