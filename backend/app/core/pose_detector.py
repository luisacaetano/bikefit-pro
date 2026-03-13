"""
Detector de Pose usando YOLOv8-Pose
"""
import cv2
import numpy as np
from ultralytics import YOLO
from typing import Optional, Dict, List, Any
from app.config import get_settings

settings = get_settings()


# Mapeamento dos keypoints do YOLOv8-Pose (COCO format)
KEYPOINT_NAMES = {
    0: "nose",
    1: "left_eye",
    2: "right_eye",
    3: "left_ear",
    4: "right_ear",
    5: "left_shoulder",
    6: "right_shoulder",
    7: "left_elbow",
    8: "right_elbow",
    9: "left_wrist",
    10: "right_wrist",
    11: "left_hip",
    12: "right_hip",
    13: "left_knee",
    14: "right_knee",
    15: "left_ankle",
    16: "right_ankle"
}


class PoseDetector:
    """Classe para detecção de pose usando YOLOv8"""

    def __init__(self, model_name: str = None):
        """
        Inicializa o detector de pose

        Args:
            model_name: Nome do modelo YOLO (default: yolov8n-pose.pt)
        """
        self.model_name = model_name or settings.yolo_model
        self.model: Optional[YOLO] = None
        self.confidence_threshold = settings.confidence_threshold

    def _load_model(self):
        """Carrega o modelo YOLO sob demanda"""
        if self.model is None:
            print(f"Carregando modelo {self.model_name}...")
            self.model = YOLO(self.model_name)
            print("Modelo carregado com sucesso!")

    def detect(self, image_data: bytes) -> Optional[Dict[str, Any]]:
        """
        Detecta pose em uma imagem

        Args:
            image_data: Dados da imagem em bytes

        Returns:
            Dicionário com keypoints ou None se não detectar
        """
        self._load_model()

        # Converter bytes para imagem OpenCV
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return None

        return self.detect_from_frame(img)

    def detect_from_frame(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Detecta pose em um frame (numpy array)

        Args:
            frame: Frame em formato numpy array (BGR)

        Returns:
            Dicionário com keypoints ou None se não detectar
        """
        self._load_model()

        # Executar inferência
        results = self.model(frame, verbose=False)

        if not results or len(results) == 0:
            return None

        result = results[0]

        # Verificar se há detecções
        if result.keypoints is None or len(result.keypoints) == 0:
            return None

        # Pegar a primeira pessoa detectada (maior confiança)
        keypoints_data = result.keypoints.data[0]  # [17, 3] - x, y, conf

        # Filtrar por confiança
        keypoints = {}
        for idx, kp in enumerate(keypoints_data):
            x, y, conf = kp.tolist()
            if conf >= self.confidence_threshold:
                keypoints[KEYPOINT_NAMES[idx]] = {
                    "x": float(x),
                    "y": float(y),
                    "confidence": float(conf)
                }

        return keypoints if keypoints else None

    def detect_with_visualization(self, frame: np.ndarray) -> tuple:
        """
        Detecta pose e retorna frame com visualização

        Args:
            frame: Frame em formato numpy array (BGR)

        Returns:
            Tupla (keypoints, frame_anotado)
        """
        self._load_model()

        # Executar inferência
        results = self.model(frame, verbose=False)

        if not results or len(results) == 0:
            return None, frame

        result = results[0]

        # Frame com anotações do YOLO
        annotated_frame = result.plot()

        # Extrair keypoints
        if result.keypoints is None or len(result.keypoints) == 0:
            return None, annotated_frame

        keypoints_data = result.keypoints.data[0]
        keypoints = {}
        for idx, kp in enumerate(keypoints_data):
            x, y, conf = kp.tolist()
            if conf >= self.confidence_threshold:
                keypoints[KEYPOINT_NAMES[idx]] = {
                    "x": float(x),
                    "y": float(y),
                    "confidence": float(conf)
                }

        return keypoints if keypoints else None, annotated_frame
