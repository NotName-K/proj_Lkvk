from data.db import DB
from data.scores_db_init import init_scores_db
from data.db import init_db

def admin_mode():
    init_db()
    init_scores_db()
    db = DB()

    while True:
        print("\n" + "="*50)
        print("🔧 ADMIN MODE")
        print("="*50)
        print("1. Agregar moto")
        print("2. Editar campo de moto")
        print("3. Eliminar moto")
        print("4. Listar motos")
        print("0. Volver al menú principal")

        op = input("\nSelecciona una opción: ").strip()

        if op == "1":
            db.agregar_moto()

        elif op == "2":
            moto_id = input("ID de la moto a editar: ").strip()
            campo = input("Campo a editar: ").strip()
            valor = input("Nuevo valor: ").strip()
            db.actualizar_campo_moto(moto_id, campo, valor)
            print("✔ Campo actualizado.")

        elif op == "3":
            moto_id = input("ID de la moto a eliminar: ").strip()
            db.eliminar_moto(moto_id)
            print("🗑 Moto eliminada.")

        elif op == "4":
            motos = db.listar_motos()
            for m in motos:
                print(f"- {m['id']} | {m['marca']} {m['modelo']} ({m['tipo']})")

        elif op == "0":
            print("🔙 Volviendo al menú principal...")
            db.cerrar()
            return

        else:
            print("❌ Opción inválida")

