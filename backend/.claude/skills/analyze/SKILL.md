---
name: analyze
description: Analisa postura de ciclista em uma imagem usando YOLOv8 pose detection
argument-hint: [caminho-da-imagem]
allowed-tools: Bash(python *), Bash(cd *)
---

# Skill: Analisar Imagem de Ciclista

Quando o usuario invocar `/analyze`, execute a analise de pose em uma imagem estatica.

## Uso

```
/analyze <caminho-da-imagem>
```

## Script de Analise

Execute o seguinte script Python:

```python
import sys
sys.path.insert(0, '/Users/luisacaetano/Desktop/TCC/backend')

from app.core.pose_detector import PoseDetector
from app.core.angle_calculator import AngleCalculator
from app.core.recommendations import RecommendationEngine
import cv2
import json

# Carregar imagem
image_path = "$ARGUMENTS"
frame = cv2.imread(image_path)

if frame is None:
    print(f"Erro: Nao foi possivel carregar a imagem: {image_path}")
    sys.exit(1)

# Detectar pose
detector = PoseDetector()
calculator = AngleCalculator()
recommender = RecommendationEngine()

keypoints, annotated_frame = detector.detect_with_visualization(frame)

if not keypoints:
    print("Nenhuma pose detectada na imagem")
    sys.exit(1)

# Calcular angulos
angles = calculator.calculate_all(keypoints, "right")
recommendations = recommender.analyze(angles)

# Mostrar resultados
print("\n=== ANALISE DE BIKE FIT ===\n")
print("ANGULOS DETECTADOS:")
for key, value in angles.items():
    if value is not None and key not in ["side_analyzed", "spine"]:
        print(f"  {key}: {value:.1f} graus")

if angles.get("spine"):
    spine = angles["spine"]
    print(f"\nCOLUNA:")
    print(f"  Tipo de curvatura: {spine['curvature_type']}")
    print(f"  Severidade: {spine['curvature_severity']}")

print(f"\nSTATUS: {recommendations['overall_status']}")
print(f"RESUMO: {recommendations['summary']}")

if recommendations.get("priority_adjustments"):
    print("\nAJUSTES RECOMENDADOS:")
    for adj in recommendations["priority_adjustments"]:
        print(f"  - [{adj['severity']}] {adj['action']}")

# Salvar imagem anotada
output_path = image_path.replace('.', '_analyzed.')
cv2.imwrite(output_path, annotated_frame)
print(f"\nImagem anotada salva em: {output_path}")
```

## Comando

```bash
cd /Users/luisacaetano/Desktop/TCC/backend && source venv/bin/activate && python -c "
[script acima com $ARGUMENTS substituido]
"
```

## Exemplos

- `/analyze /tmp/ciclista.jpg` - Analisa imagem
- `/analyze ~/Desktop/foto.png` - Analisa foto do desktop

## Notas

- Suporta formatos: JPG, PNG, JPEG
- A imagem deve mostrar o ciclista de perfil (lado direito ou esquerdo)
- O modelo YOLOv8 detecta 17 keypoints do corpo
- A imagem anotada e salva com sufixo `_analyzed`
