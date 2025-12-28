from fastapi import FastAPI
from .db import engine, Base
from .routes.customers import router as customers_router
from .routes.documents import router as documents_router
from .routes.questionnaire import router as questionnaire_router

app = FastAPI(title="Context-Aware System Prototype")

# Create DB tables on startup (simple prototype approach)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(customers_router, prefix="/customers", tags=["customers"])
app.include_router(documents_router, prefix="/customers", tags=["documents"])
app.include_router(questionnaire_router, prefix="/customers", tags=["questionnaire"])
