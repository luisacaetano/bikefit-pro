"""
Script de teste do WebSocket com webcam
Executa análise de pose em tempo real e mostra latência
"""
import cv2
import asyncio
import websockets
import json
import base64
import time
import sys

# Configurações
WS_URL = "ws://localhost:8000/ws/video"
CAMERA_INDEX = 0  # 0 = webcam padrão, mude se usar Camo
SIDE = "right"  # ou "left"


async def test_websocket():
    """Testa conexão WebSocket com frames da webcam"""

    print("=" * 50)
    print("  BikeFit Pro - Teste de WebSocket")
    print("=" * 50)
    print()

    # Abrir webcam
    print(f"[1/4] Abrindo câmera (índice {CAMERA_INDEX})...")
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print("❌ Erro: Não foi possível abrir a câmera")
        print("   Verifique se o Camo está conectado")
        print("   Ou tente mudar CAMERA_INDEX no script")

        # Listar câmeras disponíveis
        print("\n   Testando câmeras disponíveis:")
        for i in range(5):
            test_cap = cv2.VideoCapture(i)
            if test_cap.isOpened():
                print(f"   - Câmera {i}: disponível")
                test_cap.release()
        return

    # Configurar resolução
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"✅ Câmera aberta: {width}x{height}")

    # Conectar ao WebSocket
    print(f"\n[2/4] Conectando ao WebSocket...")
    print(f"   URL: {WS_URL}")

    try:
        async with websockets.connect(WS_URL) as ws:
            print("✅ WebSocket conectado!")

            print(f"\n[3/4] Iniciando análise (lado: {SIDE})...")
            print("   Pressione 'q' na janela do vídeo para sair")
            print("   Pressione 's' para salvar um frame")
            print()

            frame_count = 0
            latencies = []
            last_fps_time = time.time()
            fps_count = 0

            while True:
                # Capturar frame
                ret, frame = cap.read()
                if not ret:
                    print("❌ Erro ao capturar frame")
                    break

                # Codificar frame em base64
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                frame_base64 = base64.b64encode(buffer).decode('utf-8')

                # Enviar para o servidor
                start_time = time.time()
                await ws.send(json.dumps({
                    "type": "frame",
                    "data": f"data:image/jpeg;base64,{frame_base64}",
                    "side": SIDE
                }))

                # Receber resposta
                response = await ws.recv()
                latency = (time.time() - start_time) * 1000  # em ms
                latencies.append(latency)

                result = json.loads(response)
                frame_count += 1
                fps_count += 1

                # Calcular FPS a cada segundo
                if time.time() - last_fps_time >= 1.0:
                    fps = fps_count
                    fps_count = 0
                    last_fps_time = time.time()
                else:
                    fps = fps_count

                # Mostrar frame processado ou original
                display_frame = frame.copy()

                if result.get("frame"):
                    # Decodificar frame processado do servidor
                    frame_data = result["frame"].split(",")[1]
                    frame_bytes = base64.b64decode(frame_data)
                    import numpy as np
                    nparr = np.frombuffer(frame_bytes, np.uint8)
                    display_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                # Adicionar informações na tela
                info_text = f"FPS: {fps} | Latencia: {latency:.0f}ms"
                cv2.putText(display_frame, info_text, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Mostrar ângulos se detectados
                if result.get("angles"):
                    angles = result["angles"]
                    y_pos = 60
                    for key, value in angles.items():
                        if value is not None and key != "side_analyzed":
                            text = f"{key}: {value:.1f}°"
                            cv2.putText(display_frame, text, (10, y_pos),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                            y_pos += 25

                # Mostrar status
                if result.get("recommendations"):
                    status = result["recommendations"].get("overall_status", "")
                    color = (0, 255, 0) if status == "optimal" else (0, 255, 255) if status == "minor_adjustments" else (0, 0, 255)
                    cv2.putText(display_frame, f"Status: {status}", (10, height - 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                # Exibir frame
                cv2.imshow("BikeFit Pro - Teste WebSocket", display_frame)

                # Verificar teclas
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    filename = f"frame_{int(time.time())}.jpg"
                    cv2.imwrite(filename, display_frame)
                    print(f"   Frame salvo: {filename}")

            # Estatísticas finais
            print("\n[4/4] Estatísticas:")
            print(f"   Frames processados: {frame_count}")
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                min_latency = min(latencies)
                max_latency = max(latencies)
                print(f"   Latência média: {avg_latency:.1f}ms")
                print(f"   Latência min: {min_latency:.1f}ms")
                print(f"   Latência max: {max_latency:.1f}ms")

                if avg_latency < 100:
                    print("   ✅ Latência OK (< 100ms)")
                elif avg_latency < 200:
                    print("   ⚠️  Latência aceitável (< 200ms)")
                else:
                    print("   ❌ Latência alta (> 200ms)")

    except websockets.exceptions.ConnectionRefused:
        print("❌ Erro: Não foi possível conectar ao WebSocket")
        print("   Verifique se o backend está rodando:")
        print("   cd backend && source venv/bin/activate && uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    print()
    asyncio.run(test_websocket())
    print()
