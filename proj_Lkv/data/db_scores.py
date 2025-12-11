import sqlite3
import re
from pathlib import Path

class DBScores:

    def __init__(self):
        
        base_path = Path(__file__).parent.parent / "data" / "data"
        base_path.mkdir(parents=True, exist_ok=True)

        self.db_file = base_path / "scores.db"
        
    
    
    def get_score(self, apartado, valor):
        if not valor:
            return 0
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
        if not marca:
            return 0
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(
            "SELECT puntaje FROM marca_confiabilidad WHERE marca = ?",
            (marca.lower(),)
        )
        row = cur.fetchone()
        conn.close()
        return row[0] if row else 0

    def get_penalizacion(self, texto_fallo):
        if not texto_fallo:
            return 0
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

    
    
    def get_valores_validos(self, campo):
        """Obtiene todos los valores válidos para un campo"""
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(
            "SELECT valor, ejemplo FROM valores_validos WHERE campo = ?",
            (campo,)
        )
        resultados = cur.fetchall()
        conn.close()
        return [(row[0], row[1]) for row in resultados]
    
    def get_rango_valido(self, campo):
        """Obtiene el rango válido para un campo numérico"""
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(
            "SELECT min_valor, max_valor, unidad, ejemplo FROM rangos_validos WHERE campo = ?",
            (campo,)
        )
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                'min': row[0],
                'max': row[1],
                'unidad': row[2],
                'ejemplo': row[3]
            }
        return None
    
    def validar_valor(self, campo, valor):
        """
        Valida si un valor es válido para un campo.
        Retorna (es_valido: bool, mensaje: str)
        """
        if not valor or valor.strip() == "":
            return True, ""  
        
        valor_lower = valor.lower().strip()
        valores_validos = self.get_valores_validos(campo)
        
        if not valores_validos:
            return True, ""  
        
        
        for val_db, ejemplo in valores_validos:
            if valor_lower == val_db.lower() or valor_lower in val_db.lower():
                return True, ""
        
        
        opciones = [v[0] for v in valores_validos]
        mensaje = f"❌ '{valor}' no es válido.\n📋 Opciones: {', '.join(opciones)}"
        if valores_validos[0][1]:  
            mensaje += f"\n💡 Ejemplo: {valores_validos[0][1]}"
        
        return False, mensaje
    
    def validar_numero(self, campo, valor):
        """
        Valida si un número está en el rango válido.
        Retorna (es_valido: bool, mensaje: str)
        """
        if valor is None:
            return True, ""  
        
        rango = self.get_rango_valido(campo)
        if not rango:
            return True, ""  
        
        try:
            num = float(valor)
            if rango['min'] <= num <= rango['max']:
                return True, ""
            else:
                mensaje = (
                    f" {num} {rango['unidad']} está fuera de rango.\n"
                    f" Rango válido: {rango['min']}-{rango['max']} {rango['unidad']}\n"
                    f" Ejemplos: {rango['ejemplo']}"
                )
                return False, mensaje
        except ValueError:
            return False, f"❌ '{valor}' no es un número válido"
    
    def normalizar_valor(self, campo, valor):
        """
        Normaliza un valor a su formato correcto en la BD.
        Útil para casos como 'SÍ' -> 'si', 'LED' -> 'LED', etc.
        """
        if not valor:
            return valor
        
        valor_lower = valor.lower().strip()
        valores_validos = self.get_valores_validos(campo)
        
        
        for val_db, _ in valores_validos:
            if valor_lower == val_db.lower() or valor_lower in val_db.lower():
                return val_db
        
        return valor  
    
    def mostrar_opciones(self, campo):
        """Muestra las opciones disponibles para un campo"""
        valores = self.get_valores_validos(campo)
        if valores:
            print(f"\n Opciones válidas para '{campo}':")
            for i, (valor, ejemplo) in enumerate(valores, 1):
                if ejemplo:
                    print(f"  {i}. {valor} - {ejemplo}")
                else:
                    print(f"  {i}. {valor}")
        else:
            rango = self.get_rango_valido(campo)
            if rango:
                print(f"\n Rango válido para '{campo}':")
                print(f"  Min: {rango['min']} {rango['unidad']}")
                print(f"  Max: {rango['max']} {rango['unidad']}")
                print(f"   Ejemplos: {rango['ejemplo']}")

    

    def extraer_hp(self, potencia_str):
        if not potencia_str:
            return None
        match = re.search(r'(\d+\.?\d*)\s*hp', potencia_str.lower())
        if match:
            return float(match.group(1))
        match = re.search(r'(\d+\.?\d*)\s*kw', potencia_str.lower())
        if match:
            return float(match.group(1)) * 1.34
        return None
    
    def extraer_rpm_potencia(self, potencia_str):
        if not potencia_str:
            return None
        match = re.search(r'@?\s*(\d+)\s*rpm', potencia_str.lower())
        if match:
            return int(match.group(1))
        return None
    
    def extraer_torque(self, torque_str):
        if not torque_str:
            return None
        match = re.search(r'(\d+\.?\d*)\s*nm', torque_str.lower())
        if match:
            return float(match.group(1))
        return None
    
    def extraer_rpm_torque(self, torque_str):
        if not torque_str:
            return None
        match = re.search(r'@?\s*(\d+)\s*rpm', torque_str.lower())
        if match:
            return int(match.group(1))
        return None
    
    def mapear_hp(self, hp):
        if not hp:
            return None
        if hp < 15:
            return "0-15"
        elif hp < 30:
            return "15-30"
        elif hp < 50:
            return "30-50"
        elif hp < 75:
            return "50-75"
        elif hp < 100:
            return "75-100"
        elif hp < 150:
            return "100-150"
        else:
            return "150+"
    
    def mapear_hp_rpm(self, rpm):
        if not rpm:
            return None
        if rpm < 6000:
            return "bajo"
        elif rpm < 8000:
            return "medio"
        else:
            return "alto"
    
    def mapear_torque(self, nm):
        if not nm:
            return None
        if nm < 10:
            return "0-10"
        elif nm < 20:
            return "10-20"
        elif nm < 40:
            return "20-40"
        elif nm < 70:
            return "40-70"
        elif nm < 100:
            return "70-100"
        else:
            return "100+"
    
    def mapear_torque_rpm(self, rpm):
        if not rpm:
            return None
        if rpm < 5000:
            return "bajo"
        elif rpm < 7000:
            return "medio"
        else:
            return "alto"
    
    def mapear_cilindraje(self, cc):
        if not cc:
            return None
        if cc < 125:
            return "0-125"
        elif cc < 250:
            return "125-250"
        elif cc < 400:
            return "250-400"
        elif cc < 600:
            return "400-600"
        elif cc < 1000:
            return "600-1000"
        else:
            return "1000+"
    
    def mapear_top_speed(self, speed):
        if not speed:
            return None
        if speed < 100:
            return "0-100"
        elif speed < 140:
            return "100-140"
        elif speed < 180:
            return "140-180"
        elif speed < 220:
            return "180-220"
        else:
            return "220+"
    
    def mapear_consumo(self, consumo):
        if not consumo:
            return None
        if consumo < 25:
            return "bajo"
        elif consumo < 35:
            return "medio"
        else:
            return "alto"
    
    def mapear_tanque(self, litros):
        if not litros:
            return None
        if litros < 10:
            return "pequeño"
        elif litros < 15:
            return "mediano"
        else:
            return "grande"
    
    def mapear_altura_asiento(self, mm):
        if not mm:
            return None
        if mm < 750:
            return "bajo"
        elif mm < 820:
            return "medio"
        else:
            return "alto"
    
    def mapear_peso(self, kg):
        if not kg:
            return None
        if kg < 150:
            return "ligero"
        elif kg < 200:
            return "medio"
        else:
            return "pesado"
    
    def mapear_vel_crucero(self, kmh):
        if not kmh:
            return None
        if kmh < 80:
            return "bajo"
        elif kmh < 110:
            return "medio"
        else:
            return "alto"
    
    def normalizar_freno(self, freno_str):
        if not freno_str:
            return None
        freno = freno_str.lower()
        if 'disco' in freno and 'doble' in freno:
            return "disco_doble"
        elif 'disco' in freno:
            return "disco_simple"
        elif 'tambor' in freno:
            return "tambor"
        return None
    
    def normalizar_abs(self, abs_str):
        if not abs_str:
            return "sin_abs"
        abs_lower = abs_str.lower()
        if 'doble' in abs_lower or 'dual' in abs_lower:
            return "abs_dual"
        elif 'mono' in abs_lower or 'simple' in abs_lower:
            return "abs_simple"
        return "sin_abs"
    
    def normalizar_transmision(self, trans_str):
        if not trans_str:
            return None
        trans = trans_str.lower()
        if 'automática' in trans or 'automatica' in trans:
            return "automatica"
        elif 'mecánica' in trans or 'mecanica' in trans:
            return "mecanica"
        return None
    
    def normalizar_caja(self, caja_str):
        if not caja_str:
            return None
        match = re.search(r'(\d+)', caja_str)
        if match:
            vel = int(match.group(1))
            if vel <= 4:
                return "4_vel"
            elif vel == 5:
                return "5_vel"
            else:
                return "6_vel"
        return None
    
    def normalizar_suspension(self, susp_str):
        if not susp_str:
            return None
        susp = susp_str.lower()
        if 'invertida' in susp or 'upside' in susp:
            return "invertida"
        elif 'telescópica' in susp or 'telescopica' in susp:
            return "telescopica"
        elif 'monoamortiguador' in susp or 'mono' in susp:
            return "monoamortiguador"
        return "basica"
    
    def normalizar_parabrisas(self, parabrisas_str):
        if not parabrisas_str:
            return None
        if parabrisas_str.lower() in ['sí', 'si', 'yes']:
            return "ajustable"
        return None
    
    def normalizar_modos(self, modos_str):
        if not modos_str:
            return None
        modos = len(modos_str.split(','))
        if modos >= 3:
            return "multiples"
        elif modos == 2:
            return "dos"
        return None
    
    def normalizar_faros(self, faros_str):
        if not faros_str:
            return None
        faros = faros_str.lower()
        if 'led' in faros:
            return "led"
        else:
            return "halogena"
    
    def normalizar_neumaticos(self, neumaticos_str):
        if not neumaticos_str:
            return None
        neu = neumaticos_str.lower()
        if 'michelin' in neu or 'pirelli' in neu or 'dunlop' in neu:
            return "premium"
        elif 'metzeler' in neu or 'bridgestone' in neu:
            return "calidad"
        else:
            return "estandar"

    def extraer_metricas_moto(self, moto):
        motor = moto.motor
        transmision = moto.transmision
        rendimiento = moto.rendimiento
        electronica = moto.electronica
        chasis = moto.chasis
        dimensiones = moto.dimensiones
        info = moto.info
        atributos = moto.atributos_especificos
        
        hp = self.extraer_hp(motor.potencia if hasattr(motor, 'potencia') else None)
        hp_rpm = self.extraer_rpm_potencia(motor.potencia if hasattr(motor, 'potencia') else None)
        torque_val = self.extraer_torque(motor.torque if hasattr(motor, 'torque') else None)
        torque_rpm = self.extraer_rpm_torque(motor.torque if hasattr(motor, 'torque') else None)
        
        metricas = {
            'hp_rango': self.mapear_hp(hp),
            'hp_rpm_rango': self.mapear_hp_rpm(hp_rpm),
            'torque_rango': self.mapear_torque(torque_val),
            'torque_rpm_rango': self.mapear_torque_rpm(torque_rpm),
            'cilindraje_rango': self.mapear_cilindraje(motor.cilindraje if hasattr(motor, 'cilindraje') else None),
            'top_speed_rango': self.mapear_top_speed(rendimiento.top_speed if rendimiento else None),
            'freno_del': self.normalizar_freno(chasis.freno_d),
            'freno_tras': self.normalizar_freno(chasis.freno_t),
            'abs': self.normalizar_abs(electronica.abs_sistema),
            'transmision': self.normalizar_transmision(transmision.tipo),
            'tipo_caja': self.normalizar_caja(transmision.caja_cambios),
            'consumo_rango': self.mapear_consumo(rendimiento.consumo if rendimiento else None),
            'tanque_rango': self.mapear_tanque(rendimiento.capacidad_tanque if rendimiento else None),
            'susp_del': self.normalizar_suspension(chasis.suspension_d),
            'susp_tras': self.normalizar_suspension(chasis.suspension_t),
            'altura_asiento_rango': self.mapear_altura_asiento(dimensiones.altura_asiento),
            'parabrisas': self.normalizar_parabrisas(
                atributos.parabrisas_ajustable if atributos and hasattr(atributos, 'parabrisas_ajustable') else None
            ),
            'peso_rango': self.mapear_peso(dimensiones.peso),
            'vel_crucero_rango': self.mapear_vel_crucero(rendimiento.vel_crucero if rendimiento else None),
            'modos_rango': self.normalizar_modos(
                atributos.modos_manejo if atributos and hasattr(atributos, 'modos_manejo') else None
            ),
            'iluminacion': self.normalizar_faros(electronica.faros),
            'pantalla': 'digital',
            'neumaticos': self.normalizar_neumaticos(chasis.neumaticos),
            'marca': info.marca,
            'fallos_lista': info.get_fallos_lista(),
            'precio': info.precio or 10000000
        }
        
        return metricas
