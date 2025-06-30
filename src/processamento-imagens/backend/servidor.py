from flask import Flask, request, jsonify
import cv2
import numpy as np
import easyocr
import re

app = Flask(__name__)
reader = easyocr.Reader(['en'], gpu=False)

def validar_placa(texto):
    padrao = r'^[A-Z]{3}[0-9][0-9A-Z][0-9]{2}$'
    texto = texto.replace('-', '').upper()
    return re.match(padrao, texto) is not None

@app.route('/processa_placa', methods=['POST'])
def processa_placa():
    try:
        imagem_bytes = request.data
        npimg = np.frombuffer(imagem_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'error': 'Imagem inválida'}), 400

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)

        resultados = reader.readtext(processed)
        placas = [r[1].upper().replace('-', '') for r in resultados if validar_placa(r[1])]

        if placas:
            return jsonify({'placa': placas[0]})
        return jsonify({'placa': 'Placa não detectada'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
