"""
Motor de Recomendações para Bike Fit
"""
from typing import Dict, List, Optional, Any
from app.config import get_settings

settings = get_settings()


class RecommendationEngine:
    """
    Motor de recomendações para ajustes de bike fit
    baseado nos ângulos articulares medidos.
    """

    def __init__(self):
        """Inicializa o motor de recomendações"""
        self.references = settings.angles_reference

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
            "knee_extension": f"Joelho muito flexionado na extensão ({abs(deviation):.0f}° abaixo). "
                             "Considere AUMENTAR altura do selim.",
            "knee_flexion": f"Joelho com pouca flexão ({abs(deviation):.0f}° abaixo). "
                           "O ciclista pode estar muito esticado no topo da pedalada.",
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
            "knee_flexion": f"Joelho com flexão excessiva ({deviation:.0f}° acima). "
                           "Verificar posição do selim (pode estar muito baixo).",
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

    def analyze(self, angles: Dict[str, Optional[float]]) -> Dict[str, Any]:
        """
        Analisa todos os ângulos e gera recomendações

        Args:
            angles: Dicionário com ângulos medidos

        Returns:
            Dicionário com análise completa e recomendações
        """
        analysis = {
            "overall_status": "optimal",
            "angles_analysis": [],
            "priority_adjustments": [],
            "summary": ""
        }

        issues_count = 0

        # Mapear nomes dos ângulos para referências
        angle_mapping = {
            "knee": "knee_extension",  # Usamos knee_extension como referência principal
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

        # Definir status geral
        if issues_count == 0:
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
