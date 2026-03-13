"""
Rotas de Análise Postural
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
import tempfile
import os

from app.core.pose_detector import PoseDetector
from app.core.angle_calculator import AngleCalculator
from app.core.recommendations import RecommendationEngine
from app.services.pdf_generator import PDFGenerator

router = APIRouter()

# Instâncias dos serviços
pose_detector = PoseDetector()
angle_calculator = AngleCalculator()
recommendation_engine = RecommendationEngine()


@router.post("/frame")
async def analisar_frame(file: UploadFile = File(...)):
    """
    Analisa um único frame/imagem
    Retorna keypoints, ângulos e recomendações
    """
    # Ler imagem
    contents = await file.read()

    # Detectar pose
    keypoints = pose_detector.detect(contents)

    if not keypoints:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível detectar pose na imagem"
        )

    # Calcular ângulos
    angles = angle_calculator.calculate_all(keypoints)

    # Gerar recomendações
    recommendations = recommendation_engine.analyze(angles)

    return {
        "keypoints": keypoints,
        "angles": angles,
        "recommendations": recommendations
    }


@router.get("/referencias")
async def obter_angulos_referencia():
    """Retorna os ângulos de referência configurados"""
    from app.config import get_settings
    settings = get_settings()
    return settings.angles_reference


@router.post("/relatorio/{sessao_id}")
async def gerar_relatorio_pdf(sessao_id: int):
    """
    Gera relatório PDF de uma sessão
    """
    # TODO: Buscar dados da sessão no banco
    # Por enquanto, retorna dados de exemplo

    pdf_generator = PDFGenerator()

    # Dados de exemplo
    dados_sessao = {
        "paciente": "João Silva",
        "data": "13/03/2026",
        "angulos_antes": {
            "knee_extension": 138,
            "knee_flexion": 78,
            "hip": 52,
        },
        "angulos_depois": {
            "knee_extension": 146,
            "knee_flexion": 70,
            "hip": 46,
        },
        "ajustes": {
            "selim": "+2cm",
            "guidao": "sem alteração"
        }
    }

    # Gerar PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_path = tmp.name
        pdf_generator.generate(dados_sessao, pdf_path)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"bikefit_sessao_{sessao_id}.pdf"
    )
