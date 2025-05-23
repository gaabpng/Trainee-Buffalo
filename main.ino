const int pinoPot = A0; 

const int primeiroLed = 2;
const int ultimoLed = 13;
const int numLeds = ultimoLed - primeiroLed + 1;

int direcaoAlvo = -1;
unsigned long tempoInicio = 0;
bool esperando = false;
bool mantidoPor1Segundo = false;
unsigned long tempoDentroZona = 0;

void setup() {
  Serial.begin(9600);
  for (int pino = primeiroLed; pino <= ultimoLed; pino++) {
    pinMode(pino, OUTPUT);
  }
  randomSeed(analogRead(A1));
  escolherNovaDirecao();
}

void loop() {
  int leitura = analogRead(pinoPot);
  int posVolante = map(leitura, 0, 1023, 0, numLeds - 1);
  apagarTodosLEDs();
  digitalWrite(primeiroLed + posVolante, HIGH);
  piscarLedAlvo();

  if (esperando) {
    if (posVolante == direcaoAlvo) {
      if (!mantidoPor1Segundo) {
        tempoDentroZona = millis();
        mantidoPor1Segundo = true;
      } else if (millis() - tempoDentroZona >= 1000) {
        unsigned long tempoReacao = millis() - tempoInicio;
        Serial.print("Tempo de reação (posição alvo ");
        Serial.print(direcaoAlvo + 1);
        Serial.print("): ");
        Serial.print(tempoReacao);
        Serial.println(" ms");
        escolherNovaDirecao();
      }
    } else {
      mantidoPor1Segundo = false;
    }
  }
  delay(10);
}

void escolherNovaDirecao() {
  direcaoAlvo = random(0, numLeds);
  tempoInicio = millis();
  esperando = true;
  mantidoPor1Segundo = false;
  Serial.print("Nova direção alvo: ");
  Serial.println(direcaoAlvo + 1);
}

void apagarTodosLEDs() {
  for (int pino = primeiroLed; pino <= ultimoLed; pino++) {
    digitalWrite(pino, LOW);
  }
}

void piscarLedAlvo() {
  unsigned long agora = millis();
  if ((agora / 250) % 2 == 0) {
    digitalWrite(primeiroLed + direcaoAlvo, HIGH);
  } else {
    digitalWrite(primeiroLed + direcaoAlvo, LOW);
  }
}
