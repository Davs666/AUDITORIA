import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="api"
)

# Modelo de datos para la canción
class Cancion(BaseModel):
    titulo: str
    artista: str
    fecha_lanzamiento: str
    genero: str

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Rutas CRUD
@app.post("/canciones/")
def crear_cancion(cancion: Cancion):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO canciones (titulo, artista, fecha_lanzamiento, genero) VALUES (%s, %s, %s, %s)",
        (cancion.titulo, cancion.artista, cancion.fecha_lanzamiento, cancion.genero)
    )
    conn.commit()
    cursor.close()
    return {"mensaje": "Canción creada exitosamente"}

@app.get("/canciones/{cancion_id}")
def obtener_cancion(cancion_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM canciones WHERE id=%s", (cancion_id,))
    cancion = cursor.fetchone()
    cursor.close()
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return {"id": cancion[0], "titulo": cancion[1], "artista": cancion[2], "fecha_lanzamiento": cancion[3], "genero": cancion[4]}

@app.put("/canciones/{cancion_id}")
def actualizar_cancion(cancion_id: int, cancion: Cancion):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE canciones SET titulo=%s, artista=%s, fecha_lanzamiento=%s, genero=%s WHERE id=%s",
        (cancion.titulo, cancion.artista, cancion.fecha_lanzamiento, cancion.genero, cancion_id)
    )
    conn.commit()
    cursor.close()
    return {"mensaje": "Canción actualizada exitosamente"}

@app.delete("/canciones/{cancion_id}")
def eliminar_cancion(cancion_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM canciones WHERE id=%s", (cancion_id,))
    conn.commit()
    cursor.close()
    return {"mensaje": "Canción eliminada exitosamente"}
