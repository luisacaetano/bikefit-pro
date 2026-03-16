"""
Configurações da aplicação BikeFit Pro

Referências científicas para ângulos:
- Holmes et al. (1994): Método original de flexão do joelho (25-35° estático)
- Bini & Hume (2020): Ranges dinâmicos corrigidos (33-43° dinâmico)
- Bini et al. (2023): Diferenças estático vs dinâmico
- Martínez & Pérez (2025): Correlação flexão >40° com dor
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Dict, Any


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

    # =========================================================================
    # ÂNGULOS DE REFERÊNCIA - BASEADOS EM LITERATURA CIENTÍFICA
    # =========================================================================
    #
    # Nomenclatura:
    # - knee_flexion_bdc: Flexão do joelho no Bottom Dead Center (6h do pedal)
    # - knee_extension: Ângulo de extensão do joelho (180° - flexão)
    #
    # Modos:
    # - static: Ciclista parado na bike (medição tradicional)
    # - dynamic: Ciclista pedalando (vídeo em tempo real)
    #
    # Diferenças estático vs dinâmico (Bini et al. 2023):
    # - Joelho: +8° ± 2° no modo dinâmico
    # - Quadril: +5° ± 1° no modo dinâmico
    # - Tornozelo: +9° ± 2° no modo dinâmico
    # =========================================================================

    # Ângulos de referência por MODO DE ANÁLISE
    angles_reference_static: dict = {
        # Joelho no BDC - Método Holmes (1994)
        # Flexão ideal: 25-35° | Extensão equivalente: 145-155°
        "knee_flexion_bdc": {"min": 25, "max": 35, "optimal": 30},
        "knee_extension": {"min": 145, "max": 155, "optimal": 150},

        # Quadril (shoulder-hip-knee)
        "hip": {"min": 40, "max": 50, "optimal": 45},

        # Tornozelo
        "ankle": {"min": 90, "max": 110, "optimal": 100},

        # Tronco em relação à horizontal
        "trunk": {"min": 40, "max": 55, "optimal": 47},

        # Cotovelo (shoulder-elbow-wrist)
        "elbow": {"min": 150, "max": 170, "optimal": 160},
    }

    angles_reference_dynamic: dict = {
        # Joelho no BDC - Bini & Hume (2020) - corrigido para dinâmico
        # Flexão ideal: 33-43° (+8° vs estático)
        "knee_flexion_bdc": {"min": 33, "max": 43, "optimal": 38},
        "knee_extension": {"min": 137, "max": 147, "optimal": 142},

        # Quadril - corrigido (+5° vs estático)
        "hip": {"min": 35, "max": 45, "optimal": 40},

        # Tornozelo - corrigido (+9° vs estático, invertido pois mede dorsiflexão)
        "ankle": {"min": 81, "max": 101, "optimal": 91},

        # Tronco - pouca diferença
        "trunk": {"min": 40, "max": 55, "optimal": 47},

        # Cotovelo - pouca diferença
        "elbow": {"min": 150, "max": 170, "optimal": 160},
    }

    # Ângulos por MODALIDADE DE CICLISMO
    # Cada modalidade tem diferentes prioridades (conforto vs aerodinâmica)
    angles_by_discipline: dict = {
        "road": {
            "description": "Ciclismo de estrada - equilíbrio conforto/performance",
            "trunk": {"min": 40, "max": 50, "optimal": 45},
            "hip": {"min": 40, "max": 50, "optimal": 45},
        },
        "mtb": {
            "description": "Mountain Bike - posição mais ereta para controle",
            "trunk": {"min": 50, "max": 65, "optimal": 57},
            "hip": {"min": 45, "max": 55, "optimal": 50},
        },
        "triathlon": {
            "description": "Triathlon/TT - máxima aerodinâmica",
            "trunk": {"min": 30, "max": 40, "optimal": 35},
            "hip": {"min": 35, "max": 45, "optimal": 40},
        },
        "gravel": {
            "description": "Gravel - similar a road, ligeiramente mais ereto",
            "trunk": {"min": 42, "max": 52, "optimal": 47},
            "hip": {"min": 42, "max": 52, "optimal": 47},
        },
        "urban": {
            "description": "Urbano/Commute - máximo conforto",
            "trunk": {"min": 60, "max": 80, "optimal": 70},
            "hip": {"min": 50, "max": 60, "optimal": 55},
        },
    }

    # Limites de alerta (quando o ângulo indica risco de lesão)
    injury_risk_thresholds: dict = {
        # Flexão do joelho >40° no BDC correlaciona com dor (Martínez & Pérez 2025)
        "knee_flexion_bdc_max": 40,
        # Extensão excessiva pode causar sobrecarga no joelho
        "knee_extension_max": 160,
        # Tronco muito baixo pode causar dor cervical/lombar
        "trunk_min": 30,
    }

    # Manter compatibilidade com código legado
    @property
    def angles_reference(self) -> dict:
        """Retorna referências dinâmicas como padrão (análise em tempo real)"""
        return self.angles_reference_dynamic

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações"""
    return Settings()


def get_angles_for_mode(mode: str = "dynamic") -> dict:
    """
    Retorna ângulos de referência para o modo especificado.

    Args:
        mode: "static" ou "dynamic"

    Returns:
        Dicionário com ângulos de referência
    """
    settings = get_settings()
    if mode == "static":
        return settings.angles_reference_static
    return settings.angles_reference_dynamic


def get_angles_for_discipline(discipline: str = "road") -> dict:
    """
    Retorna ângulos específicos para a modalidade de ciclismo.

    Args:
        discipline: "road", "mtb", "triathlon", "gravel", "urban"

    Returns:
        Dicionário com ângulos específicos da modalidade
    """
    settings = get_settings()
    return settings.angles_by_discipline.get(discipline, settings.angles_by_discipline["road"])
