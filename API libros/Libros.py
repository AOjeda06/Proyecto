from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos para un libro
class Libro(BaseModel):
    id: int
    titulo: str
    idAutor: int
    isbn: str
    numPaginas: int

# Lista simulada de libros
LibroList = [
    Libro(id=1, titulo="Don Quijote de la Mancha", idAutor=1, isbn="978-3-16-148410-0", numPaginas=863),
    Libro(id=2, titulo="La casa de Bernarda Alba", idAutor=2, isbn="978-1-23-456789-0", numPaginas=112),
    Libro(id=3, titulo="Cantares Gallegos", idAutor=3, isbn="978-0-12-345678-9", numPaginas=78)
]

# Endpoint para obtener todos los libros
@app.get("/libros")
def get_libros():
    return get_all_libros()

# Endpoint para obtener un libro por su ID
@app.get("/libros/{id}")
def get_libro(id: int):
    libro = find_libro_by_id(id)
    if libro:
        return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Endpoint para crear un nuevo libro
@app.post("/libros", status_code=201, response_model=Libro)
def create_libro(libro: Libro):
    libro.id = next_id()
    add_libro(libro)
    return libro

# Endpoint para modificar un libro existente
@app.put("/libros/{id}", response_model=Libro)
def modify_libro(id: int, libro: Libro): 
    updated = update_libro(id, libro)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Endpoint para eliminar un libro por su ID
@app.delete("/libros/{id}", status_code=204)
def delete_libro(id: int):
    removed = remove_libro(id)
    if removed:
        return {}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

#region Funciones

#Función para generar el siguiente ID disponible
def next_id():
    if LibroList:
        return (max(libro.id for libro in LibroList) + 1)
    return 1

#Funcion para obtener todos los libros
def get_all_libros():
    return LibroList

#Función para buscar un libro por su ID
#Función para buscar un libro por su ID
def find_libro_by_id(id: int):
    resultados = [libro for libro in LibroList if libro.id == id]
    return resultados[0] if resultados else None

#Función para añadir un nuevo libro
def add_libro(libro: Libro):
    LibroList.append(libro)

#Función para actualizar un libro existente
def update_libro(id: int, libro: Libro):
    for index, saved_libro in enumerate(LibroList):
        if saved_libro.id == id:
            libro.id = id
            LibroList[index] = libro
            return libro
    return None

#Función para eliminar un libro por su ID
def remove_libro(id: int):
    for saved_libro in LibroList:
        if saved_libro.id == id:
             LibroList.remove(saved_libro)
             return True
    return False
#endregion