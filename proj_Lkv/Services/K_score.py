from Core.moto import crear_moto
class KronoScore:
    
    def __init__(self, db_scores):
        """
        Inicializa KronoScore con una instancia de DBScores
        
        Args:
            db_scores: Instancia de DBScores para acceder a las tablas de puntuación
        """
        self.db = db_scores
    
    def calcular(self, moto, precio_promedio_categoria=10000000):
        """
        Calcula el KronoScore completo de una motocicleta
        
        Args:
            moto: Instancia de una clase Moto (o subclase)
            precio_promedio_categoria: Precio promedio de la categoría para ajuste
            
        Returns:
            dict con todas las puntuaciones calculadas
        """
        # Extraer métricas normalizadas de la moto
        m = self.db.extraer_metricas_moto(moto)
        
        # Calcular scores por categoría (valores brutos)
        rend = self._score_rendimiento(m)
        cons = self._score_consumo(m)
        viaje = self._score_viajes(m)
        disen = self._score_diseno(m)
        confi = self._score_confiabilidad(m)
        
        # Normalizar a escala 0-100
        n_rend = self._norm(rend, 120)
        n_cons = self._norm(cons, 40)
        n_viaje = self._norm(viaje, 60)
        n_disen = self._norm(disen, 30)
        n_confi = self._norm(confi, 60)
        
        # Calcular Krono Calidad (promedio ponderado)
        krono_calidad = (
            n_rend * 0.35 +
            n_cons * 0.15 +
            n_viaje * 0.20 +
            n_disen * 0.10 +
            n_confi * 0.20
        )
        
        # Ajustar por precio
        krono_precio = self._ajuste_precio(
            krono_calidad,
            m.get("precio", 10000000),
            precio_promedio_categoria
        )
        
        return {
            "rendimiento": round(n_rend, 1),
            "consumoYAutonomia": round(n_cons, 1),
            "viajesYComodidad": round(n_viaje, 1),
            "disenoYMateriales": round(n_disen, 1),
            "confiabilidad": round(n_confi, 1),
            "krono_calidad": round(krono_calidad, 1),
            "krono_precio": round(krono_precio, 1)
        }
    
    def _score_rendimiento(self, m):
        """
        Calcula puntuación de rendimiento y potencia
        
        Incluye:
        - HP y RPM de potencia
        - Torque y RPM de torque
        - Cilindraje
        - Velocidad máxima
        - Sistema de frenos (delantero y trasero)
        - ABS
        - Transmisión
        - Caja de cambios
        
        Máximo teórico: ~120 puntos
        """
        score = 0
        score += self.db.get_score("hp", m.get("hp_rango"))
        score += self.db.get_score("hp_rpm", m.get("hp_rpm_rango"))
        score += self.db.get_score("torque", m.get("torque_rango"))
        score += self.db.get_score("torque_rpm", m.get("torque_rpm_rango"))
        score += self.db.get_score("cilindrada", m.get("cilindraje_rango"))
        score += self.db.get_score("top_speed", m.get("top_speed_rango"))
        score += self.db.get_score("freno_del", m.get("freno_del"))
        score += self.db.get_score("freno_tras", m.get("freno_tras"))
        score += self.db.get_score("abs", m.get("abs"))
        score += self.db.get_score("transmision", m.get("transmision"))
        score += self.db.get_score("caja", m.get("tipo_caja"))
        return score
    
    def _score_consumo(self, m):
        """
        Calcula puntuación de consumo y autonomía
        
        Incluye:
        - Consumo de combustible
        - Capacidad del tanque
        
        Máximo teórico: ~40 puntos
        """
        score = 0
        score += self.db.get_score("consumo", m.get("consumo_rango"))
        score += self.db.get_score("tanque", m.get("tanque_rango"))
        return score
    
    def _score_viajes(self, m):
        """
        Calcula puntuación de viajes y comodidad
        
        Incluye:
        - Suspensión delantera y trasera
        - Altura de asiento
        - Parabrisas ajustable
        - Peso
        - Velocidad crucero
        - Modos de manejo
        
        Máximo teórico: ~60 puntos
        """
        score = 0
        score += self.db.get_score("susp_del", m.get("susp_del"))
        score += self.db.get_score("susp_tras", m.get("susp_tras"))
        score += self.db.get_score("asiento", m.get("altura_asiento_rango"))
        score += self.db.get_score("parabrisas", m.get("parabrisas"))
        score += self.db.get_score("peso", m.get("peso_rango"))
        score += self.db.get_score("vel_crucero", m.get("vel_crucero_rango"))
        score += self.db.get_score("modos", m.get("modos_rango"))
        return score
    
    def _score_diseno(self, m):
        """
        Calcula puntuación de diseño y materiales
        
        Incluye:
        - Iluminación (LED/Halógena)
        - Pantalla (Digital/Analógica)
        - Calidad de neumáticos
        
        Máximo teórico: ~30 puntos
        """
        score = 0
        score += self.db.get_score("faro", m.get("iluminacion"))
        score += self.db.get_score("pantalla", m.get("pantalla"))
        score += self.db.get_score("neumaticos", m.get("neumaticos"))
        return score
    
    def _score_confiabilidad(self, m):
        """
        Calcula puntuación de confiabilidad
        
        Incluye:
        - Puntuación de marca (basada en historial)
        - Penalizaciones por fallos comunes reportados
        
        Máximo teórico: ~60 puntos (dependiendo de la marca)
        """
        marca = m.get("marca", "").lower()
        puntaje_marca = self.db.get_marca_score(marca)
        
        # Aplicar penalizaciones por fallos
        fallos = m.get("fallos_lista", [])
        penalizacion_total = sum(abs(self.db.get_penalizacion(f)) for f in fallos)
        
        return max(0, puntaje_marca - penalizacion_total)
    
    def _norm(self, valor, maximo):
        """
        Normaliza un valor a escala 0-100
        
        Args:
            valor: Valor a normalizar
            maximo: Valor máximo del rango
            
        Returns:
            float entre 0 y 100
        """
        if valor <= 0:
            return 0
        if valor >= maximo:
            return 100
        return (valor / maximo) * 100
    
    def _ajuste_precio(self, calidad, precio, promedio):
        """
        Ajusta la puntuación de calidad según el precio
        
        Si la moto cuesta más que el promedio de su categoría,
        la puntuación baja proporcionalmente. Si cuesta menos,
        la puntuación sube.
        
        Args:
            calidad: Puntuación de calidad (0-100)
            precio: Precio de la moto
            promedio: Precio promedio de la categoría
            
        Returns:
            float entre 0 y 100 (puntuación ajustada)
        """
        if precio <= 0 or promedio <= 0:
            return calidad
        
        ratio = precio / promedio
        
        # Si cuesta el doble del promedio, el score se divide entre 2
        # Si cuesta la mitad, el score se multiplica por 2 (con límite de 100)
        return max(0, min(100, calidad / ratio))
    
    def comparar_motos(self, motos, precio_promedio_categoria=10000000):
        """
        Compara múltiples motos y las ordena por KronoScore Precio
        
        Args:
            motos: Lista de instancias de Moto
            precio_promedio_categoria: Precio promedio para ajuste
            
        Returns:
            Lista de diccionarios con moto y sus scores, ordenada por krono_precio
        """
        resultados = []
        
        for moto in motos:
            scores = self.calcular(moto, precio_promedio_categoria)
            resultados.append({
                'moto': moto,
                'scores': scores
            })
        
        # Ordenar por Krono Precio (de mayor a menor)
        resultados.sort(key=lambda x: x['scores']['krono_precio'], reverse=True)
        
        return resultados
    
    def analizar_categoria(self, motos_categoria, precio_promedio=None):
        """
        Analiza todas las motos de una categoría y calcula estadísticas
        
        Args:
            motos_categoria: Lista de motos de la misma categoría
            precio_promedio: Si no se provee, se calcula automáticamente
            
        Returns:
            dict con estadísticas de la categoría
        """
        if not motos_categoria:
            return None
        
        # Calcular precio promedio si no se provee
        if precio_promedio is None:
            precios = [m.info.precio for m in motos_categoria if m.info.precio]
            precio_promedio = sum(precios) / len(precios) if precios else 10000000
        
        # Calcular scores de todas las motos
        scores_list = []
        for moto in motos_categoria:
            scores = self.calcular(moto, precio_promedio)
            scores_list.append({
                'moto': moto,
                'scores': scores
            })
        
        # Calcular promedios
        avg_calidad = sum(s['scores']['krono_calidad'] for s in scores_list) / len(scores_list)
        avg_precio_score = sum(s['scores']['krono_precio'] for s in scores_list) / len(scores_list)
        
        # Encontrar mejor y peor
        mejor = max(scores_list, key=lambda x: x['scores']['krono_precio'])
        peor = min(scores_list, key=lambda x: x['scores']['krono_precio'])
        
        return {
            'total_motos': len(motos_categoria),
            'precio_promedio': precio_promedio,
            'krono_calidad_promedio': round(avg_calidad, 1),
            'krono_precio_promedio': round(avg_precio_score, 1),
            'mejor_moto': {
                'info': mejor['moto'].info.to_dict(),
                'scores': mejor['scores']
            },
            'peor_moto': {
                'info': peor['moto'].info.to_dict(),
                'scores': peor['scores']
            },
            'todas_motos': scores_list
        }
    
    def recomendar_por_presupuesto(self, motos, presupuesto_max, top_n=5):
        """
        Recomienda las mejores motos dentro de un presupuesto
        
        Args:
            motos: Lista de motos a evaluar
            presupuesto_max: Presupuesto máximo del usuario
            top_n: Número de recomendaciones a retornar
            
        Returns:
            Lista de las top N motos ordenadas por krono_precio
        """
        # Filtrar por presupuesto
        en_presupuesto = [m for m in motos if m.info.precio and m.info.precio <= presupuesto_max]
        
        if not en_presupuesto:
            return []
        
        # Calcular precio promedio de las que están en presupuesto
        precios = [m.info.precio for m in en_presupuesto]
        precio_prom = sum(precios) / len(precios)
        
        # Calcular scores
        resultados = self.comparar_motos(en_presupuesto, precio_prom)
        
        # Retornar top N
        return resultados[:top_n]


# ============================================================
# FUNCIONES AUXILIARES PARA USAR EN OTROS MÓDULOS
# ============================================================

def calcular_precio_promedio_categoria(db, tipo_moto):
    """
    Calcula el precio promedio de una categoría de motos
    
    Args:
        db: Instancia de DB
        tipo_moto: Tipo de moto (naked, sport, etc.)
        
    Returns:
        float con el precio promedio
    """
   
    
    motos = db.listar_motos()
    motos_tipo = [m for m in motos if m['tipo'].lower() == tipo_moto.lower()]
    
    precios = []
    for moto_data in motos_tipo:
        moto = crear_moto(db, moto_data['id'])
        if moto and moto.info.precio:
            precios.append(moto.info.precio)
    
    if precios:
        return sum(precios) / len(precios)
    else:
        return 10000000  # Valor por defecto


def clasificar_krono(score):
    """
    Clasifica una moto según su KronoScore
    
    Args:
        score: Puntuación krono_precio o krono_calidad
        
    Returns:
        str con la clasificación
    """
    if score >= 85:
        return "⭐⭐⭐⭐⭐ EXCEPCIONAL - Premium en su categoría"
    elif score >= 75:
        return "⭐⭐⭐⭐ EXCELENTE - Muy recomendada"
    elif score >= 65:
        return "⭐⭐⭐ BUENA - Relación calidad-precio equilibrada"
    elif score >= 50:
        return "⭐⭐ ACEPTABLE - Cumple expectativas básicas"
    else:
        return "⭐ LIMITADA - Considerar otras opciones"
 