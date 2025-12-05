def libro_schema(libro) -> dict:
    return {
        "id": str(libro ["_id"]),
        "titulo": libro ["titulo"],
        "idAutor": str(libro ["idAutor"]),
        "isbn": libro ["isbn"],
        "numPaginas": libro ["numPaginas"]}
    
def libros_schema(libros) -> list:
    return [libro_schema(libro) for libro in libros]