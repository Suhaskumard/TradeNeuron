"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.db.session import engine, get_db
from app.db.models import Base
from app.api.v1.api import router as api_router
from app.api.v1.data import router as data_router
from app.api.v1.predictions import router as predictions_router
from app.api.v1.backtest import router as backtest_router

# Create FastAPI app
app = FastAPI(
    title="TradeNeuron AI Trading API",
    description="Production-grade AI stock trading system",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# API routes
app.include_router(api_router, prefix="/api/v1")
app.include_router(data_router, prefix="/api/v1")
app.include_router(predictions_router, prefix="/api/v1")
app.include_router(backtest_router, prefix="/api/v1")

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, templates=Depends(templates)):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
"""

