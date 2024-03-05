from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos MySQL con SQLAlchemy
SQLALCHEMY_DATABASE_URL = "mysql://root:@localhost/api"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definición de la clase base para las tablas
Base = declarative_base()

# Definición del modelo de datos para la canción utilizando SQLAlchemy
class Cancion(Base):
    __tablename__ = "canciones"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    artista = Column(String, index=True)
    fecha_lanzamiento = Column(String)
    genero = Column(String)

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Rutas CRUD
@app.post("/canciones/")
def crear_cancion(cancion: Cancion):
    db = SessionLocal()
    db.add(cancion)
    db.commit()
    db.close()
    return {"mensaje": "Canción creada exitosamente"}

@app.get("/canciones/{cancion_id}")
def obtener_cancion(cancion_id: int):
    db = SessionLocal()
    cancion = db.query(Cancion).filter(Cancion.id == cancion_id).first()
    db.close()
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion

@app.put("/canciones/{cancion_id}")
def actualizar_cancion(cancion_id: int, cancion: Cancion):
    db = SessionLocal()
    db_query = db.query(Cancion).filter(Cancion.id == cancion_id)
    db_cancion = db_query.first()
    if not db_cancion:
        db.close()
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    db_query.update(cancion.dict())
    db.commit()
    db.close()
    return {"mensaje": "Canción actualizada exitosamente"}

@app.delete("/canciones/{cancion_id}")
def eliminar_cancion(cancion_id: int):
    db = SessionLocal()
    db_query = db.query(Cancion).filter(Cancion.id == cancion_id)
    db_cancion = db_query.first()
    if not db_cancion:
        db.close()
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    db_query.delete(synchronize_session=False)
    db.commit()
    db.close()
    return {"mensaje": "Canción eliminada exitosamente"}
