# 4. Desenvolvimento

Este capítulo apresenta os detalhes de implementação do sistema ALPR, incluindo a arquitetura do sistema, módulo de detecção, módulo de OCR e interface de usuário.

## 4.1 Visão Geral da Arquitetura

O sistema foi desenvolvido seguindo uma arquitetura modular, facilitando manutenção e testes independentes de cada componente.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SISTEMA ALPR                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐          │
│  │   Entrada    │    │   Detecção   │    │     OCR      │          │
│  │  (Câmera/    │───▶│   de Placa   │───▶│  (EasyOCR)   │          │
│  │   Arquivo)   │    │   (YOLOv8)   │    │              │          │
│  └──────────────┘    └──────────────┘    └──────────────┘          │
│         │                   │                   │                   │
│         │                   │                   │                   │
│         ▼                   ▼                   ▼                   │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │                    Pós-processamento                     │       │
│  │  (Validação de formato, correção, banco de dados)       │       │
│  └─────────────────────────────────────────────────────────┘       │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │                   Interface de Usuário                   │       │
│  │              (Streamlit / Terminal / API)                │       │
│  └─────────────────────────────────────────────────────────┘       │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 4.2 Estrutura de Diretórios do Código

```
src/
├── main.py                 # Ponto de entrada da aplicação
├── config.py               # Configurações globais
│
├── detection/
│   ├── __init__.py
│   ├── detector.py         # Classe de detecção com YOLO
│   └── preprocessing.py    # Pré-processamento de imagens
│
├── ocr/
│   ├── __init__.py
│   ├── recognizer.py       # Classe de OCR
│   └── postprocessing.py   # Validação e correção
│
├── utils/
│   ├── __init__.py
│   ├── visualization.py    # Funções de visualização
│   └── helpers.py          # Funções auxiliares
│
└── app/
    ├── __init__.py
    └── streamlit_app.py    # Interface web
```

## 4.3 Módulo de Detecção de Placas

### 4.3.1 Classe PlateDetector

```python
# src/detection/detector.py

from ultralytics import YOLO
import cv2
import numpy as np

class PlateDetector:
    """
    Classe responsável pela detecção de placas veiculares
    utilizando o modelo YOLOv8.
    """

    def __init__(self, model_path: str = "models/weights/best.pt"):
        """
        Inicializa o detector com o modelo treinado.

        Args:
            model_path: Caminho para os pesos do modelo YOLO
        """
        self.model = YOLO(model_path)
        self.confidence_threshold = 0.5

    def detect(self, image: np.ndarray) -> list:
        """
        Detecta placas na imagem fornecida.

        Args:
            image: Imagem em formato numpy array (BGR)

        Returns:
            Lista de dicionários com informações das detecções:
            [{'bbox': [x1, y1, x2, y2], 'confidence': float, 'plate_image': np.ndarray}]
        """
        results = self.model(image, conf=self.confidence_threshold)[0]

        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])

            # Recorta a região da placa
            plate_image = image[y1:y2, x1:x2]

            detections.append({
                'bbox': [x1, y1, x2, y2],
                'confidence': confidence,
                'plate_image': plate_image
            })

        return detections

    def detect_from_file(self, image_path: str) -> list:
        """
        Detecta placas a partir de um arquivo de imagem.

        Args:
            image_path: Caminho para o arquivo de imagem

        Returns:
            Lista de detecções
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
        return self.detect(image)
```

### 4.3.2 Pré-processamento de Imagens

```python
# src/detection/preprocessing.py

import cv2
import numpy as np

class ImagePreprocessor:
    """
    Classe para pré-processamento de imagens antes da detecção.
    """

    @staticmethod
    def resize(image: np.ndarray, max_size: int = 640) -> np.ndarray:
        """Redimensiona imagem mantendo proporção."""
        h, w = image.shape[:2]
        scale = max_size / max(h, w)
        if scale < 1:
            new_w, new_h = int(w * scale), int(h * scale)
            return cv2.resize(image, (new_w, new_h))
        return image

    @staticmethod
    def enhance_contrast(image: np.ndarray) -> np.ndarray:
        """Melhora o contraste usando CLAHE."""
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    @staticmethod
    def denoise(image: np.ndarray) -> np.ndarray:
        """Remove ruído da imagem."""
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
```

### 4.3.3 Treinamento do Modelo

O treinamento do YOLOv8 foi realizado utilizando o seguinte script:

```python
# scripts/train_detector.py

from ultralytics import YOLO

# Carrega modelo pré-treinado
model = YOLO('yolov8n.pt')  # nano version para velocidade

# Treina com dataset customizado
results = model.train(
    data='data/dataset.yaml',    # Configuração do dataset
    epochs=100,                   # Número de épocas
    imgsz=640,                    # Tamanho da imagem
    batch=16,                     # Batch size
    patience=20,                  # Early stopping
    device=0,                     # GPU
    workers=4,                    # Data loaders
    project='runs/train',        # Diretório de saída
    name='alpr_detector',        # Nome do experimento

    # Data augmentation
    hsv_h=0.015,                 # Variação de matiz
    hsv_s=0.7,                   # Variação de saturação
    hsv_v=0.4,                   # Variação de valor
    degrees=10.0,                # Rotação
    translate=0.1,               # Translação
    scale=0.5,                   # Escala
    flipud=0.0,                  # Não inverter verticalmente
    fliplr=0.5,                  # Inverter horizontalmente
)
```

**Arquivo de configuração do dataset** (`data/dataset.yaml`):

```yaml
# Dataset configuration
path: /path/to/dataset
train: images/train
val: images/val
test: images/test

# Classes
names:
  0: plate
```

## 4.4 Módulo de OCR

### 4.4.1 Classe PlateRecognizer

```python
# src/ocr/recognizer.py

import easyocr
import cv2
import numpy as np
from .postprocessing import PostProcessor

class PlateRecognizer:
    """
    Classe responsável pelo reconhecimento dos caracteres
    das placas utilizando EasyOCR.
    """

    def __init__(self, languages: list = ['pt', 'en']):
        """
        Inicializa o reconhecedor OCR.

        Args:
            languages: Lista de idiomas para reconhecimento
        """
        self.reader = easyocr.Reader(languages, gpu=True)
        self.postprocessor = PostProcessor()

    def preprocess_plate(self, plate_image: np.ndarray) -> np.ndarray:
        """
        Pré-processa a imagem da placa para melhorar OCR.

        Args:
            plate_image: Imagem recortada da placa

        Returns:
            Imagem pré-processada
        """
        # Redimensiona para tamanho adequado
        plate_image = cv2.resize(plate_image, (400, 130))

        # Converte para escala de cinza
        gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)

        # Aplica filtro bilateral para reduzir ruído
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)

        # Binarização adaptativa
        binary = cv2.adaptiveThreshold(
            filtered, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )

        return binary

    def recognize(self, plate_image: np.ndarray) -> dict:
        """
        Reconhece os caracteres da placa.

        Args:
            plate_image: Imagem da placa

        Returns:
            Dicionário com texto reconhecido e confiança
        """
        # Pré-processa a imagem
        processed = self.preprocess_plate(plate_image)

        # Executa OCR
        results = self.reader.readtext(processed)

        # Combina todos os textos detectados
        raw_text = ''.join([r[1] for r in results])
        avg_confidence = np.mean([r[2] for r in results]) if results else 0

        # Pós-processa o texto
        cleaned_text = self.postprocessor.clean_plate_text(raw_text)
        validated = self.postprocessor.validate_format(cleaned_text)

        return {
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'is_valid': validated,
            'confidence': avg_confidence
        }
```

### 4.4.2 Pós-processamento do OCR

```python
# src/ocr/postprocessing.py

import re

class PostProcessor:
    """
    Classe para pós-processamento e validação do texto reconhecido.
    """

    # Mapeamento de caracteres confundidos
    CHAR_CORRECTIONS = {
        'O': '0',  # Em posições numéricas
        '0': 'O',  # Em posições de letra
        'I': '1',
        '1': 'I',
        'S': '5',
        '5': 'S',
        'B': '8',
        '8': 'B',
        'G': '6',
        'Z': '2',
    }

    # Padrões de placas brasileiras
    PATTERN_OLD = r'^[A-Z]{3}[0-9]{4}$'           # ABC1234
    PATTERN_MERCOSUL = r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$'  # ABC1D23

    def clean_plate_text(self, text: str) -> str:
        """
        Limpa o texto removendo caracteres inválidos.

        Args:
            text: Texto bruto do OCR

        Returns:
            Texto limpo contendo apenas letras e números
        """
        # Remove espaços e caracteres especiais
        cleaned = re.sub(r'[^A-Za-z0-9]', '', text.upper())
        return cleaned

    def validate_format(self, text: str) -> bool:
        """
        Valida se o texto corresponde a um formato de placa válido.

        Args:
            text: Texto da placa

        Returns:
            True se formato válido, False caso contrário
        """
        if re.match(self.PATTERN_OLD, text):
            return True
        if re.match(self.PATTERN_MERCOSUL, text):
            return True
        return False

    def correct_characters(self, text: str) -> str:
        """
        Corrige caracteres baseado na posição esperada.

        Formato antigo: LLL NNNN (3 letras + 4 números)
        Formato Mercosul: LLL N L NN (3 letras + 1 número + 1 letra + 2 números)

        Args:
            text: Texto a ser corrigido

        Returns:
            Texto com caracteres corrigidos
        """
        if len(text) != 7:
            return text

        corrected = list(text)

        # Posições 0, 1, 2 devem ser letras
        for i in [0, 1, 2]:
            if corrected[i].isdigit():
                corrected[i] = self.CHAR_CORRECTIONS.get(corrected[i], corrected[i])

        # Posição 3 deve ser número
        if corrected[3].isalpha():
            corrected[3] = self.CHAR_CORRECTIONS.get(corrected[3], corrected[3])

        # Verifica se é padrão Mercosul (posição 4 é letra)
        # ou padrão antigo (posição 4 é número)

        return ''.join(corrected)

    def format_plate(self, text: str) -> str:
        """
        Formata a placa para exibição.

        Args:
            text: Texto da placa

        Returns:
            Texto formatado (ex: ABC-1234 ou ABC1D23)
        """
        if len(text) == 7:
            # Verifica se é Mercosul ou antigo
            if text[4].isalpha():  # Mercosul
                return text  # ABC1D23
            else:  # Antigo
                return f"{text[:3]}-{text[3:]}"  # ABC-1234
        return text
```

## 4.5 Pipeline Completo

### 4.5.1 Classe Principal

```python
# src/main.py

import cv2
import argparse
from detection.detector import PlateDetector
from ocr.recognizer import PlateRecognizer
from utils.visualization import draw_results

class ALPRSystem:
    """
    Sistema completo de reconhecimento automático de placas.
    """

    def __init__(self, model_path: str = "models/weights/best.pt"):
        """
        Inicializa o sistema ALPR.

        Args:
            model_path: Caminho para o modelo de detecção
        """
        self.detector = PlateDetector(model_path)
        self.recognizer = PlateRecognizer()

    def process_image(self, image) -> list:
        """
        Processa uma imagem e retorna as placas detectadas.

        Args:
            image: Imagem (numpy array) ou caminho para arquivo

        Returns:
            Lista de placas detectadas com texto e confiança
        """
        # Carrega imagem se for caminho
        if isinstance(image, str):
            image = cv2.imread(image)

        # Detecta placas
        detections = self.detector.detect(image)

        results = []
        for det in detections:
            # Reconhece caracteres
            ocr_result = self.recognizer.recognize(det['plate_image'])

            results.append({
                'bbox': det['bbox'],
                'detection_confidence': det['confidence'],
                'text': ocr_result['cleaned_text'],
                'ocr_confidence': ocr_result['confidence'],
                'is_valid': ocr_result['is_valid']
            })

        return results

    def process_video(self, source, display: bool = True):
        """
        Processa vídeo em tempo real.

        Args:
            source: Caminho do vídeo ou 0 para webcam
            display: Se True, exibe resultado em janela
        """
        cap = cv2.VideoCapture(source)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Processa frame
            results = self.process_image(frame)

            # Desenha resultados
            annotated = draw_results(frame, results)

            if display:
                cv2.imshow('ALPR System', annotated)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description='Sistema ALPR')
    parser.add_argument('--image', type=str, help='Caminho da imagem')
    parser.add_argument('--video', type=str, help='Caminho do vídeo')
    parser.add_argument('--webcam', action='store_true', help='Usar webcam')
    parser.add_argument('--model', type=str, default='models/weights/best.pt')

    args = parser.parse_args()

    system = ALPRSystem(args.model)

    if args.image:
        results = system.process_image(args.image)
        for r in results:
            print(f"Placa: {r['text']} | Confiança: {r['ocr_confidence']:.2f}")

    elif args.video:
        system.process_video(args.video)

    elif args.webcam:
        system.process_video(0)


if __name__ == '__main__':
    main()
```

## 4.6 Interface de Usuário

### 4.6.1 Aplicação Streamlit

```python
# src/app/streamlit_app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from main import ALPRSystem

st.set_page_config(
    page_title="Sistema ALPR",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Sistema de Reconhecimento de Placas")
st.markdown("---")

# Inicializa sistema
@st.cache_resource
def load_system():
    return ALPRSystem()

system = load_system()

# Sidebar
st.sidebar.header("Configurações")
confidence_threshold = st.sidebar.slider(
    "Confiança mínima", 0.0, 1.0, 0.5
)

# Upload de imagem
uploaded_file = st.file_uploader(
    "Envie uma imagem",
    type=['jpg', 'jpeg', 'png']
)

if uploaded_file is not None:
    # Converte para formato OpenCV
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Processa
    with st.spinner("Processando..."):
        results = system.process_image(image_bgr)

    # Exibe resultados
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagem Original")
        st.image(image, use_column_width=True)

    with col2:
        st.subheader("Placas Detectadas")
        if results:
            for i, r in enumerate(results):
                st.success(f"**Placa {i+1}:** {r['text']}")
                st.write(f"Confiança: {r['ocr_confidence']:.2%}")
                st.write(f"Formato válido: {'✅' if r['is_valid'] else '❌'}")
        else:
            st.warning("Nenhuma placa detectada")
```

## 4.7 Considerações do Capítulo

Este capítulo apresentou a implementação completa do sistema ALPR, desde a arquitetura geral até os detalhes de cada módulo. O código foi estruturado de forma modular, facilitando manutenção e testes. O próximo capítulo apresentará os resultados dos experimentos realizados.
