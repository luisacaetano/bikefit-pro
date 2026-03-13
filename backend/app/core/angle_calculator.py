"""
Calculador de Ângulos Articulares para Bike Fit
"""
import math
from typing import Dict, Any, Optional, Tuple


def calculate_angle(p1: Tuple[float, float], p2: Tuple[float, float], p3: Tuple[float, float]) -> float:
    """
    Calcula o ângulo formado por três pontos.

    O ângulo é calculado no ponto p2 (vértice do ângulo).

    Args:
        p1: Primeiro ponto (x, y)
        p2: Ponto central/vértice (x, y)
        p3: Terceiro ponto (x, y)

    Returns:
        Ângulo em graus (0-180)
    """
    # Vetores
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])

    # Produto escalar
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]

    # Magnitudes
    mag1 = math.sqrt(v1[0]**2 + v1[1]**2)
    mag2 = math.sqrt(v2[0]**2 + v2[1]**2)

    if mag1 == 0 or mag2 == 0:
        return 0

    # Ângulo em radianos
    cos_angle = dot_product / (mag1 * mag2)
    # Limitar ao intervalo [-1, 1] para evitar erros de arredondamento
    cos_angle = max(-1, min(1, cos_angle))

    angle_rad = math.acos(cos_angle)

    # Converter para graus
    return math.degrees(angle_rad)


class AngleCalculator:
    """Calculador de ângulos articulares para análise de bike fit"""

    def __init__(self):
        """Inicializa o calculador"""
        pass

    def _get_point(self, keypoints: Dict, name: str) -> Optional[Tuple[float, float]]:
        """
        Extrai coordenadas de um keypoint

        Args:
            keypoints: Dicionário de keypoints
            name: Nome do keypoint

        Returns:
            Tupla (x, y) ou None se não existir
        """
        if name not in keypoints:
            return None
        kp = keypoints[name]
        return (kp["x"], kp["y"])

    def calculate_knee_angle(self, keypoints: Dict, side: str = "right") -> Optional[float]:
        """
        Calcula o ângulo do joelho (hip-knee-ankle)

        Para bike fit, medimos:
        - Extensão máxima: quando a perna está mais estendida (140-150°)
        - Flexão máxima: quando a perna está mais flexionada (65-75°)

        Args:
            keypoints: Dicionário de keypoints
            side: "left" ou "right"

        Returns:
            Ângulo do joelho em graus
        """
        hip = self._get_point(keypoints, f"{side}_hip")
        knee = self._get_point(keypoints, f"{side}_knee")
        ankle = self._get_point(keypoints, f"{side}_ankle")

        if not all([hip, knee, ankle]):
            return None

        return calculate_angle(hip, knee, ankle)

    def calculate_hip_angle(self, keypoints: Dict, side: str = "right") -> Optional[float]:
        """
        Calcula o ângulo do quadril (shoulder-hip-knee)

        Ângulo ideal para bike fit: 40-50°

        Args:
            keypoints: Dicionário de keypoints
            side: "left" ou "right"

        Returns:
            Ângulo do quadril em graus
        """
        shoulder = self._get_point(keypoints, f"{side}_shoulder")
        hip = self._get_point(keypoints, f"{side}_hip")
        knee = self._get_point(keypoints, f"{side}_knee")

        if not all([shoulder, hip, knee]):
            return None

        return calculate_angle(shoulder, hip, knee)

    def calculate_ankle_angle(self, keypoints: Dict, side: str = "right") -> Optional[float]:
        """
        Calcula o ângulo do tornozelo (knee-ankle-toe)

        Nota: YOLOv8 não detecta o dedo do pé, então usamos
        uma estimativa baseada na posição do tornozelo.
        Ângulo ideal: 90-110° (dorsiflexão neutra)

        Args:
            keypoints: Dicionário de keypoints
            side: "left" ou "right"

        Returns:
            Ângulo estimado do tornozelo
        """
        knee = self._get_point(keypoints, f"{side}_knee")
        ankle = self._get_point(keypoints, f"{side}_ankle")

        if not all([knee, ankle]):
            return None

        # Estimativa: consideramos um ponto virtual à frente do tornozelo
        # representando a posição do pé
        toe_virtual = (ankle[0] + 50, ankle[1])  # 50px à frente

        return calculate_angle(knee, ankle, toe_virtual)

    def calculate_elbow_angle(self, keypoints: Dict, side: str = "right") -> Optional[float]:
        """
        Calcula o ângulo do cotovelo (shoulder-elbow-wrist)

        Ângulo ideal para bike fit: 150-170° (ligeira flexão)

        Args:
            keypoints: Dicionário de keypoints
            side: "left" ou "right"

        Returns:
            Ângulo do cotovelo em graus
        """
        shoulder = self._get_point(keypoints, f"{side}_shoulder")
        elbow = self._get_point(keypoints, f"{side}_elbow")
        wrist = self._get_point(keypoints, f"{side}_wrist")

        if not all([shoulder, elbow, wrist]):
            return None

        return calculate_angle(shoulder, elbow, wrist)

    def calculate_trunk_angle(self, keypoints: Dict) -> Optional[float]:
        """
        Calcula o ângulo do tronco em relação à horizontal

        Ângulo ideal para bike fit: 40-55°

        Returns:
            Ângulo do tronco em graus
        """
        # Usar média dos ombros e quadris
        l_shoulder = self._get_point(keypoints, "left_shoulder")
        r_shoulder = self._get_point(keypoints, "right_shoulder")
        l_hip = self._get_point(keypoints, "left_hip")
        r_hip = self._get_point(keypoints, "right_hip")

        if not any([l_shoulder, r_shoulder]) or not any([l_hip, r_hip]):
            return None

        # Calcular pontos médios
        if l_shoulder and r_shoulder:
            shoulder = ((l_shoulder[0] + r_shoulder[0]) / 2, (l_shoulder[1] + r_shoulder[1]) / 2)
        else:
            shoulder = l_shoulder or r_shoulder

        if l_hip and r_hip:
            hip = ((l_hip[0] + r_hip[0]) / 2, (l_hip[1] + r_hip[1]) / 2)
        else:
            hip = l_hip or r_hip

        # Calcular ângulo com a horizontal
        dx = shoulder[0] - hip[0]
        dy = hip[1] - shoulder[1]  # Invertido porque y cresce para baixo

        angle_rad = math.atan2(dy, abs(dx))
        return math.degrees(angle_rad)

    def calculate_all(self, keypoints: Dict, side: str = "right") -> Dict[str, Optional[float]]:
        """
        Calcula todos os ângulos relevantes para bike fit

        Args:
            keypoints: Dicionário de keypoints
            side: Lado a analisar ("left" ou "right")

        Returns:
            Dicionário com todos os ângulos
        """
        return {
            "knee": self.calculate_knee_angle(keypoints, side),
            "hip": self.calculate_hip_angle(keypoints, side),
            "ankle": self.calculate_ankle_angle(keypoints, side),
            "elbow": self.calculate_elbow_angle(keypoints, side),
            "trunk": self.calculate_trunk_angle(keypoints),
            "side_analyzed": side
        }
