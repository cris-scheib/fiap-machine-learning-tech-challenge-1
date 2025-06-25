from fastapi import FastAPI
from app.routes import router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)
