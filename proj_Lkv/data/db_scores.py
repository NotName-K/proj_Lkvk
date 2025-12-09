import sqlite3

class DBScores:

    def __init__(self, db_file="scores.db"):
        self.db_file = db_file

    def get_score(self, apartado, valor):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(
            "SELECT puntaje FROM scores WHERE apartado = ? AND valor = ?",
            (apartado, valor)
        )
        row = cur.fetchone()
        conn.close()
        return row[0] if row else 0

    def get_marca_score(self, marca):
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(
            "SELECT puntaje FROM marca_confiabilidad WHERE marca = ?",
            (marca,)
        )
        row = cur.fetchone()
        conn.close()
        return row[0] if row else 0

    def get_penalizacion(self, texto_fallo):
        texto = texto_fallo.lower()
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(
            "SELECT penalizacion FROM fallos_scores WHERE ? LIKE '%' || palabra || '%'",
            (texto,)
        )
        row = cur.fetchone()
        conn.close()
        return row[0] if row else 0
