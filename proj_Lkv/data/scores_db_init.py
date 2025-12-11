

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "data" / "scores.db"

def init_scores_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Tabla de scores (sin cambios)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        apartado TEXT NOT NULL,
        valor TEXT NOT NULL,
        puntaje REAL NOT NULL,
        UNIQUE(apartado, valor)
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS marca_confiabilidad (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT NOT NULL UNIQUE,
        puntaje INTEGER NOT NULL
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fallos_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra TEXT NOT NULL UNIQUE,
        penalizacion INTEGER NOT NULL
    )
    """)
    
    # Tabla expandida de valores válidos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS valores_validos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campo TEXT NOT NULL,
        valor TEXT NOT NULL,
        categoria TEXT,
        ejemplo TEXT,
        UNIQUE(campo, valor)
    )
    """)
    
    # Tabla de rangos numéricos válidos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rangos_validos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campo TEXT NOT NULL UNIQUE,
        min_valor REAL,
        max_valor REAL,
        unidad TEXT,
        ejemplo TEXT
    )
    """)
    
    # ============ INSERTAR SCORES (sin cambios) ============
    hp_scores = [
        ("0-15", 2), ("15-30", 6), ("30-50", 10),
        ("50-75", 14), ("75-100", 17), ("100-150", 19), ("150+", 20)
    ]
    for valor, puntaje in hp_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("hp", valor, puntaje))
    
    hp_rpm_scores = [
        ("muy_bajo", 10), ("bajo", 9), ("medio_bajo", 8),
        ("medio", 7), ("medio_alto", 5), ("alto", 3)
    ]
    for valor, puntaje in hp_rpm_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("hp_rpm", valor, puntaje))
    
    torque_scores = [
        ("0-10", 3), ("10-20", 7), ("20-40", 11),
        ("40-70", 15), ("70-100", 18), ("100+", 20)
    ]
    for valor, puntaje in torque_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("torque", valor, puntaje))
    
    torque_rpm_scores = [
        ("muy_bajo", 10), ("bajo", 9), ("medio_bajo", 8),
        ("medio", 7), ("medio_alto", 5), ("alto", 3)
    ]
    for valor, puntaje in torque_rpm_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("torque_rpm", valor, puntaje))
    
    cilindrada_scores = [
        ("0-125", 3), ("125-250", 7), ("250-400", 10),
        ("400-600", 12), ("600-1000", 14), ("1000+", 15)
    ]
    for valor, puntaje in cilindrada_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("cilindrada", valor, puntaje))
    
    top_speed_scores = [
        ("0-100", 3), ("100-140", 7), ("140-180", 10),
        ("180-220", 13), ("220+", 15)
    ]
    for valor, puntaje in top_speed_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("top_speed", valor, puntaje))
    
    freno_del_scores = [("tambor", 2), ("disco_simple", 7), ("disco_doble", 10)]
    for valor, puntaje in freno_del_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("freno_del", valor, puntaje))
    
    freno_tras_scores = [("tambor", 2), ("disco_simple", 5)]
    for valor, puntaje in freno_tras_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("freno_tras", valor, puntaje))
    
    abs_scores = [("sin_abs", 0), ("abs_simple", 6), ("abs_dual", 10)]
    for valor, puntaje in abs_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("abs", valor, puntaje))
    
    transmision_scores = [("mecanica", 3), ("automatica", 5)]
    for valor, puntaje in transmision_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("transmision", valor, puntaje))
    
    config_embrague = [
        ("automatico", None, "CVT"),
        ("manual", None, "Con palanca"),
        ("baño de aceite", None, "Húmedo"),
        ("seco", None, "Competición"),
        ("centrifugo", None, "Motos semiautomáticas")
    ]

    for valor, cat, ejemplo in config_embrague:
        cur.execute(
            "INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
            ("embrague", valor, cat, ejemplo)
        )
        
    config_caja = [
        ("automatico", None, "CVT"),
        ("semiautomatico", None, "Honda Wave"),
        ("manual 4", None, "4 velocidades"),
        ("manual 5", None, "5 velocidades"),
        ("manual 6", None, "6 velocidades")
    ]

    for valor, cat, ejemplo in config_caja:
        cur.execute(
            "INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
            ("caja", valor, cat, ejemplo)
        )
    caja_scores = [("4_vel", 2), ("5_vel", 4), ("6_vel", 5)]
    for valor, puntaje in caja_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("caja", valor, puntaje))
    
    consumo_scores = [("bajo", 10), ("medio", 18), ("alto", 25)]
    for valor, puntaje in consumo_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("consumo", valor, puntaje))
    
    tanque_scores = [("pequeño", 5), ("mediano", 10), ("grande", 15)]
    for valor, puntaje in tanque_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("tanque", valor, puntaje))
    
    susp_del_scores = [
        ("horquilla_convencional", 4), ("telescopica", 7), ("invertida", 10)
    ]
    for valor, puntaje in susp_del_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("susp_del", valor, puntaje))
    
    susp_tras_scores = [
        ("doble_amortiguador", 4), ("monoamortiguador_basico", 7),
        ("monoamortiguador_ajustable", 10)
    ]
    for valor, puntaje in susp_tras_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("susp_tras", valor, puntaje))
    
    asiento_scores = [("bajo", 10), ("medio", 7), ("alto", 4)]
    for valor, puntaje in asiento_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("asiento", valor, puntaje))
    
    parabrisas_scores = [("ajustable", 5)]
    for valor, puntaje in parabrisas_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("parabrisas", valor, puntaje))
    
    peso_scores = [("ligero", 10), ("medio", 7), ("pesado", 4)]
    for valor, puntaje in peso_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("peso", valor, puntaje))
    
    vel_crucero_scores = [
        ("60-80", 4), ("80-100", 7), ("100-120", 9), ("120+", 10)
    ]
    for valor, puntaje in vel_crucero_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("vel_crucero", valor, puntaje))
    
    modos_scores = [("dos", 2), ("tres", 4), ("multiples", 5)]
    for valor, puntaje in modos_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("modos", valor, puntaje))
    
    faro_scores = [("halogena", 5), ("led", 10)]
    for valor, puntaje in faro_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("faro", valor, puntaje))
    
    pantalla_scores = [("analogica", 4), ("digital", 10)]
    for valor, puntaje in pantalla_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("pantalla", valor, puntaje))
    
    neumaticos_scores = [
        ("kaptor", 5.5), ("queen", 5.5), ("kontrol", 5.5),
        ("ceat", 6.0), ("cst", 6.5), ("chaoyang", 6.5),
        ("mrf", 6.8), ("irc", 7.0), ("kenda", 7.5),
        ("dunlop", 8.0), ("bridgestone", 8.5), ("metzeler", 9.0),
        ("continental", 9.3), ("michelin", 9.5), ("pirelli", 9.5)
    ]
    for valor, puntaje in neumaticos_scores:
        cur.execute("INSERT OR IGNORE INTO scores (apartado, valor, puntaje) VALUES (?, ?, ?)",
                   ("neumaticos", valor, puntaje))
    
    # ============ MARCAS CONFIABILIDAD ============
    marcas_confiabilidad = [
        ("yamaha", 58), ("akt", 38), ("bajaj", 42), ("suzuki", 56),
        ("honda", 60), ("tvs", 40), ("hero", 36), ("victory", 44),
        ("kymco", 43), ("ktm", 48), ("kawasaki", 55), ("royal enfield", 38),
        ("cfmoto", 45), ("bmw", 52), ("voge", 44), ("benelli", 42),
        ("harley-davidson", 46), ("ducati", 45), ("triumph", 47), ("sym", 41)
    ]
    for marca, puntaje in marcas_confiabilidad:
        cur.execute("INSERT OR IGNORE INTO marca_confiabilidad (marca, puntaje) VALUES (?, ?)",
                   (marca, puntaje))
    
    # ============ FALLOS PENALIZACIONES ============
    fallos_penalizaciones = [
        ("motor", -20), ("transmision", -18), ("cigüeñal", -20),
        ("pistones", -18), ("valvulas", -15), ("embrague", -12),
        ("cadena", -8), ("suspension", -10), ("frenos", -12),
        ("electrico", -10), ("bateria", -8), ("encendido", -10),
        ("vibración", -5), ("ruido", -4), ("arranque", -6),
        ("consumo excesivo", -5), ("fugas", -6), ("luces", -3),
        ("pintura", -3), ("asiento", -4), ("calentamiento", -8),
        ("oxidacion", -5)
    ]
    for palabra, penalizacion in fallos_penalizaciones:
        cur.execute("INSERT OR IGNORE INTO fallos_scores (palabra, penalizacion) VALUES (?, ?)",
                   (palabra, penalizacion))
    
    # ============ VALORES VÁLIDOS EXPANDIDOS ============
    
    # Tipos de moto
    tipos = [
        ("naked", None, "Yamaha MT-07, Honda CB650R"),
        ("sport", None, "Yamaha R3, Kawasaki Ninja 400"),
        ("touring", None, "Honda Gold Wing, BMW K1600"),
        ("adventure", None, "BMW GS, KTM Adventure"),
        ("scooter", None, "Yamaha NMAX, Honda PCX"),
        ("street", None, "Honda CB190R, Yamaha FZ"),
        ("doble proposito", None, "Yamaha XTZ, Honda XR"),
        ("electric", None, "Zero SR/F, Energica"),
        ("motocarro", None, "Akt Cargo, TVS King")
    ]
    for valor, cat, ejemplo in tipos:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("tipo", valor, cat, ejemplo))
    
    # Marcas
    marcas = ["yamaha", "akt", "bajaj", "suzuki", "honda", "tvs", "hero", 
              "victory", "kymco", "ktm", "kawasaki", "royal enfield", "cfmoto", 
              "bmw", "voge", "benelli", "harley-davidson", "ducati", "triumph", "sym"]
    for marca in marcas:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("marca", marca, None, None))
    
    # Tiempos de motor
    for tiempo in ["2T", "4T"]:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("tiempos", tiempo, None, "2T (2 tiempos) o 4T (4 tiempos)"))
    
    config_cilindros = [
        ("monocilindrico", None, "1 cilindro"),
        ("bicilindrico en linea", None, "2 en línea"),
        ("bicilindrico en v", None, "Motor en V"),
        ("tricilindrico", None, "3 cilindros"),
        ("4 en linea", None, "4 cilindros en línea"),
        ("6 en linea", None, "6 cilindros en línea")
    ]
    
    for valor, cat, ejemplo in config_cilindros:
        cur.execute(
            "INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
            ("cilindros", valor, cat, ejemplo)
        )
    
    config_arbol_levas = [
        ("sohc", None, "Árbol de levas simple"),
        ("dohc", None, "Doble árbol de levas")
    ]

    for valor, cat, ejemplo in config_arbol_levas:
        cur.execute(
            "INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
            ("arbol_levas", valor, cat, ejemplo)
        )

    
    # Refrigeración
    for refrig in ["aire", "aire-aceite", "liquido"]:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("refrigeracion", refrig, None, None))
    
    # Arranque
    for arr in ["electrico", "pedal", "ambos"]:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("arranque", arr, None, None))
    
    # Inyección
    for iny in ["FI", "carburador"]:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("inyeccion", iny, None, "FI (Fuel Injection)"))
    
    # Transmisión
    for trans in ["mecanica", "automatica"]:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("transmision", trans, None, None))
    
    # Faros
    for faro in ["LED", "halogena"]:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("faros", faro, None, None))
    
    # ABS
    for abs_val in ["mono", "doble", "sin"]:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("abs_sistema", abs_val, None, "mono/doble/sin"))
    
    # Frenos
    for freno in ["disco", "disco doble", "tambor"]:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("freno", freno, "frenos", None))
    
    # Suspensión delantera
    susp_d = [
        ("horquilla convencional", "Horquilla básica"),
        ("telescopica", "Horquilla telescópica estándar"),
        ("invertida", "Horquilla invertida (upside down)")
    ]
    for susp, ejemplo in susp_d:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("suspension_d", susp, None, ejemplo))
    
    # Suspensión trasera
    susp_t = [
        ("doble amortiguador", "Dos amortiguadores"),
        ("monoamortiguador", "Monoamortiguador estándar"),
        ("monoamortiguador ajustable", "Monoamortiguador con ajustes")
    ]
    for susp, ejemplo in susp_t:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("suspension_t", susp, None, ejemplo))
    
    # Neumáticos
    neumaticos = ["kaptor", "queen", "kontrol", "ceat", "cst", "chaoyang", 
                  "mrf", "irc", "kenda", "dunlop", "bridgestone", "metzeler", 
                  "continental", "michelin", "pirelli"]
    for neu in neumaticos:
        cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                   ("neumaticos", neu, None, None))
    
    # Respuestas Sí/No
    for respuesta in ["si", "no"]:
        for campo in ["parabrisas_ajustable", "control_crucero", "sliper_clutch", 
                     "suspension_largo_recorrido", "proteccion_motor", "tanque_grande",
                     "maletas_laterales", "suspension_ajustable"]:
            cur.execute("INSERT OR IGNORE INTO valores_validos (campo, valor, categoria, ejemplo) VALUES (?, ?, ?, ?)",
                       (campo, respuesta, "booleano", None))
    
    # ============ RANGOS NUMÉRICOS VÁLIDOS ============
    rangos = [
        ("cilindraje", 49, 2500, "cc", "125, 250, 650"),
        ("año", 1990, 2030, "año", "2020, 2023"),
        ("consumo", 10, 50, "km/l", "30, 45"),
        ("capacidad_tanque", 3, 30, "L", "12, 15"),
        ("vel_crucero", 40, 200, "km/h", "90, 120"),
        ("top_speed", 50, 350, "km/h", "140, 180"),
        ("largo", 1500, 2800, "mm", "2000, 2100"),
        ("ancho", 600, 1000, "mm", "750, 800"),
        ("altura", 800, 1500, "mm", "1100, 1200"),
        ("distancia_ejes", 1200, 1800, "mm", "1400, 1450"),
        ("altura_asiento", 650, 950, "mm", "780, 820"),
        ("peso", 80, 400, "kg", "150, 180"),
        ("precio", 1000000, 150000000, "COP", "5000000, 15000000"),
        ("aceleracion_0_100", 2, 15, "s", "4.5, 6.2"),
        ("capacidad_maletas", 10, 100, "L", "30, 45"),
        ("espacio_baul", 10, 80, "L", "25, 35"),
        ("bateria_capacidad", 1, 30, "kWh", "5, 10"),
        ("autonomia_electrica", 30, 400, "km", "100, 150"),
        ("tiempo_carga", 0.5, 12, "h", "3, 6"),
        ("capacidad_pasajeros", 1, 4, "personas", "2, 3"),
        ("capacidad_carga", 50, 1000, "kg", "150, 300")
    ]
    for campo, min_v, max_v, unidad, ejemplo in rangos:
        cur.execute("INSERT OR IGNORE INTO rangos_validos (campo, min_valor, max_valor, unidad, ejemplo) VALUES (?, ?, ?, ?, ?)",
                   (campo, min_v, max_v, unidad, ejemplo))
    
    conn.commit()
    conn.close()
    print("✅ Base de datos de scores inicializada correctamente")


if __name__ == "__main__":
    print("🚀 Inicializando base de datos de scores...")
    init_scores_db()
    print("✨ Proceso completado. La base de datos está lista para usar.")
