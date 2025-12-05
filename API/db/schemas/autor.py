def autor_schema(autor) -> dict:
    return {
        "id": str(autor ["_id"]),
        "dni": autor ["dni"],
        "nombre": autor ["nombre"],
        "apellidos": autor ["apellidos"]}

def autores_schema(autores) -> list:
    return [autor_schema(autor) for autor in autores]