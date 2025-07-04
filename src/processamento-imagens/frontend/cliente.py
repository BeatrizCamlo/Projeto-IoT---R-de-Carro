import time
import requests
import cv2
from io import BytesIO
from config_placa import ADAFRUIT_AIO_USERNAME, ADAFRUIT_AIO_KEY, NGROK_URL, FEED_NAME

def captura_imagem():
    camera = cv2.VideoCapture(0)  # Usa a webcam local
    ret, frame = camera.read()
    camera.release()
    if not ret:
        print("Erro ao capturar imagem.")
        return None
    _, img_encoded = cv2.imencode('.jpg', frame)
    return img_encoded.tobytes()

def obter_placa(imagem_bytes):
    try:
        r = requests.post(
            NGROK_URL + "/processa_placa",
            data=imagem_bytes,
            headers={'Content-Type': 'application/octet-stream'}
        )
        resultado = r.json()
        placa = resultado.get('placa', 'ERRO')
        return placa
    except Exception as e:
        print("Erro ao detectar placa:", e)
        return "ERRO"

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
    while True:
        imagem = captura_imagem()
        if imagem is None:
            time.sleep(5)
            continue

        placa = obter_placa(imagem)
        print("Placa detectada:", placa)
        if placa != "ERRO" and placa != "Placa não detectada":
            enviar_para_adafruit_io(placa)

        time.sleep(10)  # espera 10 segundos até a próxima captura

if __name__ == "__main__":
    main()
