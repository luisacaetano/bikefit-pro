# Stack Tecnológica - BikeFit AI

> Documentação das tecnologias utilizadas no projeto

---

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              ENTRADA                                     │
│                    (Vídeo MP4 / Webcam / Celular)                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PROCESSAMENTO DE VÍDEO                           │
│                              (OpenCV)                                    │
│         • Leitura de frames • Redimensionamento • Conversão RGB         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         ESTIMATIVA DE POSE                               │
│                            (MediaPipe)                                   │
│              • Detecção de 33 pontos anatômicos (landmarks)             │
│              • Coordenadas 2D e 3D de cada articulação                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CÁLCULO DE ÂNGULOS                               │
│                             (NumPy)                                      │
│         • Vetores entre landmarks • Produto escalar • Arco-cosseno      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      ANÁLISE E RECOMENDAÇÕES                             │
│                            (Pandas)                                      │
│       • Comparação com ângulos ideais • Geração de recomendações        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              SAÍDA                                       │
│              (Streamlit / PDF / Visualização em tempo real)             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Tecnologias Principais

### 1. MediaPipe Pose (Google)

**O que é:** Biblioteca de ML do Google para estimativa de pose em tempo real.

**Por que usar:**
- Detecta 33 pontos anatômicos (landmarks) do corpo
- Funciona com câmera 2D comum (não precisa de sensores especiais)
- Tempo real (~30 FPS em CPU)
- Gratuito e open-source
- Boa documentação

**Landmarks relevantes para Bike Fit:**
```
QUADRIL:      23 (esquerdo), 24 (direito)
JOELHO:       25 (esquerdo), 26 (direito)
TORNOZELO:    27 (esquerdo), 28 (direito)
OMBRO:        11 (esquerdo), 12 (direito)
COTOVELO:     13 (esquerdo), 14 (direito)
PUNHO:        15 (esquerdo), 16 (direito)
CALCANHAR:    29 (esquerdo), 30 (direito)
PÉ (PONTA):   31 (esquerdo), 32 (direito)
```

**Instalação:**
```bash
pip install mediapipe
```

**Exemplo básico:**
```python
import mediapipe as mp
import cv2

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture("video.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converter BGR para RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar pose
    results = pose.process(rgb)

    if results.pose_landmarks:
        # Acessar coordenadas do joelho direito
        knee = results.pose_landmarks.landmark[26]
        print(f"Joelho: x={knee.x}, y={knee.y}, z={knee.z}")
```

---

### 2. OpenCV (Open Computer Vision)

**O que é:** Biblioteca para processamento de imagens e vídeo.

**Uso no projeto:**
- Leitura de vídeos (MP4, webcam)
- Conversão de cores (BGR ↔ RGB)
- Desenho de linhas e pontos na imagem
- Redimensionamento de frames
- Gravação de vídeo processado

**Instalação:**
```bash
pip install opencv-python
```

---

### 3. NumPy

**O que é:** Biblioteca para computação numérica.

**Uso no projeto:**
- Cálculo de ângulos entre vetores
- Operações com coordenadas 3D
- Estatísticas (média, desvio padrão dos ângulos)

**Cálculo de ângulo entre 3 pontos:**
```python
import numpy as np

def calcular_angulo(p1, p2, p3):
    """
    Calcula o ângulo no ponto p2 formado pelos pontos p1-p2-p3

    Args:
        p1, p2, p3: arrays com coordenadas [x, y] ou [x, y, z]

    Returns:
        Ângulo em graus
    """
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)

    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))

    return np.degrees(angle)

# Exemplo: ângulo do joelho
quadril = [0.5, 0.3]
joelho = [0.5, 0.5]
tornozelo = [0.5, 0.7]

angulo_joelho = calcular_angulo(quadril, joelho, tornozelo)
print(f"Ângulo do joelho: {angulo_joelho:.1f}°")
```

---

### 4. Pandas

**O que é:** Biblioteca para análise de dados.

**Uso no projeto:**
- Armazenar histórico de ângulos por frame
- Calcular médias e variações ao longo do vídeo
- Exportar dados para CSV/Excel
- Comparar com parâmetros de referência

**Instalação:**
```bash
pip install pandas
```

---

### 5. Streamlit

**O que é:** Framework para criar interfaces web com Python.

**Uso no projeto:**
- Interface para upload de vídeo
- Visualização em tempo real
- Dashboard com gráficos dos ângulos
- Exibição de recomendações

**Instalação:**
```bash
pip install streamlit
```

**Exemplo básico:**
```python
import streamlit as st

st.title("BikeFit AI")

video_file = st.file_uploader("Upload do vídeo", type=["mp4", "mov"])

if video_file:
    st.video(video_file)

    if st.button("Analisar"):
        st.write("Processando...")
        # Chamar função de análise
```

---

### 6. Matplotlib

**O que é:** Biblioteca para criação de gráficos.

**Uso no projeto:**
- Gráficos de evolução dos ângulos ao longo do tempo
- Comparação visual com faixas ideais
- Exportação de figuras para relatório

**Instalação:**
```bash
pip install matplotlib
```

---

## Tecnologias Opcionais/Futuras

| Tecnologia | Uso | Quando implementar |
|------------|-----|-------------------|
| **ReportLab** | Geração de PDF | Fase final |
| **SQLite** | Banco de dados local | Se precisar histórico |
| **FastAPI** | API REST | Versão web/mobile |
| **TensorFlow Lite** | Deploy mobile | Versão app celular |

---

## Requisitos de Hardware

### Mínimo
- CPU: Intel i5 / Apple M1 ou equivalente
- RAM: 8 GB
- Câmera: 720p

### Recomendado
- CPU: Intel i7 / Apple M2 ou superior
- RAM: 16 GB
- Câmera: 1080p a 30fps

### Seu Setup (MacBook M3)
- **CPU:** Apple M3 (excelente para ML)
- **Câmera:** 1080p FaceTime HD
- **Recomendação:** Usar celular no tripé para gravação lateral

---

## Estrutura de Módulos do Projeto

```
src/
├── main.py                 # Ponto de entrada
├── pose/
│   ├── __init__.py
│   ├── detector.py         # Classe para detecção de pose
│   └── landmarks.py        # Mapeamento dos landmarks
├── analysis/
│   ├── __init__.py
│   ├── angles.py           # Cálculo de ângulos
│   └── comparator.py       # Comparação com referência
├── recommendations/
│   ├── __init__.py
│   ├── rules.py            # Regras de ajuste
│   └── generator.py        # Geração de recomendações
├── utils/
│   ├── __init__.py
│   ├── video.py            # Utilitários de vídeo
│   └── visualization.py    # Desenho na imagem
└── app.py                  # Interface Streamlit
```

---

## Fluxo de Dados

```
1. ENTRADA
   └── Vídeo lateral do ciclista (celular/webcam)

2. PRÉ-PROCESSAMENTO
   ├── Extrair frames (30 fps)
   ├── Converter para RGB
   └── Redimensionar se necessário

3. DETECÇÃO DE POSE
   ├── MediaPipe processa cada frame
   ├── Retorna 33 landmarks com coordenadas (x, y, z)
   └── Confiança de cada detecção (visibility)

4. CÁLCULO DE ÂNGULOS
   ├── Identificar frames no BDC (pedivela às 6h)
   ├── Calcular ângulos: joelho, quadril, tornozelo, etc.
   └── Armazenar em DataFrame

5. ANÁLISE
   ├── Calcular média dos ângulos
   ├── Comparar com parâmetros ideais
   └── Identificar desvios

6. RECOMENDAÇÕES
   ├── Se joelho > 40° → "Aumentar altura do selim"
   ├── Se joelho < 25° → "Diminuir altura do selim"
   └── etc.

7. SAÍDA
   ├── Vídeo anotado com ângulos
   ├── Dashboard com gráficos
   └── Relatório PDF com recomendações
```

---

*Última atualização: 13/03/2026*
