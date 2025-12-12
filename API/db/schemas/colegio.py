def colegio_schema(colegio) -> dict:
    return {
        "id": str(colegio ["_id"]),
        "nombre": colegio ["nombre"],
        "distrito": colegio ["distrito"],
        "tipo": colegio ["tipo"],
        "direccion": colegio ["direccion"]
    }

def colegios_schema(colegios) -> list:
    return [colegio_schema(colegio) for colegio in colegios]