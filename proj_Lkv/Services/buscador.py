class Buscador:
    def __init__(self, db):
        self.criterios_activos = {}
        self.historial_busquedas = []
        self.resultados_actuales = []
        self.ordenamiento_actual = ""
        self.paginacion_actual = 0
        self.favoritos = []

    def buscar_modelo(self, nombre):
        pass

    def filtrar_por_tipo(self, tipo):
        pass

    def filtrar_por_precio(self, min, max):
        pass

    def filtrar_por_cilindraje(self, min, max):
        pass

    def ordenar_por(self, criterio):
        pass

    def mostrar_resultados(self):
        pass

    def limpiar_busqueda(self):
        pass
