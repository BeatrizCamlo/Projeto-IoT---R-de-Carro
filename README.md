***Projeto Ré Automotivo***

**UNIDADE I**  


O sistema de ré de um carro é responsável por identificar objetos atrás do carro e sinalizar ao montorista o qunato mais ele pode se aproximar sem causar danos ao carro e similarmente aos objetos próximos.

O projeto é composto por:
- 1 Arduino Uno;
- 3 Leds (Verde, Amarelo, Vermelho);
- 1 Sensor Ultrassônico;
- 1 Buzzer
- 1 Display LCD 16x2.

**Funcionamento do Projeto**  

O sensor ultrassonico é responsável por identifiar a distância e definir o comportamento dos leds. Se a distância identificada for maior que 300cm, o led verde pisca de forma lenta e é exibido no display a mensagem "Distância segura.". Caso a distância seja maior 50 a luz amarela pisca com maior frequência e é exibido no diplay a mensagem "Distância arriscada. Atenção!". Já para distânica menores que 50, o led vermelho fica acessa, o buzzer dispara e é exibida a mensagem no display "Distância intensa. Pare!".


**UNIDADE III - PROJETO FINAL**  

Para complementar as funcionalidades do Sensor de Ré Automotivo, serão adicionados:

- 1 Raspberry;
- Integração com API GPS;
- Integração com API de informações sobre o tempo;
- Processamento e publicação de imagens;
- Dashboard em Adafruit.

O projeto consiste na ampliação das funcionalidades de um sistema de Sensor de Ré Automotivo tradicional, transformando-o em uma solução inteligente IoT capaz de fornecer informações em tempo real sobre o ambiente ao redor do veículo. Essa solução será composta por sensores, processamento local com Raspberry Pi, coleta de dados via APIs e publicação em um dashboard online.
