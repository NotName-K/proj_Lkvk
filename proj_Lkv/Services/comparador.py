def comp_gen(motoA, motoB):
    critA = motoA.obtener_criterios_comparacion()
    critB = motoB.obtener_criterios_comparacion()

    comunes = set(critA.keys()) & set(critB.keys())
    comunes = [c for c in comunes if c != "categoria"]

    comparacion = {}

    for c in comunes:
        a = critA[c]
        b = critB[c]
        comparacion[c] = {
            "motoA": a,
            "motoB": b,
            "mejor": mejor_gen(c, a, b)
        }

    return comparacion


def mejor_gen(criterio, a, b):
    if a is None or b is None:
        return None

    mayor = {
        "potencia", "top_speed", "velocidad_maxima",
        "autonomia", "espacio_baul", "capacidad_maletas",
        "cilindraje"
    }

    menor = {
        "peso", "aceleracion", "aceleracion_0a100",
        "tiempo_carga"
    }

    if criterio in mayor:
        if a > b: return "A"
        if b > a: return "B"
        return "Igual"

    if criterio in menor:
        if a < b: return "A"
        if b < a: return "B"
        return "Igual"

    return None


def krono_compare(motoA, motoB):
    tipoA = motoA.info.tipo.lower()
    tipoB = motoB.info.tipo.lower()

    if tipoA != tipoB:
        raise ValueError("Diferente tipo.")

    critA = motoA.obtener_criterios_comparacion()
    critB = motoB.obtener_criterios_comparacion()

    comparacion = {}

    for c in critA.keys():
        if c == "categoria":
            continue

        a = critA[c]
        b = critB[c]

        comparacion[c] = {
            "motoA": a,
            "motoB": b,
            "mejor": krono_choice(c, a, b, tipoA)
        }

    return comparacion


def krono_choice(criterio, a, b, tipo):
    if a is None or b is None:
        return None

    if tipo == "sport":
        if criterio in {"potencia", "velocidad_maxima"}:
            return _max(a, b)
        if criterio in {"aceleracion", "aceleracion_0a100"}:
            return _min(a, b)
        if criterio == "peso":
            return _min(a, b)

    if tipo == "touring":
        if criterio == "autonomia":
            return _max(a, b)
        if criterio == "capacidad_maletas":
            return _max(a, b)
        if criterio == "altura_asiento":
            return _min(a, b)

    if tipo == "scooter":
        if criterio == "espacio_baul":
            return _max(a, b)
        if criterio == "consumo":
            return _max(a, b)
        if criterio == "peso":
            return _min(a, b)

    if tipo in {"adventure", "doble pps"}:
        if criterio == "autonomia":
            return _max(a, b)
        if criterio == "recorrido_suspension":
            return _max(a, b)
        if criterio == "peso":
            return _min(a, b)

    if tipo == "electric":
        if criterio == "autonomia":
            return _max(a, b)
        if criterio == "tiempo_carga":
            return _min(a, b)
        if criterio == "eficiencia":
            return _max(a, b)

    return None


def _max(a, b):
    if a > b: return "A"
    if b > a: return "B"
    return "Igual"


def _min(a, b):
    if a < b: return "A"
    if b < a: return "B"
    return "Igual"
