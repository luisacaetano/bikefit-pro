"""
Configurações da aplicação BikeFit Pro
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configurações carregadas de variáveis de ambiente"""

    # App
    app_name: str = "BikeFit Pro"
    app_version: str = "1.0.0"
    debug: bool = True

    # Database
    database_url: str = "postgresql://bikefit:bikefit123@localhost:5432/bikefit_pro"

    # Auth
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 horas

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Pose Detection
    yolo_model: str = "yolov8n-pose.pt"  # nano model (mais rápido)
    confidence_threshold: float = 0.5

    # Ângulos de referência (em graus)
    angles_reference: dict = {
        "knee_extension": {"min": 140, "max": 150, "optimal": 145},
        "knee_flexion": {"min": 65, "max": 75, "optimal": 70},
        "hip": {"min": 40, "max": 50, "optimal": 45},
        "ankle": {"min": 90, "max": 110, "optimal": 100},
        "trunk": {"min": 40, "max": 55, "optimal": 47},
        "elbow": {"min": 150, "max": 170, "optimal": 160},
    }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações"""
    return Settings()
