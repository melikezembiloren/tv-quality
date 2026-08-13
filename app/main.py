from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.presentation.api.v1.routers.tv_router import router as tv_router
from app.presentation.api.v1.routers.audit_router import router as audit_router
from app.presentation.api.v1.routers.quality_dashboard_router import router as quality_dashboard_router
from app.presentation.api.v1.routers.reference_data_router import router as reference_data_router
from app.presentation.api.v1.routers.inspection_router import router as inspection_router
from app.presentation.api.v1.routers.defect_dashboard_router import router as defect_dashboard_router

app = FastAPI(title="QualiTV API", version="0.1.0")

app.include_router(tv_router, prefix="/api/v1")
app.include_router(audit_router, prefix="/api/v1")
app.include_router(quality_dashboard_router, prefix="/api/v1")
app.include_router(reference_data_router, prefix="/api/v1")
app.include_router(inspection_router, prefix="/api/v1")
app.include_router(defect_dashboard_router, prefix="/api/v1")

STATIC_DIR = Path(__file__).resolve().parent / "presentation" / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/quality-dashboard")
def quality_dashboard_page():
    """Kalite dashboard'unun kendi sayfası — üretim/TV ekranlarından ayrı, bağımsız bir rota."""
    return FileResponse(STATIC_DIR / "quality-dashboard.html")


@app.get("/audits/new")
def audit_form_page():
    """Denetim + bulgu girişi için form ekranı."""
    return FileResponse(STATIC_DIR / "audit-form.html")


@app.get("/inspections/new")
def inspection_form_page():
    """TV kontrolü (OK/Hatalı) giriş ekranı — üretim hattından bağımsız."""
    return FileResponse(STATIC_DIR / "inspection-form.html")


@app.get("/defect-dashboard")
def defect_dashboard_page():
    """Hata analizi dashboard'u — günlük/haftalık/aylık trend, audit modülünden ayrı."""
    return FileResponse(STATIC_DIR / "defect-dashboard.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}
