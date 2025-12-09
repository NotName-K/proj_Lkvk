import sqlite3
from pathlib import Path

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

    def cerrar(self):
        self.conn.close()

    def get_moto(self, moto_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM moto WHERE id = ?", (moto_id,))
        row = cur.fetchone()
        if row:
            return dict(row)
        return None

    def listar_motos(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, marca, modelo, tipo, año FROM moto")
        return [dict(row) for row in cur.fetchall()]

    def agregar_moto_db(self, moto):
        columnas = ', '.join(moto.keys())
        placeholders = ':' + ', :'.join(moto.keys())
        sql = f"INSERT INTO moto ({columnas}) VALUES ({placeholders})"
        cur = self.conn.cursor()
        cur.execute(sql, moto)
        self.conn.commit()
        return moto['id']

    def borrar_moto_db(self, moto_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM moto WHERE id = ?", (moto_id,))
        self.conn.commit()

    def pedir_texto(self, msg):
        return input(msg).strip()

    def pedir_float(self, msg):
        while True:
            try:
                valor = input(msg).strip()
                if not valor:
                    return None
                return float(valor)
            except ValueError:
                print("Número inválido")

    def pedir_int(self, msg):
        while True:
            try:
                valor = input(msg).strip()
                if not valor:
                    return None
                return int(valor)
            except ValueError:
                print("Número inválido")

    def pd_naked(self):
        return {
            'aceleracion_0_100': self.pedir_float("Aceleración 0_100 km/h (s): "),
        }

    def pd_sport(self):
        return {
            'aceleracion_0_100': self.pedir_float("Aceleración 0_100 km/h (s): "),
            'modos_manejo': self.pedir_texto("Modos de conducción(Rain,road, etc... ): ") or None,
        }

    def pd_touring(self):
        return {
            'capacidad_maletas': self.pedir_float("Capacidad maletas (L): "),
            'parabrisas_ajustable': self.pedir_texto("¿Parabrisas ajustable? (Sí/No): ") or None,
            'control_crucero': self.pedir_texto("¿Control crucero? (Sí/No): ") or None,
            'tanque_grande': self.pedir_texto("¿Tanque grande? (Sí/No): ") or None,
            'proteccion_motor': self.pedir_texto("¿Protección motor? (Sí/No): ") or None,  
            'suspension_largo_recorrido': self.pedir_texto("Recorrido suspensión (Sí/No): "), 
            'modos_manejo': self.pedir_texto("Modos de manejo: ") or None
        }

    def pd_scooter(self):
        return {
            'espacio_baul': self.pedir_float("Espacio baúl (L): "),
        }

    def pd_street(self):
        return {}

    def pd_doble_pps(self):
        return {
            'suspension_largo_recorrido': self.pedir_texto("Recorrido suspensión (Sí/No): "),
            'proteccion_motor': self.pedir_texto("¿Protección motor? (Sí/No): ") or None,
            'tanque_grande': self.pedir_texto("¿Tanque grande? (Sí/No): ") or None
        }

    def pd_adventure(self):
        return {
            'maletas_laterales': self.pedir_texto("¿Maletas laterales? (Sí/No): ") or None,
            'proteccion_motor': self.pedir_texto("¿Protección de motor? (Sí/No): ") or None,
            'suspension_ajustable': self.pedir_texto("¿Suspensión ajustable? (Sí/No): ") or None,
            'modos_manejo': self.pedir_texto("Modos de manejo: ") or None
        }

    def pd_electric(self):
        return {
            'bateria_capacidad': self.pedir_float("Capacidad batería (kWh): "),
            'autonomia_electrica': self.pedir_float("Autonomía eléctrica (km): "),
            'tiempo_carga': self.pedir_float("Tiempo de carga (h): ")
        }

    def pd_motocarro(self):
        return {
            'capacidad_pasajeros': self.pedir_int("Capacidad pasajeros: "),
            'capacidad_carga': self.pedir_float("Capacidad de carga (kg): ")
        }

    def agregar_moto(self):
        tipos = {
            '1': 'naked',
            '2': 'sport',
            '3': 'touring',
            '4': 'scooter',
            '5': 'street',
            '6': 'doble pps',
            '7': 'adventure',
            '8': 'electric',
            '9': 'motocarro'
        }

        for num, tipo in tipos.items():
            print(f"{num}. {tipo}")

        tn = input("Selecciona tipo (1-9): ").strip()
        tps = tipos.get(tn)
        if not tps:
            return None

        marca = self.pedir_texto("Marca: ")
        modelo = self.pedir_texto("Modelo: ")
        año = self.pedir_int("Año: ")
        color = self.pedir_texto("Colores disponibles: ")

        es_combustion = tps != 'electric'

        if es_combustion:
            cilindraje = self.pedir_int("Cilindraje (cc): ")
            tiempos= self.pedir_texto("tiempos(4T,2T): ")
            cilindros = self.pedir_texto("Configuración de cilindros (ej: monocilíndrico, bicilíndrico paralelo, V2): ")
            arbol_levas = self.pedir_texto("Tipo de árbol de levas (ej: SOHC, DOHC): ")
            refrigeracion = self.pedir_texto("Sistema de refrigeración (ej: aire, aire-aceite, líquido): ")
            arranque = self.pedir_texto("Tipo de arranque (eléctrico, pedal, Ambos): ")
            sliper_clutch = self.pedir_texto("¿Sliper clutch?: ")
            inyeccion = self.pedir_texto("Sistema de inyección (FI, carburador): ")
            potencia = self.pedir_texto("Potencia(Hp rpm): ")
            torque = self.pedir_texto("Torque(nm rpm): ")
            consumo = self.pedir_float("Consumo (km/l): ")
            capacidad_tanque = self.pedir_float("Capacidad tanque (L): ")
        else:
            cilindraje = None
            tiempos= None
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

        if tps in ['scooter', 'electric']:
            transmision = "Automática"
            caja_cambios = None
            if tps == "scooter":
                embrague = "CVT"
            elif tps == "electric":
                embrague = "Unidireccional"
        else:
            transmision = self.pedir_texto("Transmisión (Mecánica/Automática): ")
            caja_cambios = self.pedir_texto("Caja de cambios (5,6 vel): ")
            embrague = self.pedir_texto("Tipo de embrague (multidisco, bidisco,...): ")

        vel_crucero = self.pedir_float("Velocidad crucero: ")
        top_speed = self.pedir_float("Velocidad máxima: ")

        faros = self.pedir_texto("Faros(LED, Halógena): ")
        direccionales = self.pedir_texto("Direccionales(LED, Halógena): ")
        abs_sistema = self.pedir_texto("ABS(Mono, Doble): ")

        suspension_d = self.pedir_texto("Suspensión delantera(telescópica, invertida,...): ")
        suspension_t = self.pedir_texto("Suspensión trasera(telescópica, invertida,...): ")
        freno_d = self.pedir_texto("Freno delantero(Disco, tambor): ")
        freno_t = self.pedir_texto("Freno trasero(Disco, tambor): ")
        neumaticos = self.pedir_texto("Neumáticos(michelin, mrf, cst,...): ")

        dimensiones = self.pedir_texto("Dimensiones L x A x H: ")

        if dimensiones:
            try:
                partes = [x.strip() for x in dimensiones.lower().split('x')]
                largo = float(partes[0]) if len(partes) > 0 else None
                ancho = float(partes[1]) if len(partes) > 1 else None
                altura = float(partes[2]) if len(partes) > 2 else None
            except:
                largo = self.pedir_float("Largo (mm): ")
                ancho = self.pedir_float("Ancho (mm): ")
                altura = self.pedir_float("Altura (mm): ")
        else:
            largo = None
            ancho = None
            altura = None

        distancia_ejes = self.pedir_float("Distancia entre ejes(mm): ")
        altura_asiento = self.pedir_float("Altura asiento(mm): ")
        peso = self.pedir_float("Peso seco(kg): ")

        precio = self.pedir_float("Precio: ")
        
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
    'modos_manejo': None,

    'bateria_capacidad': None,
    'autonomia_electrica': None,
    'tiempo_carga': None,

    'capacidad_pasajeros': None,
    'capacidad_carga': None
}

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
        elif tps == 'doble pps':
            datos_ex = self.pd_doble_pps()
        elif tps == 'adventure':
            datos_ex = self.pd_adventure()
        elif tps == 'electric':
            datos_ex = self.pd_electric()
        elif tps == 'motocarro':
            datos_ex = self.pd_motocarro()

        moto.update(datos_ex)

        self.agregar_moto_db(moto)
        return moto['id']

if __name__ == "__main__":
    init_db()
    db = DB()
    db.agregar_moto()
    db.cerrar()
