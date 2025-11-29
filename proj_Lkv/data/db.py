import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "moto.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
CREATE TABLE IF NOT EXISTS moto (
    -- Identificación
    id TEXT PRIMARY KEY,
    marca TEXT,
    modelo TEXT,
    año INTEGER,
    tipo TEXT,
    color TEXT,
    colores TEXT,

    -- Motor y rendimiento
    cilindraje INTEGER,
    ciclos INTEGER,
    arbol_levas TEXT,
    refrigeracion TEXT,
    arranque TEXT,
    embrague TEXT,
    sliper_clutch TEXT,
    inyeccion TEXT,
    potencia TEXT,
    torque REAL,
    transmision TEXT,
    consumo REAL,
    capacidad_tanque REAL,
    vel_crucero REAL,
    top_speed REAL,
    bateria TEXT,
    tablero INTEGER,
    faros TEXT,
    direccionales TEXT,
    seguridad TEXT,
    abs_sistema TEXT,
    suspension_d TEXT,
    suspension_t TEXT,
    freno_d TEXT,
    freno_t TEXT,
    frenos_delanteros TEXT,
    frenos_traseros TEXT,
    neumaticos TEXT,
    largo REAL,
    ancho REAL,
    altura REAL,
    distancia_ejes REAL,
    altura_asiento REAL,
    peso REAL,
    precio REAL,
    accesorios TEXT,
    fallos_comunes TEXT
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

    def get_todas(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM moto")
        return [dict(row) for row in cur.fetchall()]

    def agregar_moto(self, moto):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO moto VALUES (
                :id, :marca, :modelo, :cilindraje, :precio, :tipo, :seguridad,
                :suspension, :peso, :transmision, :iluminacion, :potencia, :torque,
                :capacidad_tanque, :consumo, :color, :neumaticos, :frenos_delanteros,
                :frenos_traseros, :vel_crucero, :top_speed, :accesorios, :fallos_comunes
            )
        """, moto)
        self.conn.commit()
        return moto['id']

    def borrar_moto(self, moto_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM moto WHERE id = ?", (moto_id,))
        self.conn.commit()
        
if __name__ == "__main__":
    init_db()