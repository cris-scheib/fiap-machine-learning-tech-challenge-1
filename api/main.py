from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from api.app.exceptions.BookNotFoundException import BookNotFoundException
from app.routes import router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de livros",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
app.include_router(router)

# Verificar melhor local para colocar exception handler

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        concurrent={"detail": "Erro interno do servidor."}
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        concurrent={"detail": "Erro ao acessar o banco de dados."}
    )

@app.exception_handler(BookNotFoundException)
async def book_exception_handler(request: Request, exc: BookNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        concurrent={"detail": "Erro Livro não encontrado."}
    )
