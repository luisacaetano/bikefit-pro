"""
Motor de Recomendações para Bike Fit

Baseado em literatura científica:
- Holmes et al. (1994): Método original de posicionamento
- Bini & Hume (2020): Ranges dinâmicos corrigidos
- Bini et al. (2023): Diferenças estático vs dinâmico
- Martínez & Pérez (2025): Correlação com dor/lesão
"""
from typing import Dict, List, Optional, Any, Literal
from app.config import get_settings, get_angles_for_mode, get_angles_for_discipline

settings = get_settings()

AnalysisMode = Literal["static", "dynamic"]
CyclingDiscipline = Literal["road", "mtb", "triathlon", "gravel", "urban"]


class RecommendationEngine:
    """
    Motor de recomendações para ajustes de bike fit
    baseado nos ângulos articulares medidos.

    Suporta:
    - Modo estático vs dinâmico
    - Diferentes modalidades de ciclismo
    - Alertas de risco de lesão
    """

    def __init__(
        self,
        mode: AnalysisMode = "dynamic",
        discipline: CyclingDiscipline = "road"
    ):
        """
        Inicializa o motor de recomendações.

        Args:
            mode: "static" ou "dynamic"
            discipline: Modalidade de ciclismo
        """
        self.mode = mode
        self.discipline = discipline
        self._update_references()

    def _update_references(self):
        """Atualiza referências baseado no modo e modalidade"""
        # Referências base por modo
        self.references = get_angles_for_mode(self.mode)

        # Sobrescrever com valores específicos da modalidade
        discipline_refs = get_angles_for_discipline(self.discipline)
        for key, value in discipline_refs.items():
            if key not in ["description"] and isinstance(value, dict):
                self.references[key] = value

        # Limites de risco de lesão
        self.injury_thresholds = settings.injury_risk_thresholds

    def set_mode(self, mode: AnalysisMode):
        """Define modo de análise e atualiza referências"""
        self.mode = mode
        self._update_references()

    def set_discipline(self, discipline: CyclingDiscipline):
        """Define modalidade e atualiza referências"""
        self.discipline = discipline
        self._update_references()

    def _analyze_angle(
        self,
        angle_name: str,
        measured: Optional[float],
        reference: Dict
    ) -> Dict[str, Any]:
        """
        Analisa um ângulo específico

        Args:
            angle_name: Nome do ângulo
            measured: Valor medido
            reference: Valores de referência (min, max, optimal)

        Returns:
            Análise do ângulo com status e recomendação
        """
        if measured is None:
            return {
                "angle": angle_name,
                "measured": None,
                "reference": reference,
                "status": "not_detected",
                "deviation": None,
                "recommendation": "Ângulo não detectado na imagem"
            }

        min_val = reference["min"]
        max_val = reference["max"]
        optimal = reference["optimal"]

        # Calcular desvio do ótimo
        deviation = measured - optimal

        # Determinar status
        if min_val <= measured <= max_val:
            status = "optimal"
            recommendation = "Dentro da faixa ideal"
        elif measured < min_val:
            status = "below"
            recommendation = self._get_recommendation_below(angle_name, deviation)
        else:
            status = "above"
            recommendation = self._get_recommendation_above(angle_name, deviation)

        return {
            "angle": angle_name,
            "measured": round(measured, 1),
            "reference": reference,
            "status": status,
            "deviation": round(deviation, 1),
            "recommendation": recommendation
        }

    def _get_recommendation_below(self, angle_name: str, deviation: float) -> str:
        """Retorna recomendação quando ângulo está abaixo do ideal"""
        recommendations = {
            "knee_extension": f"Joelho muito flexionado ({abs(deviation):.0f}° abaixo). "
                             "Considere AUMENTAR altura do selim.",
            "knee_flexion_bdc": f"Flexão do joelho insuficiente ({abs(deviation):.0f}° abaixo). "
                               "Considere DIMINUIR altura do selim.",
            "hip": f"Ângulo do quadril fechado demais ({abs(deviation):.0f}° abaixo). "
                  "Considere AUMENTAR altura do guidão ou ajustar reach.",
            "ankle": f"Tornozelo em dorsiflexão excessiva ({abs(deviation):.0f}° abaixo). "
                    "Verificar posição do taco ou selim muito alto.",
            "trunk": f"Tronco muito inclinado ({abs(deviation):.0f}° abaixo). "
                    "Considere AUMENTAR altura do guidão.",
            "elbow": f"Cotovelo muito flexionado ({abs(deviation):.0f}° abaixo). "
                    "Considere ajustar reach (alcance) ou avanço."
        }
        return recommendations.get(angle_name, f"Ângulo abaixo do ideal ({abs(deviation):.0f}°)")

    def _get_recommendation_above(self, angle_name: str, deviation: float) -> str:
        """Retorna recomendação quando ângulo está acima do ideal"""
        recommendations = {
            "knee_extension": f"Joelho muito estendido ({deviation:.0f}° acima). "
                             "Considere DIMINUIR altura do selim para evitar sobrecarga.",
            "knee_flexion_bdc": f"Flexão do joelho excessiva ({deviation:.0f}° acima). "
                               "ATENÇÃO: >40° correlaciona com dor (Martínez 2025). "
                               "Considere AUMENTAR altura do selim.",
            "hip": f"Ângulo do quadril muito aberto ({deviation:.0f}° acima). "
                  "Considere posição mais aerodinâmica ou verificar selim.",
            "ankle": f"Tornozelo em plantiflexão excessiva ({deviation:.0f}° acima). "
                    "Verificar posição do taco ou técnica de pedalada.",
            "trunk": f"Tronco muito ereto ({deviation:.0f}° acima). "
                    "Para performance, considere posição mais aerodinâmica.",
            "elbow": f"Cotovelo muito estendido ({deviation:.0f}° acima). "
                    "Braços muito esticados podem causar desconforto. Verificar reach."
        }
        return recommendations.get(angle_name, f"Ângulo acima do ideal ({deviation:.0f}°)")

    def _check_injury_risk(self, angles: Dict[str, Optional[float]]) -> List[Dict[str, Any]]:
        """
        Verifica riscos de lesão baseado nos limiares definidos.

        Referência: Martínez & Pérez (2025) - flexão >40° correlaciona com dor

        Returns:
            Lista de alertas de risco de lesão
        """
        risks = []

        # Verificar flexão excessiva do joelho
        knee_flexion = angles.get("knee_flexion_bdc")
        if knee_flexion and knee_flexion > self.injury_thresholds.get("knee_flexion_bdc_max", 40):
            risks.append({
                "type": "injury_risk",
                "joint": "knee",
                "severity": "high",
                "message": f"ALERTA: Flexão do joelho ({knee_flexion:.1f}°) acima de 40° - "
                          "risco de dor/lesão (Martínez & Pérez 2025). "
                          "Recomenda-se AUMENTAR altura do selim.",
                "reference": "Martínez & Pérez (2025)"
            })

        # Verificar extensão excessiva do joelho
        knee_ext = angles.get("knee_extension") or angles.get("knee")
        if knee_ext and knee_ext > self.injury_thresholds.get("knee_extension_max", 160):
            risks.append({
                "type": "injury_risk",
                "joint": "knee",
                "severity": "medium",
                "message": f"ATENÇÃO: Extensão do joelho ({knee_ext:.1f}°) muito alta - "
                          "risco de sobrecarga. Considere DIMINUIR altura do selim.",
                "reference": "Holmes et al. (1994)"
            })

        # Verificar tronco muito baixo
        trunk = angles.get("trunk")
        if trunk and trunk < self.injury_thresholds.get("trunk_min", 30):
            risks.append({
                "type": "injury_risk",
                "joint": "spine",
                "severity": "medium",
                "message": f"ATENÇÃO: Tronco muito inclinado ({trunk:.1f}°) - "
                          "risco de dor cervical/lombar. Considere AUMENTAR altura do guidão.",
                "reference": "Burt (2014)"
            })

        return risks

    def analyze(self, angles: Dict[str, Optional[float]]) -> Dict[str, Any]:
        """
        Analisa todos os ângulos e gera recomendações.

        Args:
            angles: Dicionário com ângulos medidos

        Returns:
            Dicionário com análise completa e recomendações
        """
        analysis = {
            "overall_status": "optimal",
            "angles_analysis": [],
            "priority_adjustments": [],
            "injury_risks": [],
            "summary": "",
            "mode": self.mode,
            "discipline": self.discipline
        }

        issues_count = 0

        # Mapear nomes dos ângulos para referências
        # Suporta tanto nomenclatura nova quanto legada
        angle_mapping = {
            "knee_extension": "knee_extension",
            "knee_flexion_bdc": "knee_flexion_bdc",
            "knee": "knee_extension",  # Alias legado
            "hip": "hip",
            "ankle": "ankle",
            "trunk": "trunk",
            "elbow": "elbow"
        }

        for angle_key, ref_key in angle_mapping.items():
            if angle_key not in angles:
                continue

            measured = angles[angle_key]
            reference = self.references.get(ref_key, {"min": 0, "max": 180, "optimal": 90})

            angle_analysis = self._analyze_angle(ref_key, measured, reference)
            analysis["angles_analysis"].append(angle_analysis)

            if angle_analysis["status"] not in ["optimal", "not_detected"]:
                issues_count += 1
                # Adicionar aos ajustes prioritários se desvio significativo
                if angle_analysis["deviation"] and abs(angle_analysis["deviation"]) > 5:
                    analysis["priority_adjustments"].append({
                        "angle": ref_key,
                        "severity": "high" if abs(angle_analysis["deviation"]) > 10 else "medium",
                        "action": angle_analysis["recommendation"]
                    })

        # Verificar riscos de lesão
        analysis["injury_risks"] = self._check_injury_risk(angles)
        has_injury_risk = len(analysis["injury_risks"]) > 0

        # Definir status geral
        if has_injury_risk:
            analysis["overall_status"] = "injury_risk"
            analysis["summary"] = f"ATENÇÃO: {len(analysis['injury_risks'])} alerta(s) de risco de lesão!"
        elif issues_count == 0:
            analysis["overall_status"] = "optimal"
            analysis["summary"] = "Todos os ângulos estão dentro da faixa ideal. Posição adequada!"
        elif issues_count <= 2:
            analysis["overall_status"] = "minor_adjustments"
            analysis["summary"] = f"Posição boa com {issues_count} ajuste(s) menor(es) sugerido(s)."
        else:
            analysis["overall_status"] = "needs_adjustment"
            analysis["summary"] = f"Posição requer atenção. {issues_count} ajustes recomendados."

        # Ordenar ajustes prioritários por severidade
        analysis["priority_adjustments"].sort(
            key=lambda x: 0 if x["severity"] == "high" else 1
        )

        return analysis

    def compare_before_after(
        self,
        angles_before: Dict,
        angles_after: Dict
    ) -> Dict[str, Any]:
        """
        Compara ângulos antes e depois do ajuste

        Args:
            angles_before: Ângulos antes do ajuste
            angles_after: Ângulos depois do ajuste

        Returns:
            Comparação com melhorias
        """
        comparison = {
            "improvements": [],
            "regressions": [],
            "unchanged": [],
            "overall_improvement": 0
        }

        angle_mapping = {
            "knee": "knee_extension",
            "hip": "hip",
            "ankle": "ankle",
            "trunk": "trunk",
            "elbow": "elbow"
        }

        total_improvement = 0
        count = 0

        for angle_key, ref_key in angle_mapping.items():
            before = angles_before.get(angle_key)
            after = angles_after.get(angle_key)

            if before is None or after is None:
                continue

            reference = self.references.get(ref_key, {})
            optimal = reference.get("optimal", 90)

            # Calcular melhoria (redução do desvio do ótimo)
            deviation_before = abs(before - optimal)
            deviation_after = abs(after - optimal)
            improvement = deviation_before - deviation_after

            total_improvement += improvement
            count += 1

            item = {
                "angle": ref_key,
                "before": round(before, 1),
                "after": round(after, 1),
                "change": round(after - before, 1),
                "improvement": round(improvement, 1)
            }

            if improvement > 1:
                comparison["improvements"].append(item)
            elif improvement < -1:
                comparison["regressions"].append(item)
            else:
                comparison["unchanged"].append(item)

        if count > 0:
            comparison["overall_improvement"] = round(total_improvement / count, 1)

        return comparison
