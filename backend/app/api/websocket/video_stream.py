"""
WebSocket para streaming de vídeo em tempo real
"""
import cv2
import base64
import json
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Optional

from app.core.pose_detector import PoseDetector
from app.core.angle_calculator import AngleCalculator
from app.core.recommendations import RecommendationEngine

router = APIRouter()

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
                side = message.get("side")
                confidence = message.get("confidence")

                if side:
                    # Armazenar preferência de lado (pode ser usado em futuros frames)
                    pass

                if confidence:
                    detector.confidence_threshold = float(confidence)

                await websocket.send_json({
                    "type": "config_ack",
                    "message": "Configuration updated"
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
