from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
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

# Funciones de acceso a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cancion(db, cancion_id: int):
    cancion = db.query(Cancion).filter(Cancion.id == cancion_id).first()
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion

def create_cancion(db, cancion: CancionPydantic):
    db_cancion = Cancion(**cancion.dict())
    db.add(db_cancion)
    db.commit()
    db.refresh(db_cancion)
    return db_cancion

def update_cancion(db, cancion_id: int, cancion: CancionPydantic):
    db_cancion = get_cancion(db, cancion_id)
    for key, value in cancion.dict().items():
        setattr(db_cancion, key, value)
    db.commit()
    db.refresh(db_cancion)
    return db_cancion

def delete_cancion(db, cancion_id: int):
    db_cancion = get_cancion(db, cancion_id)
    db.delete(db_cancion)
    db.commit()
    return {"mensaje": "Canción eliminada exitosamente"}

# Rutas
@app.post("/canciones/", response_model=CancionPydantic)
def crear_cancion(cancion: CancionPydantic, db: Session = Depends(get_db)):
    return create_cancion(db, cancion)

@app.get("/canciones/{cancion_id}", response_model=CancionPydantic)
def obtener_cancion(cancion_id: int, db: Session = Depends(get_db)):
    return get_cancion(db, cancion_id)

@app.put("/canciones/{cancion_id}", response_model=CancionPydantic)
def actualizar_cancion(cancion_id: int, cancion: CancionPydantic, db: Session = Depends(get_db)):
    return update_cancion(db, cancion_id, cancion)

@app.delete("/canciones/{cancion_id}")
def eliminar_cancion(cancion_id: int, db: Session = Depends(get_db)):
    return delete_cancion(db, cancion_id)
