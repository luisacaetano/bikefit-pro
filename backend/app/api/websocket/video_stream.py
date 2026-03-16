"""
WebSocket para streaming de vídeo em tempo real
"""
import cv2
import base64
import json
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Optional, Dict, Any

from app.core.pose_detector import PoseDetector
from app.core.angle_calculator import AngleCalculator
from app.core.recommendations import RecommendationEngine

router = APIRouter()


def draw_spine_on_frame(frame: np.ndarray, spine_data: Dict[str, Any]) -> np.ndarray:
    """
    Desenha os 3 pontos da coluna e a linha de curvatura no frame.

    Args:
        frame: Frame de vídeo
        spine_data: Dados da coluna calculados pelo AngleCalculator

    Returns:
        Frame com a coluna desenhada
    """
    if not spine_data:
        return frame

    # Cores
    SPINE_COLOR = (0, 255, 255)  # Amarelo (BGR)
    SPINE_LINE_COLOR = (0, 200, 200)  # Amarelo escuro
    TEXT_COLOR = (255, 255, 255)  # Branco
    KYPHOSIS_COLOR = (0, 0, 255)  # Vermelho
    LORDOSIS_COLOR = (255, 0, 0)  # Azul
    NEUTRAL_COLOR = (0, 255, 0)  # Verde

    # Extrair pontos
    top = spine_data.get("spine_top")
    mid = spine_data.get("spine_mid")
    low = spine_data.get("spine_low")

    if not all([top, mid, low]):
        return frame

    # Converter para inteiros
    pt_top = (int(top["x"]), int(top["y"]))
    pt_mid = (int(mid["x"]), int(mid["y"]))
    pt_low = (int(low["x"]), int(low["y"]))

    # Determinar cor baseado no tipo de curvatura
    curvature_type = spine_data.get("curvature_type", "neutral")
    if curvature_type == "kyphosis":
        curve_color = KYPHOSIS_COLOR
    elif curvature_type == "lordosis":
        curve_color = LORDOSIS_COLOR
    else:
        curve_color = NEUTRAL_COLOR

    # Desenhar linha da coluna (conectando os 3 pontos)
    cv2.line(frame, pt_top, pt_mid, SPINE_LINE_COLOR, 2)
    cv2.line(frame, pt_mid, pt_low, SPINE_LINE_COLOR, 2)

    # Desenhar linha reta de referência (tracejada)
    # Linha pontilhada de top a low para comparação
    draw_dashed_line(frame, pt_top, pt_low, (128, 128, 128), 1)

    # Desenhar círculos nos pontos da coluna
    cv2.circle(frame, pt_top, 8, SPINE_COLOR, -1)
    cv2.circle(frame, pt_top, 10, curve_color, 2)

    cv2.circle(frame, pt_mid, 10, curve_color, -1)
    cv2.circle(frame, pt_mid, 12, (255, 255, 255), 2)

    cv2.circle(frame, pt_low, 8, SPINE_COLOR, -1)
    cv2.circle(frame, pt_low, 10, curve_color, 2)

    # Labels nos pontos
    cv2.putText(frame, "C7", (pt_top[0] + 15, pt_top[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, TEXT_COLOR, 1)
    cv2.putText(frame, "T12", (pt_mid[0] + 15, pt_mid[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, TEXT_COLOR, 1)
    cv2.putText(frame, "L5", (pt_low[0] + 15, pt_low[1]),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, TEXT_COLOR, 1)

    # Mostrar tipo de curvatura no canto
    severity = spine_data.get("curvature_severity", "normal")
    if curvature_type != "neutral":
        curvature_text = f"Coluna: {curvature_type.upper()} ({severity})"
        cv2.putText(frame, curvature_text, (10, frame.shape[0] - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, curve_color, 2)

    return frame


def draw_dashed_line(frame, pt1, pt2, color, thickness, dash_length=10):
    """Desenha uma linha tracejada"""
    dist = np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
    if dist == 0:
        return

    dashes = int(dist / dash_length)
    for i in range(0, dashes, 2):
        start = (
            int(pt1[0] + (pt2[0] - pt1[0]) * i / dashes),
            int(pt1[1] + (pt2[1] - pt1[1]) * i / dashes)
        )
        end = (
            int(pt1[0] + (pt2[0] - pt1[0]) * min(i + 1, dashes) / dashes),
            int(pt1[1] + (pt2[1] - pt1[1]) * min(i + 1, dashes) / dashes)
        )
        cv2.line(frame, start, end, color, thickness)

# Instâncias globais (compartilhadas entre conexões)
pose_detector: Optional[PoseDetector] = None
angle_calculator: Optional[AngleCalculator] = None
recommendation_engine: Optional[RecommendationEngine] = None


def get_pose_detector() -> PoseDetector:
    """Retorna instância do detector de pose (lazy loading)"""
    global pose_detector
    if pose_detector is None:
        pose_detector = PoseDetector()
    return pose_detector


def get_angle_calculator() -> AngleCalculator:
    """Retorna instância do calculador de ângulos"""
    global angle_calculator
    if angle_calculator is None:
        angle_calculator = AngleCalculator()
    return angle_calculator


def get_recommendation_engine() -> RecommendationEngine:
    """Retorna instância do motor de recomendações"""
    global recommendation_engine
    if recommendation_engine is None:
        recommendation_engine = RecommendationEngine()
    return recommendation_engine


@router.websocket("/ws/video")
async def video_stream_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket para análise de vídeo em tempo real.

    O cliente envia frames em base64 e recebe:
    - Frame processado com pose detection
    - Keypoints detectados
    - Ângulos calculados
    - Recomendações em tempo real
    """
    await websocket.accept()
    print("WebSocket conectado")

    detector = get_pose_detector()
    calculator = get_angle_calculator()
    recommender = get_recommendation_engine()

    try:
        while True:
            # Receber frame do cliente
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "error": "Invalid JSON format"
                })
                continue

            # Processar frame
            if message.get("type") == "frame":
                frame_data = message.get("data")
                side = message.get("side", "right")  # Lado a analisar
                mode = message.get("mode")  # Opcional: mudar modo por frame
                discipline = message.get("discipline")  # Opcional: mudar modalidade

                # Atualizar modo/discipline se especificado
                if mode and mode in ["static", "dynamic"]:
                    calculator.set_mode(mode)
                    recommender.set_mode(mode)
                if discipline and discipline in ["road", "mtb", "triathlon", "gravel", "urban"]:
                    calculator.set_discipline(discipline)
                    recommender.set_discipline(discipline)

                if not frame_data:
                    await websocket.send_json({
                        "error": "No frame data"
                    })
                    continue

                # Decodificar frame base64
                try:
                    # Remover prefixo data:image/... se existir
                    if "," in frame_data:
                        frame_data = frame_data.split(",")[1]

                    frame_bytes = base64.b64decode(frame_data)
                    nparr = np.frombuffer(frame_bytes, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if frame is None:
                        raise ValueError("Failed to decode frame")

                except Exception as e:
                    await websocket.send_json({
                        "error": f"Failed to decode frame: {str(e)}"
                    })
                    continue

                # Detectar pose com visualização
                keypoints, annotated_frame = detector.detect_with_visualization(frame)

                # Preparar resposta
                response = {
                    "type": "result",
                    "keypoints": keypoints,
                    "angles": None,
                    "recommendations": None,
                    "frame": None
                }

                # Se detectou keypoints, calcular ângulos
                if keypoints:
                    angles = calculator.calculate_all(keypoints, side)
                    response["angles"] = angles

                    # Desenhar pontos da coluna no frame
                    if angles.get("spine"):
                        annotated_frame = draw_spine_on_frame(annotated_frame, angles["spine"])

                    # Gerar recomendações
                    recommendations = recommender.analyze(angles)
                    response["recommendations"] = recommendations

                # Codificar frame processado
                _, buffer = cv2.imencode('.jpg', annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                response["frame"] = f"data:image/jpeg;base64,{frame_base64}"

                await websocket.send_json(response)

            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

            elif message.get("type") == "config":
                # Configurações em tempo real
                confidence = message.get("confidence")
                mode = message.get("mode")  # "static" ou "dynamic"
                discipline = message.get("discipline")  # "road", "mtb", etc.

                if confidence:
                    detector.confidence_threshold = float(confidence)

                if mode and mode in ["static", "dynamic"]:
                    calculator.set_mode(mode)
                    recommender.set_mode(mode)

                if discipline and discipline in ["road", "mtb", "triathlon", "gravel", "urban"]:
                    calculator.set_discipline(discipline)
                    recommender.set_discipline(discipline)

                await websocket.send_json({
                    "type": "config_ack",
                    "message": "Configuration updated",
                    "config": {
                        "mode": calculator.mode,
                        "discipline": calculator.discipline,
                        "confidence": detector.confidence_threshold
                    }
                })

    except WebSocketDisconnect:
        print("WebSocket desconectado")

    except Exception as e:
        print(f"Erro no WebSocket: {e}")
        try:
            await websocket.send_json({
                "error": str(e)
            })
        except Exception:
            pass


@router.websocket("/ws/capture")
async def capture_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket para captura de foto (análise única).

    Diferente do stream contínuo, esse endpoint processa um único frame
    e retorna análise completa.
    """
    await websocket.accept()
    print("WebSocket de captura conectado")

    detector = get_pose_detector()
    calculator = get_angle_calculator()
    recommender = get_recommendation_engine()

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON"})
                continue

            if message.get("type") == "capture":
                frame_data = message.get("data")
                side = message.get("side", "right")
                capture_type = message.get("capture_type", "before")  # "before" ou "after"

                if not frame_data:
                    await websocket.send_json({"error": "No frame data"})
                    continue

                # Decodificar frame
                try:
                    if "," in frame_data:
                        frame_data = frame_data.split(",")[1]

                    frame_bytes = base64.b64decode(frame_data)
                    nparr = np.frombuffer(frame_bytes, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                except Exception as e:
                    await websocket.send_json({
                        "error": f"Failed to decode: {str(e)}"
                    })
                    continue

                # Detectar pose
                keypoints, annotated_frame = detector.detect_with_visualization(frame)

                if not keypoints:
                    await websocket.send_json({
                        "type": "capture_result",
                        "success": False,
                        "error": "No pose detected in image"
                    })
                    continue

                # Calcular ângulos e recomendações
                angles = calculator.calculate_all(keypoints, side)
                recommendations = recommender.analyze(angles)

                # Desenhar pontos da coluna no frame
                if angles.get("spine"):
                    annotated_frame = draw_spine_on_frame(annotated_frame, angles["spine"])

                # Codificar frame processado
                _, buffer = cv2.imencode('.jpg', annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')

                await websocket.send_json({
                    "type": "capture_result",
                    "success": True,
                    "capture_type": capture_type,
                    "keypoints": keypoints,
                    "angles": angles,
                    "recommendations": recommendations,
                    "processed_image": f"data:image/jpeg;base64,{frame_base64}"
                })

            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        print("WebSocket de captura desconectado")

    except Exception as e:
        print(f"Erro no WebSocket de captura: {e}")
