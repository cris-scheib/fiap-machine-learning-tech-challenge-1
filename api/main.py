import logging
import sys
import yaml
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions.custom_exceptions import BookNotFoundException, BookNotFoundInRangePriceException, DatabaseException
from app.routes import router
from app.core.database import Base, engine

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

logger.info("Initializing database...")
Base.metadata.create_all(bind=engine)
logger.info("Database initialized successfully")

def load_openapi():
    BASE_DIR = Path(__file__).resolve().parent
    with open(BASE_DIR / "openapi.yaml", encoding='utf-8') as f:
        return yaml.safe_load(f)

               
app = FastAPI(
    title="Books API",
    description="API for book management",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    contact={
        "name": "Development Team",
        "email": "contact@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.openapi_schema = load_openapi()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Registering API routes...")
app.include_router(router)
logger.info("Routes registered successfully")


#@app.exception_handler(AppException)
#async def generic_exception_handler(request: Request, exc: AppException):
#    status_codes = {
#        "BOOK_NOT_FOUND": 404,
#        "USER_ALREADY_EXISTS": 409,  # 409 Conflict
#        "INVALID_CREDENTIALS": 401,
#        "AUTHENTICATION_FAILED": 401
#    }

#    status_code = status_codes.get(exc.error_code, 400)  # 400 Bad Request como padrão
#    return JSONResponse(
#        status_code=status_code,
#        content=exc.message,
#    )

@app.exception_handler(DatabaseException)
async def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error accessing the database."}
    )

@app.exception_handler(BookNotFoundException)
async def book_exception_handler(request: Request, exc: BookNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": exc.message,
        }
    )

@app.exception_handler(BookNotFoundInRangePriceException)
async def book_exception_handler(request: Request, exc: BookNotFoundInRangePriceException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": exc.message,
        }
    )