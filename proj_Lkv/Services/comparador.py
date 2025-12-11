import os
from Core.moto import crear_moto
from Services.k_score import clasificar_krono

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

class Comparador:
    def __init__(self, db, krono):
        self.db = db
        self.krono = krono

    def ejecutar(self):
        limpiar()
        print("\n" + "="*70)
        print("        COMPARADOR DE MOTOS")
        print("="*70 + "\n")

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
                precio_valor = m.get('precio')
                precio_texto = f"${precio_valor:,.0f}" if precio_valor else "N/A"
                print(f"{i:<3} {m['marca']:<12} {m['modelo']:<20} {m['tipo']:<12} {precio_texto:>15}")

            try:
                entrada = input(f"\nElige moto {len(seleccionadas)+1} (0 para terminar): ").strip()
                if entrada == "0":
                    break
                idx = int(entrada) - 1
                if 0 <= idx < len(motos_raw):
                    moto_id = motos_raw[idx]['id']
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
        print("\n" + "="*100)
        print("                   COMPARACIÓN DE MOTOS")
        print("="*100 + "\n")

        # Calcular precio promedio solo con las que tienen precio
        precios_validos = [m.info.precio for m in motos if m.info.precio]
        precio_prom = sum(precios_validos) / len(precios_validos) if precios_validos else 10000000

        resultados = self.krono.comparar_motos(motos, precio_prom)

        print(f"{'Pos':<4} {'Moto':<40} {'Calidad':<10} {'Precio':<10} {'Clasificación'}")
        print("-" * 100)
        for i, res in enumerate(resultados, 1):
            m = res['moto']
            s = res['scores']
            nombre = f"{m.info.marca} {m.info.modelo} ({m.info.año})"
            clasif = clasificar_krono(s['krono_precio'])  # Asegúrate de tener esta función
            print(f"{i:<4} {nombre:<40} {s['krono_calidad']:<10.1f} {s['krono_precio']:<10.1f} {clasif}")

        input("\nPresiona ENTER para volver al menú...")