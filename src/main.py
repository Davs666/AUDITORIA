from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

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
    fecha_lanzamiento = Column(String, index=True)
    genero = Column(String, index=True)

# Definición del modelo Pydantic para la Cancion
class CancionPydantic(BaseModel):
    id: int
    titulo: str
    artista: str
    fecha_lanzamiento: str
    genero: str

# Inicialización de la aplicación FastAPI
app = FastAPI()

# Ruta para crear una canción
@app.post("/canciones/", response_model=CancionPydantic)
def crear_cancion(cancion: CancionPydantic):
    db = SessionLocal()
    db_cancion = Cancion(**cancion.dict())
    db.add(db_cancion)
    db.commit()
    db.refresh(db_cancion)
    db.close()
    return db_cancion

# Ruta para obtener una canción por su ID
@app.get("/canciones/{cancion_id}", response_model=CancionPydantic)
def obtener_cancion(cancion_id: int):
    db = SessionLocal()
    cancion = db.query(Cancion).filter(Cancion.id == cancion_id).first()
    db.close()
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion

# Ruta para actualizar una canción por su ID
@app.put("/canciones/{cancion_id}", response_model=CancionPydantic)
def actualizar_cancion(cancion_id: int, cancion: CancionPydantic):
    db = SessionLocal()
    db_cancion = db.query(Cancion).filter(Cancion.id == cancion_id).first()
    if not db_cancion:
        db.close()
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    for key, value in cancion.dict().items():
        setattr(db_cancion, key, value)
    db.commit()
    db.refresh(db_cancion)
    db.close()
    return db_cancion

# Ruta para eliminar una canción por su ID
@app.delete("/canciones/{cancion_id}")
def eliminar_cancion(cancion_id: int):
    db = SessionLocal()
    db_cancion = db.query(Cancion).filter(Cancion.id == cancion_id).first()
    if not db_cancion:
        db.close()
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    db.delete(db_cancion)
    db.commit()
    db.close()
    return {"mensaje": "Canción eliminada exitosamente"}
