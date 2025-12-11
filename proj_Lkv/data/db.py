import re
import sqlite3
from pathlib import Path
from data.scores_db_init import init_scores_db
from data.db_scores import DBScores

DB_PATH = Path(__file__).parent / "data" / "moto.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
CREATE TABLE IF NOT EXISTS moto (
    id TEXT PRIMARY KEY,
    marca TEXT,
    modelo TEXT,
    año INTEGER,
    tipo TEXT,
    color TEXT,

    cilindraje INTEGER,
    tiempos TEXT,
    cilindros TEXT,
    arbol_levas TEXT,
    refrigeracion TEXT,
    arranque TEXT,
    embrague TEXT,
    sliper_clutch TEXT,
    inyeccion TEXT,
    potencia TEXT,
    torque TEXT,

    transmision TEXT,
    caja_cambios TEXT,

    consumo REAL,
    capacidad_tanque REAL,

    vel_crucero REAL,
    top_speed REAL,

    faros TEXT,
    direccionales TEXT,
    abs_sistema TEXT,

    suspension_d TEXT,
    suspension_t TEXT,
    freno_d TEXT,
    freno_t TEXT,
    neumaticos TEXT,

    largo REAL,
    ancho REAL,
    altura REAL,
    distancia_ejes REAL,
    altura_asiento REAL,
    peso REAL,

    precio REAL,

    fallos_comunes TEXT,

    aceleracion_0_100 REAL,

    capacidad_maletas REAL,
    parabrisas_ajustable TEXT,
    control_crucero TEXT,

    espacio_baul REAL,

    suspension_largo_recorrido TEXT,
    proteccion_motor TEXT,
    tanque_grande TEXT,

    maletas_laterales TEXT,
    suspension_ajustable TEXT,
    modos_manejo TEXT,

    bateria_capacidad REAL,
    autonomia_electrica REAL,
    tiempo_carga REAL,

    capacidad_pasajeros INTEGER,
    capacidad_carga REAL
);
    """)
    conn.commit()
    conn.close()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()  # FIX: Crea cursor persistente aquí
        self.validator = DBScores()

    def cerrar(self):
        self.conn.commit()  # FIX: Commit pendiente antes de cerrar
        self.conn.close()

    def get_moto(self, moto_id):
        self.cursor.execute("SELECT * FROM moto WHERE id = ?", (moto_id,))
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None

    def listar_motos(self):
        try:
            self.cursor.execute("""
                SELECT id, marca, modelo, tipo, COALESCE(precio, 0) AS precio, año 
                FROM moto 
                ORDER BY marca, modelo
            """)
            filas = self.cursor.fetchall()
            return [
                {
                    'id': f[0],
                    'marca': f[1],
                    'modelo': f[2],
                    'tipo': f[3],
                    'precio': f[4],
                    'año': f[5]
                } for f in filas
            ]
        except Exception as e:
            print(f"Error al listar: {e}")
            return []

    def agregar_moto_db(self, moto):
        columnas = ', '.join(moto.keys())
        placeholders = ':' + ', :'.join(moto.keys())
        sql = f"INSERT OR REPLACE INTO moto ({columnas}) VALUES ({placeholders})"  # FIX: OR REPLACE para updates si ID existe
        self.cursor.execute(sql, moto)
        self.conn.commit()
        return moto['id']

    def borrar_moto_db(self, moto_id):
        self.cursor.execute("DELETE FROM moto WHERE id = ?", (moto_id,))
        self.conn.commit()

    # ============ MÉTODOS DE INPUT CON VALIDACIÓN ============

    def pedir_texto_validado(self, msg, campo, obligatorio=False):
        """Pide texto y valida contra valores_validos"""
        while True:
            valor = input(msg).strip()
            
            if not valor and not obligatorio:
                return None
            
            if not valor and obligatorio:
                print("⚠️  Este campo es obligatorio")
                continue
            
            es_valido, mensaje = self.validator.validar_valor(campo, valor)
            
            if es_valido:
                return self.validator.normalizar_valor(campo, valor)
            else:
                print(mensaje)
                self.validator.mostrar_opciones(campo)

    def pedir_float_validado(self, msg, campo, obligatorio=False):
        """Pide float y valida contra rangos_validos"""
        while True:
            try:
                valor_str = input(msg).strip()
                
                if not valor_str and not obligatorio:
                    return None
                
                if not valor_str and obligatorio:
                    print("⚠️  Este campo es obligatorio")
                    continue
                
                valor = float(valor_str)
                es_valido, mensaje = self.validator.validar_numero(campo, valor)
                
                if es_valido:
                    return valor
                else:
                    print(mensaje)
                    
            except ValueError:
                print("❌ Número inválido. Intenta de nuevo.")
                rango = self.validator.get_rango_valido(campo)
                if rango:
                    print(f"💡 Ejemplos: {rango['ejemplo']}")

    def pedir_int_validado(self, msg, campo, obligatorio=False):
        """Pide int y valida contra rangos_validos"""
        while True:
            try:
                valor_str = input(msg).strip()
                
                if not valor_str and not obligatorio:
                    return None
                
                if not valor_str and obligatorio:
                    print("⚠️  Este campo es obligatorio")
                    continue
                
                valor = int(valor_str)
                es_valido, mensaje = self.validator.validar_numero(campo, valor)
                
                if es_valido:
                    return valor
                else:
                    print(mensaje)
                    
            except ValueError:
                print("❌ Número inválido. Intenta de nuevo.")
                rango = self.validator.get_rango_valido(campo)
                if rango:
                    print(f"💡 Ejemplos: {rango['ejemplo']}")

    def pedir_texto(self, msg):
        """Input de texto sin validación (para campos libres)"""
        return input(msg).strip() or None

    def pedir_float(self, msg):
        """Input de float sin validación"""
        while True:
            try:
                valor = input(msg).strip()
                if not valor:
                    return None
                return float(valor)
            except ValueError:
                print("❌ Número inválido")

    def pedir_int(self, msg):
        """Input de int sin validación"""
        while True:
            try:
                valor = input(msg).strip()
                if not valor:
                    return None
                return int(valor)
            except ValueError:
                print("❌ Número inválido")
                
    def pedir_potencia(self):
        

        while True:
            txt = input("Potencia (ej: 15 hp, 8000): ").lower().strip()

            match = re.match(r"^(\d+(\.\d+)?)\s*(hp|cv)\s*,\s*(\d+)$", txt)
            if not match:
                print("❌ Formato inválido. Ejemplo correcto: 15 hp, 8000")
                continue

            valor = float(match.group(1))    # potencia (hp/cv)
            rpm = int(match.group(4))        # rpm

        # Límites
            if not (1 <= valor <= 300):
                print("❌ Potencia fuera de rango (1–300 hp)")
                continue

            if not (1000 <= rpm <= 20000):
                print("❌ RPM fuera de rango (1000–20000)")
                continue

            return txt
        
    def pedir_torque(self):
        import re

        while True:
            txt = input("Torque (ej: 14 nm, 6500): ").lower().strip()

            match = re.match(r"^(\d+(\.\d+)?)\s*nm\s*,\s*(\d+)$", txt)
            if not match:
                print("❌ Formato inválido. Ejemplo correcto: 14 nm, 6500")
                continue

            valor = float(match.group(1))    # torque en nm
            rpm = int(match.group(3))        # rpm
        # Límites
            if not (1 <= valor <= 300):
                print("❌ Torque fuera de rango (1–300 Nm)")
                continue

            if not (1000 <= rpm <= 20000):
                print("❌ RPM fuera de rango (1000–20000)")
                continue

            return txt


    # ============ MÉTODOS POR TIPO DE MOTO ============

    def pd_naked(self):
        return {
            'aceleracion_0_100': self.pedir_float_validado("Aceleración 0-100 km/h (s): ", "aceleracion_0_100"),
        }

    def pd_sport(self):
        return {
            'aceleracion_0_100': self.pedir_float_validado("Aceleración 0-100 km/h (s): ", "aceleracion_0_100"),
            'modos_manejo': self.pedir_texto("Modos de conducción (Rain, Road, Sport): "),
        }

    def pd_touring(self):
        return {
            'capacidad_maletas': self.pedir_float_validado("Capacidad maletas (L): ", "capacidad_maletas"),
            'parabrisas_ajustable': self.pedir_texto_validado("¿Parabrisas ajustable? (si/no): ", "parabrisas_ajustable"),
            'control_crucero': self.pedir_texto_validado("¿Control crucero? (si/no): ", "control_crucero"),
            'tanque_grande': self.pedir_texto_validado("¿Tanque grande? (si/no): ", "tanque_grande"),
            'proteccion_motor': self.pedir_texto_validado("¿Protección motor? (si/no): ", "proteccion_motor"),
            'suspension_largo_recorrido': self.pedir_texto_validado("¿Suspensión largo recorrido? (si/no): ", "suspension_largo_recorrido"),
            'modos_manejo': self.pedir_texto("Modos de manejo: "),
        }

    def pd_scooter(self):
        return {
            'espacio_baul': self.pedir_float_validado("Espacio baúl (L): ", "espacio_baul"),
        }

    def pd_street(self):
        return {}

    def pd_doble_pps(self):
        return {
            'suspension_largo_recorrido': self.pedir_texto_validado("¿Suspensión largo recorrido? (si/no): ", "suspension_largo_recorrido"),
            'proteccion_motor': self.pedir_texto_validado("¿Protección motor? (si/no): ", "proteccion_motor"),
            'tanque_grande': self.pedir_texto_validado("¿Tanque grande? (si/no): ", "tanque_grande"),
        }

    def pd_adventure(self):
        return {
            'maletas_laterales': self.pedir_texto_validado("¿Maletas laterales? (si/no): ", "maletas_laterales"),
            'proteccion_motor': self.pedir_texto_validado("¿Protección de motor? (si/no): ", "proteccion_motor"),
            'suspension_ajustable': self.pedir_texto_validado("¿Suspensión ajustable? (si/no): ", "suspension_ajustable"),
            'modos_manejo': self.pedir_texto("Modos de manejo: "),
        }

    def pd_electric(self):
        return {
            'bateria_capacidad': self.pedir_float_validado("Capacidad batería (kWh): ", "bateria_capacidad"),
            'autonomia_electrica': self.pedir_float_validado("Autonomía eléctrica (km): ", "autonomia_electrica"),
            'tiempo_carga': self.pedir_float_validado("Tiempo de carga (h): ", "tiempo_carga"),
        }

    def pd_motocarro(self):
        return {
            'capacidad_pasajeros': self.pedir_int_validado("Capacidad pasajeros: ", "capacidad_pasajeros"),
            'capacidad_carga': self.pedir_float_validado("Capacidad de carga (kg): ", "capacidad_carga"),
        }

    def agregar_moto(self):
        print("\n" + "="*60)
        print("🏍️  AGREGAR NUEVA MOTO")
        print("="*60)
        
        # Mostrar tipos disponibles
                # Mostrar tipos disponibles
        print("\n📋 TIPOS DE MOTO DISPONIBLES:")
        self.validator.mostrar_opciones("tipo")
        
        tipos = {
    '1': 'adventure',
    '2': 'doble proposito',
    '3': 'electric',
    '4': 'motocarro',
    '5': 'naked',
    '6': 'scooter',
    '7': 'sport',
    '8': 'street',
    '9': 'touring'
     }


        # 🔄 BUCLE PARA OBLIGAR A ELEGIR UN VALOR CORRECTO
        while True:
            tn = input("\nSelecciona tipo (1-9): ").strip()
            tps = tipos.get(tn)

            if tps:
                break   # ✔️ Tipo válido → salimos del bucle
            else:
                print("❌ Tipo inválido. Debes seleccionar un número entre 1 y 9.")

        print(f"\n✅ Tipo seleccionado: {tps.upper()}")


        marca = self.pedir_texto_validado("Marca: ", "marca", obligatorio=True)
        modelo = self.pedir_texto("Modelo: ")
        año = self.pedir_int_validado("Año: ", "año", obligatorio=True)
        color = self.pedir_texto("Colores disponibles: ")

        es_combustion = tps != 'electric'

        if es_combustion:
            print("\n" + "-"*60)
            print("MOTOR Y RENDIMIENTO")
            print("-"*60)
            
            cilindraje = self.pedir_int_validado("Cilindraje (cc): ", "cilindraje", obligatorio=True)
            tiempos = self.pedir_texto_validado("Tiempos (2T/4T): ", "tiempos", obligatorio=True)
            cilindros = self.pedir_texto_validado("Configuración de cilindros: ", "cilindros")
            arbol_levas = self.pedir_texto("Tipo de árbol de levas (SOHC, DOHC): ")
            refrigeracion = self.pedir_texto_validado("Sistema de refrigeración: ", "refrigeracion")
            arranque = self.pedir_texto_validado("Tipo de arranque: ", "arranque")
            sliper_clutch = self.pedir_texto_validado("¿Sliper clutch? (si/no): ", "sliper_clutch")
            inyeccion = self.pedir_texto_validado("Sistema de inyección: ", "inyeccion")
            potencia = self.pedir_potencia()
            torque = self.pedir_torque()
            consumo = self.pedir_float_validado("Consumo (km/l): ", "consumo")
            capacidad_tanque = self.pedir_float_validado("Capacidad tanque (L): ", "capacidad_tanque")
        else:
            cilindraje = None
            tiempos = None
            cilindros = None
            arbol_levas = None
            refrigeracion = None
            arranque = None
            embrague = None
            sliper_clutch = None
            inyeccion = None
            potencia = self.pedir_texto("Potencia (kW): ")
            torque = self.pedir_texto("Torque (Nm): ")
            consumo = None
            capacidad_tanque = None

        print("\n" + "-"*60)
        print("TRANSMISIÓN")
        print("-"*60)

        if tps in ['scooter', 'electric']:
            transmision = "automatica"
            caja_cambios = None
            if tps == "scooter":
                embrague = "CVT"
            elif tps == "electric":
                embrague = "Unidireccional"
        else:
            transmision = self.pedir_texto_validado("Transmisión: ", "transmision")
            caja_cambios = self.pedir_texto_validado("Caja de cambios (ej: 6 vel): ", "caja")
            embrague = self.pedir_texto_validado("Tipo de embrague: ", "embrague")

        print("\n" + "-"*60)
        print("VELOCIDAD Y RENDIMIENTO")
        print("-"*60)

        vel_crucero = self.pedir_float_validado("Velocidad crucero (km/h): ", "vel_crucero")
        top_speed = self.pedir_float_validado("Velocidad máxima (km/h): ", "top_speed")

        print("\n" + "-"*60)
        print("ELECTRÓNICA Y SISTEMAS")
        print("-"*60)

        faros = self.pedir_texto_validado("Faros: ", "faros")
        direccionales = self.pedir_texto_validado("Direccionales: ", "faros")
        abs_sistema = self.pedir_texto_validado("ABS: ", "abs_sistema")

        print("\n" + "-"*60)
        print("CHASIS Y SUSPENSIÓN")
        print("-"*60)

        suspension_d = self.pedir_texto_validado("Suspensión delantera: ", "suspension_d")
        suspension_t = self.pedir_texto_validado("Suspensión trasera: ", "suspension_t")
        freno_d = self.pedir_texto_validado("Freno delantero: ", "freno")
        freno_t = self.pedir_texto_validado("Freno trasero: ", "freno")
        neumaticos = self.pedir_texto_validado("Neumáticos: ", "neumaticos")

        print("\n" + "-"*60)
        print("DIMENSIONES Y PESO")
        print("-"*60)

        dimensiones = self.pedir_texto("Dimensiones L x A x H (mm): ")

        if dimensiones:
            try:
                partes = [x.strip() for x in dimensiones.lower().split('x')]
                largo = float(partes[0]) if len(partes) > 0 else None
                ancho = float(partes[1]) if len(partes) > 1 else None
                altura = float(partes[2]) if len(partes) > 2 else None
            except:
                largo = self.pedir_float_validado("Largo (mm): ", "largo")
                ancho = self.pedir_float_validado("Ancho (mm): ", "ancho")
                altura = self.pedir_float_validado("Altura (mm): ", "altura")
        else:
            largo = None
            ancho = None
            altura = None

        distancia_ejes = self.pedir_float_validado("Distancia entre ejes (mm): ", "distancia_ejes")
        altura_asiento = self.pedir_float_validado("Altura asiento (mm): ", "altura_asiento")
        peso = self.pedir_float_validado("Peso seco (kg): ", "peso")

        print("\n" + "-"*60)
        print("PRECIO Y OBSERVACIONES")
        print("-"*60)

        precio = self.pedir_float_validado("Precio (COP): ", "precio")
        fallos_comunes = self.pedir_texto("Fallos comunes: ")

        moto = {
            'id': f"{marca[:3].upper()}-{modelo.replace(' ', '')}",
            'marca': marca,
            'modelo': modelo,
            'año': año,
            'tipo': tps,
            'color': color,

            'cilindraje': cilindraje,
            'tiempos': tiempos,
            'cilindros': cilindros,
            'arbol_levas': arbol_levas,
            'refrigeracion': refrigeracion,
            'arranque': arranque,
            'embrague': embrague,
            'sliper_clutch': sliper_clutch,
            'inyeccion': inyeccion,
            'potencia': potencia,
            'torque': torque,

            'transmision': transmision,
            'caja_cambios': caja_cambios,

            'consumo': consumo,
            'capacidad_tanque': capacidad_tanque,

            'vel_crucero': vel_crucero,
            'top_speed': top_speed,

            'faros': faros,
            'direccionales': direccionales,
            'abs_sistema': abs_sistema,

            'suspension_d': suspension_d,
            'suspension_t': suspension_t,
            'freno_d': freno_d,
            'freno_t': freno_t,
            'neumaticos': neumaticos,

            'largo': largo,
            'ancho': ancho,
            'altura': altura,
            'distancia_ejes': distancia_ejes,
            'altura_asiento': altura_asiento,
            'peso': peso,

            'precio': precio,
            'fallos_comunes': fallos_comunes,

            'aceleracion_0_100': None,
            'modos_manejo': None,
            'capacidad_maletas': None,
            'parabrisas_ajustable': None,
            'control_crucero': None,
            'espacio_baul': None,
            'suspension_largo_recorrido': None,
            'proteccion_motor': None,
            'tanque_grande': None,
            'maletas_laterales': None,
            'suspension_ajustable': None,
            'bateria_capacidad': None,
            'autonomia_electrica': None,
            'tiempo_carga': None,
            'capacidad_pasajeros': None,
            'capacidad_carga': None
        }

        print("\n" + "-"*60)
        print("DATOS ESPECÍFICOS DEL TIPO")
        print("-"*60)

        datos_ex = {}
        if tps == 'naked':
            datos_ex = self.pd_naked()
        elif tps == 'sport':
            datos_ex = self.pd_sport()
        elif tps == 'touring':
            datos_ex = self.pd_touring()
        elif tps == 'scooter':
            datos_ex = self.pd_scooter()
        elif tps == 'street':
            datos_ex = self.pd_street()
        elif tps == 'doble proposito':
            datos_ex = self.pd_doble_pps()
        elif tps == 'adventure':
            datos_ex = self.pd_adventure()
        elif tps == 'electric':
            datos_ex = self.pd_electric()
        elif tps == 'motocarro':
            datos_ex = self.pd_motocarro()

        moto.update(datos_ex)

        self.agregar_moto_db(moto)
        
        print("\n" + "="*60)
        print(f"✅ Moto '{marca} {modelo}' agregada exitosamente!")
        print(f"🆔 ID: {moto['id']}")
        print("="*60 + "\n")
        
        return moto['id']
    
    def obtener_modelos_por_marca(self, marca):
        self.cursor.execute("""
            SELECT id, marca, modelo, tipo, año
            FROM moto
            WHERE marca LIKE ?
            ORDER BY modelo ASC
        """, (f"%{marca}%",))
        return [dict(row) for row in self.cursor.fetchall()]

    def obtener_detalles(self, moto_id):
        self.cursor.execute("SELECT * FROM moto WHERE id = ?", (moto_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def actualizar_campo_moto(self, moto_id, campo, valor):
        self.cursor.execute(f"UPDATE moto SET {campo}=? WHERE id=?", (valor, moto_id))
        self.conn.commit()

    def eliminar_moto(self, moto_id):
        self.borrar_moto_db(moto_id)