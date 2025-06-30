import cv2
import requests
import time

# Configurações
NGROK_URL = "https://SEU_NGROK.ngrok-free.app"  # Atualize com seu URL ngrok

FEED_NAME = "placa-carro"

def captura_frame_rtsp(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Erro ao abrir stream RTSP")
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Erro ao capturar frame")
        return None
    return frame

def enviar_frame_para_servidor(frame):
    _, img_encoded = cv2.imencode('.jpg', frame)
    try:
        response = requests.post(
            NGROK_URL + "/processa_placa",
            data=img_encoded.tobytes(),
            headers={'Content-Type': 'application/octet-stream'}
        )
        return response.json()
    except Exception as e:
        print("Erro ao comunicar com o servidor:", e)
        return None

def enviar_para_adafruit_io(valor):
    url = f"https://io.adafruit.com/api/v2/{ADAFRUIT_AIO_USERNAME}/feeds/{FEED_NAME}/data"
    headers = {
        "X-AIO-Key": ADAFRUIT_AIO_KEY,
        "Content-Type": "application/json"
    }
    data = '{"value": "' + valor + '"}'
    try:
        r = requests.post(url, data=data, headers=headers)
        print("Enviado para Adafruit IO:", r.text)
    except Exception as e:
        print("Erro no Adafruit IO:", e)

def main():
    rtsp_url = "rtsp://USUARIO:SENHA@IP_DA_CAMERA:PORTA/caminho"  # Substitua com seu RTSP
    while True:
        frame = captura_frame_rtsp(rtsp_url)
        if frame is not None:
            resultado = enviar_frame_para_servidor(frame)
            print("Resposta do servidor:", resultado)
            if resultado and 'placa' in resultado:
                placa = resultado['placa']
                if placa != 'Placa não detectada':
                    enviar_para_adafruit_io(placa)
                else:
                    print("Nenhuma placa detectada para enviar ao Adafruit IO.")
            else:
                print("Resposta inválida do servidor.")
        else:
            print("Frame inválido, tentando novamente...")

        time.sleep(5)  # aguarda 5 segundos antes da próxima captura

if __name__ == "__main__":
    main()
