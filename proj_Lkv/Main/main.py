import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.db import DB, init_db
from data.db_scores import DBScores
from Services.k_score import KronoScore, clasificar_krono
from Services.review import ReviewModule
from Services.admin import admin_mode
from Services.review import ReviewModule

def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPresiona ENTER para continuar...")

def main():
    limpiar()
    print("Iniciando KronoScorer...\n")
    
    init_db()
    db = DB()
    db_scores = DBScores()
    krono = KronoScore(db_scores)

    while True:
        limpiar()
        print("="*60)
        print("     KRONOSCORER - Motocicletas")
        print("="*60)
        print("\n1. Review de una moto")
        print("2. Comparar motos")
        print("3. KronoFind")
        print("4. ADMIN Mode")
        print("\n0. Salir")
        print("-"*60)
        
        op = input("\nElige: ").strip()

        if op == "1":
            ReviewModule(db, db_scores, krono).ejecutar()
        elif op == "2":
            from Services.comparador import Comparador
            Comparador(db, krono).ejecutar()
        elif op == "3":
            from Services.buscador import KronoFind
            KronoFind(db, krono).ejecutar()
        elif op == "4":
            admin_mode()
        elif op == "0":
            print("\n¡Chao!")
            break
        else:
            print("\nAún no está listo")
            pausar()

    db.cerrar()

if __name__ == "__main__":
    main()
