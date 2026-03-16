"""
Calculador de Ângulos Articulares para Bike Fit

Referências científicas:
- Holmes et al. (1994): Método original (25-35° flexão estática)
- Bini & Hume (2020): Ranges dinâmicos (33-43° flexão)
- Bini et al. (2023): Diferenças estático vs dinâmico
- Martínez & Pérez (2025): Flexão >40° correlaciona com dor

Nomenclatura:
- knee_extension: Ângulo de extensão do joelho (hip-knee-ankle)
- knee_flexion_bdc: Flexão no Bottom Dead Center = 180° - extensão
"""
import math
from typing import Dict, Any, Optional, Tuple, Literal

# Tipo para modo de análise
AnalysisMode = Literal["static", "dynamic"]
CyclingDiscipline = Literal["road", "mtb", "triathlon", "gravel", "urban"]


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
    """
    Calculador de ângulos articulares para análise de bike fit.

    Suporta dois modos de análise:
    - static: Ciclista parado (referência Holmes 1994)
    - dynamic: Ciclista pedalando (referência Bini 2020)

    Suporta diferentes modalidades:
    - road, mtb, triathlon, gravel, urban
    """

    def __init__(
        self,
        mode: AnalysisMode = "dynamic",
        discipline: CyclingDiscipline = "road"
    ):
        """
        Inicializa o calculador.

        Args:
            mode: Modo de análise ("static" ou "dynamic")
            discipline: Modalidade de ciclismo
        """
        self.mode = mode
        self.discipline = discipline

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

    def calculate_knee_extension(self, keypoints: Dict, side: str = "right") -> Optional[float]:
        """
        Calcula o ângulo de EXTENSÃO do joelho (hip-knee-ankle).

        Este é o ângulo interno do joelho:
        - 180° = perna totalmente esticada
        - 90° = joelho em ângulo reto

        Referências:
        - Estático: 145-155° (Holmes 1994)
        - Dinâmico: 137-147° (Bini 2020)

        Args:
            keypoints: Dicionário de keypoints
            side: "left" ou "right"

        Returns:
            Ângulo de extensão do joelho em graus
        """
        hip = self._get_point(keypoints, f"{side}_hip")
        knee = self._get_point(keypoints, f"{side}_knee")
        ankle = self._get_point(keypoints, f"{side}_ankle")

        if not all([hip, knee, ankle]):
            return None

        return calculate_angle(hip, knee, ankle)

    def calculate_knee_flexion_bdc(self, keypoints: Dict, side: str = "right") -> Optional[float]:
        """
        Calcula o ângulo de FLEXÃO do joelho no Bottom Dead Center (BDC).

        BDC = ponto morto inferior (6 horas do pedal)
        Flexão = 180° - Extensão

        Este é o valor usado na literatura científica:
        - Estático: 25-35° (Holmes 1994)
        - Dinâmico: 33-43° (Bini 2020)
        - >40° correlaciona com dor (Martínez & Pérez 2025)

        Args:
            keypoints: Dicionário de keypoints
            side: "left" ou "right"

        Returns:
            Ângulo de flexão do joelho em graus
        """
        extension = self.calculate_knee_extension(keypoints, side)
        if extension is None:
            return None

        # Flexão = 180° - Extensão
        return 180.0 - extension

    # Alias para compatibilidade com código legado
    def calculate_knee_angle(self, keypoints: Dict, side: str = "right") -> Optional[float]:
        """Alias para calculate_knee_extension (compatibilidade)"""
        return self.calculate_knee_extension(keypoints, side)

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

    def calculate_spine_points(self, keypoints: Dict) -> Optional[Dict[str, Any]]:
        """
        Calcula 3 pontos estimados da coluna vertebral.

        Pontos:
        - spine_top: Coluna alta (~C7/T1) - entre os ombros
        - spine_mid: Coluna média (~T12/L1) - ponto médio do tronco
        - spine_low: Coluna baixa (~L5/S1) - entre os quadris

        Returns:
            Dicionário com os 3 pontos da coluna e análise de curvatura
        """
        # Obter pontos dos ombros e quadris
        l_shoulder = self._get_point(keypoints, "left_shoulder")
        r_shoulder = self._get_point(keypoints, "right_shoulder")
        l_hip = self._get_point(keypoints, "left_hip")
        r_hip = self._get_point(keypoints, "right_hip")

        # Precisamos de pelo menos um ombro e um quadril de cada lado
        # ou ambos de um lado
        if not any([l_shoulder, r_shoulder]) or not any([l_hip, r_hip]):
            return None

        # Calcular ponto médio dos ombros (COLUNA ALTA - C7/T1)
        if l_shoulder and r_shoulder:
            spine_top = (
                (l_shoulder[0] + r_shoulder[0]) / 2,
                (l_shoulder[1] + r_shoulder[1]) / 2
            )
        else:
            spine_top = l_shoulder or r_shoulder

        # Calcular ponto médio dos quadris (COLUNA BAIXA - L5/S1)
        if l_hip and r_hip:
            spine_low = (
                (l_hip[0] + r_hip[0]) / 2,
                (l_hip[1] + r_hip[1]) / 2
            )
        else:
            spine_low = l_hip or r_hip

        # Calcular ponto médio da coluna (COLUNA MÉDIA - T12/L1)
        # Este é o ponto que indica a curvatura
        spine_mid_straight = (
            (spine_top[0] + spine_low[0]) / 2,
            (spine_top[1] + spine_low[1]) / 2
        )

        # Para estimar curvatura real, usamos uma heurística:
        # Em posição de ciclismo, a coluna média tende a ir ligeiramente
        # para frente (em X) devido à flexão do tronco
        # Vamos detectar isso comparando com a linha reta

        # Calcular desvio da linha reta (curvatura)
        # Positivo = cifose (curvado para frente/corcunda)
        # Negativo = lordose (curvado para trás)
        # Para isso, precisamos de uma referência lateral

        # Usar a posição X relativa para detectar curvatura
        # Se o ponto médio está à frente da linha reta = cifose
        spine_length = math.sqrt(
            (spine_top[0] - spine_low[0])**2 +
            (spine_top[1] - spine_low[1])**2
        )

        # Calcular ângulo da coluna
        spine_angle = self.calculate_trunk_angle(keypoints)

        # O ponto médio real pode ser ajustado baseado em padrões típicos
        # Por enquanto, usamos o ponto médio geométrico
        spine_mid = spine_mid_straight

        # Calcular curvatura como o ângulo formado pelos 3 pontos
        # 180° = perfeitamente reto
        # < 180° = curvatura (cifose ou lordose dependendo da direção)
        spine_curvature_angle = calculate_angle(spine_top, spine_mid, spine_low)

        # Determinar tipo de curvatura baseado na posição
        # Em vista lateral: se mid está à frente da linha top-low = cifose
        curvature_type = "neutral"
        curvature_severity = "normal"

        # Calcular desvio perpendicular do ponto médio
        # da linha que conecta top a low
        if spine_length > 0:
            # Vetor da linha top -> low
            line_vec = (spine_low[0] - spine_top[0], spine_low[1] - spine_top[1])
            # Vetor de top -> mid
            point_vec = (spine_mid[0] - spine_top[0], spine_mid[1] - spine_top[1])

            # Produto vetorial 2D (componente Z)
            cross = line_vec[0] * point_vec[1] - line_vec[1] * point_vec[0]

            # Normalizar pelo comprimento da coluna
            deviation = cross / spine_length

            # Classificar curvatura
            if abs(deviation) < 5:
                curvature_type = "neutral"
                curvature_severity = "normal"
            elif deviation > 0:
                curvature_type = "kyphosis"  # Cifose
                curvature_severity = "mild" if deviation < 15 else "moderate" if deviation < 25 else "severe"
            else:
                curvature_type = "lordosis"  # Lordose
                curvature_severity = "mild" if abs(deviation) < 15 else "moderate" if abs(deviation) < 25 else "severe"

        return {
            "spine_top": {"x": spine_top[0], "y": spine_top[1], "label": "C7/T1"},
            "spine_mid": {"x": spine_mid[0], "y": spine_mid[1], "label": "T12/L1"},
            "spine_low": {"x": spine_low[0], "y": spine_low[1], "label": "L5/S1"},
            "spine_angle": spine_curvature_angle,
            "curvature_type": curvature_type,
            "curvature_severity": curvature_severity,
            "spine_length": spine_length
        }

    def calculate_all(self, keypoints: Dict, side: str = "right") -> Dict[str, Any]:
        """
        Calcula todos os ângulos relevantes para bike fit.

        Args:
            keypoints: Dicionário de keypoints
            side: Lado a analisar ("left" ou "right")

        Returns:
            Dicionário com todos os ângulos e dados da coluna
        """
        knee_extension = self.calculate_knee_extension(keypoints, side)
        knee_flexion = 180.0 - knee_extension if knee_extension else None

        return {
            # Ângulos principais
            "knee_extension": knee_extension,
            "knee_flexion_bdc": knee_flexion,
            "hip": self.calculate_hip_angle(keypoints, side),
            "ankle": self.calculate_ankle_angle(keypoints, side),
            "elbow": self.calculate_elbow_angle(keypoints, side),
            "trunk": self.calculate_trunk_angle(keypoints),

            # Análise da coluna
            "spine": self.calculate_spine_points(keypoints),

            # Metadados
            "side_analyzed": side,
            "analysis_mode": self.mode,
            "discipline": self.discipline,

            # Alias para compatibilidade
            "knee": knee_extension,
        }

    def set_mode(self, mode: AnalysisMode) -> None:
        """Define o modo de análise (static/dynamic)"""
        self.mode = mode

    def set_discipline(self, discipline: CyclingDiscipline) -> None:
        """Define a modalidade de ciclismo"""
        self.discipline = discipline
