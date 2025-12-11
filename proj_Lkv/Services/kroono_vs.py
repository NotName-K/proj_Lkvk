import os
from Core.moto import crear_moto
from Core.kroono_score import clasificar_krono
import matplotlib.pyplot as plt
import numpy as np


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


class Comparador:
    def __init__(self, db, krono):
        self.db = db
        self.krono = krono

    def ejecutar(self):
        limpiar()
        print("\n" + "=" * 70)
        print("        COMPARADOR DE MOTOS")
        print("=" * 70 + "\n")

        motos_raw = self.db.listar_motos()
        if len(motos_raw) < 2:
            print("Necesitas al menos 2 motos en la base de datos.")
            input("\nPresiona ENTER...")
            return

        seleccionadas = []
        while len(seleccionadas) < 4:
            limpiar()
            print(f"\nMotos seleccionadas: {len(seleccionadas)}/4\n")
            print(f"{'#':<3} {'Marca':<12} {'Modelo':<20} {'Tipo':<12} {'Precio':>15}")
            print("-" * 70)
            for i, m in enumerate(motos_raw, 1):
                precio_valor = m.get("precio")
                precio_texto = (
                    f"${precio_valor:,.0f}"
                    if precio_valor and precio_valor > 0
                    else "Consultar"
                )
                print(
                    f"{i:<3} {m['marca']:<12} {m['modelo']:<20} {m['tipo']:<12} {precio_texto:>15}"
                )

            try:
                entrada = input(
                    f"\nElige moto {len(seleccionadas) + 1} (0 para terminar): "
                ).strip()
                if entrada == "0":
                    break
                idx = int(entrada) - 1
                if 0 <= idx < len(motos_raw):
                    moto_id = motos_raw[idx]["id"]
                    if moto_id not in [s.moto_id for s in seleccionadas]:
                        moto = crear_moto(self.db, moto_id)
                        if moto:
                            seleccionadas.append(moto)
                            print(f"\nAgregada: {moto.info.marca} {moto.info.modelo}")
                    else:
                        print("Ya la seleccionaste!")
                else:
                    print("Número inválido")
            except ValueError:
                print("Entrada inválida")
            input("\nENTER para continuar...")

            if len(seleccionadas) >= 2:
                break

        if len(seleccionadas) < 2:
            print("\nNecesitas al menos 2 motos para comparar.")
            input("ENTER...")
            return

        self.mostrar_comparacion(seleccionadas)

    def mostrar_comparacion(self, motos):
        limpiar()
        print("\n" + "=" * 100)
        print("                   COMPARACIÓN DE MOTOS")
        print("=" * 100 + "\n")

        precios_validos = [
            m.info.precio for m in motos if m.info.precio and m.info.precio > 0
        ]
        precio_prom = (
            sum(precios_validos) / len(precios_validos) if precios_validos else 15000000
        )

        resultados = self.krono.comparar_motos(motos, precio_prom)

        print(
            f"{'Pos':<4} {'Moto':<45} {'Calidad':<10} {'Precio':<10} {'Clasificación'}"
        )
        print("-" * 100)
        for i, res in enumerate(resultados, 1):
            m = res["moto"]
            s = res["scores"]
            nombre = f"{m.info.marca} {m.info.modelo} ({m.info.año})"
            clasif = clasificar_krono(s["krono_precio"])
            print(
                f"{i:<4} {nombre:<45} {s['krono_calidad']:<10.1f} {s['krono_precio']:<10.1f} {clasif}"
            )

        if len(motos) == 2:
            print("\n¿Quieres ver la comparación visual en gráfico radar?")
            if input("s/n: ").strip().lower() == "s":
                m1, m2 = motos[0], motos[1]
                s1, s2 = resultados[0]["scores"], resultados[1]["scores"]
                self.mostrar_radar_comparativo(m1, m2, s1, s2)

        input("\nPresiona ENTER para volver al menú...")

    def mostrar_radar_comparativo(self, moto1, moto2, scores1, scores2):
        limpiar()
        print("\n" + "=" * 90)
        print("               COMPARACIÓN VISUAL - GRÁFICO RADAR")
        print("=" * 90 + "\n")

        categorias = [
            "Rendimiento",
            "Consumo/Autonomía",
            "Viajes/Comodidad",
            "Diseño/Materiales",
            "Confiabilidad",
        ]

        valores1 = [
            scores1["rendimiento"],
            scores1["consumoYAutonomia"],
            scores1["viajesYComodidad"],
            scores1["disenoYMateriales"],
            scores1["confiabilidad"],
        ]

        valores2 = [
            scores2["rendimiento"],
            scores2["consumoYAutonomia"],
            scores2["viajesYComodidad"],
            scores2["disenoYMateriales"],
            scores2["confiabilidad"],
        ]

        N = len(categorias)

        # Cerrar el círculo
        valores1 += valores1[:1]
        valores2 += valores2[:1]
        categorias_cerradas = categorias + [categorias[0]]

        angulos = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        angulos += angulos[:1]

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

        # Moto 1 - Azul Yamaha
        ax.plot(
            angulos,
            valores1,
            "o-",
            linewidth=4,
            label=f"{moto1.info.marca} {moto1.info.modelo} ({moto1.info.año})",
            color="#1f77b4",
        )
        ax.fill(angulos, valores1, alpha=0.25, color="#1f77b4")

        # Moto 2 - Naranja KTM
        ax.plot(
            angulos,
            valores2,
            "o-",
            linewidth=4,
            label=f"{moto2.info.marca} {moto2.info.modelo} ({moto2.info.año})",
            color="#ff7f0e",
        )
        ax.fill(angulos, valores2, alpha=0.25, color="#ff7f0e")

        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontsize=12, fontweight="bold")
        ax.set_ylim(0, 100)
        ax.set_yticklabels([])
        ax.grid(True, linewidth=2, color="gray", alpha=0.7)
        ax.legend(
            loc="upper right",
            bbox_to_anchor=(1.3, 1.1),
            fontsize=12,
            frameon=True,
            fancybox=True,
            shadow=True,
        )

        plt.title(
            "KronoScore - Comparación Radar",
            size=20,
            weight="bold",
            color="#2c3e50",
            pad=40,
        )
        plt.tight_layout()
        plt.show()
