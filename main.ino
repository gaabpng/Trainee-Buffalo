const int pinPot = A0;

const int FSTLed = 2;
const int LSTLed = 13;
const int NLeds = LSTLed - FSTLed + 1;

int targetDirection = -1;
unsigned long startTime = 0;
bool waiting = false;
bool heldFor1Second = false;
unsigned long timeWithinZone = 0;

void setup() {
  Serial.begin(9600);
  for (int pin = FSTLed; pin <= LSTLed; pin++) {
    pinMode(pin, OUTPUT);
  }
  randomSeed(analogRead(A1));
  choseNewDirection();
}

void loop() {
  int read = analogRead(pinPot);

  // Definir os limites seguros: 20% e 80% da faixa do potenciômetro
  const int minRead = 205;  // ~20% de 1023
  const int maxRead = 818;  // ~80% de 1023

  // Restringir read aos limites definidos
  read = constrain(read, minRead, maxRead);

  // Mapear a faixa central para a quantidade de LEDs
  int steeringPos = map(read, minRead, maxRead, 0, NLeds - 1);

  turnOffAllLEDs();
  digitalWrite(FSTLed + steeringPos, HIGH);
  blinkTargetLED();

  if (waiting) {
    if (steeringPos == targetDirection) {
      if (!heldFor1Second) {
        timeWithinZone = millis();
        heldFor1Second = true;
      } else if (millis() - timeWithinZone >= 1000) {
        unsigned long reactionTime = millis() - startTime;
        //Serial.print("Reaction time (target position) ");
        //Serial.print(targetDirection + 1);
        //Serial.print("): ");
        Serial.print(reactionTime);
        //Serial.println(" ms");
        choseNewDirection();
      }
    } else {
      heldFor1Second = false;
    }
  }

  delay(10);
}

void choseNewDirection() {
  targetDirection = random(0, NLeds);
  startTime = millis();
  waiting = true;
  heldFor1Second = false;
  //Serial.print("Nova direção alvo: ");
  //Serial.println(targetDirection + 1);
}

void turnOffAllLEDs() {
  for (int pin = FSTLed; pin <= LSTLed; pin++) {
    digitalWrite(pin, LOW);
  }
}

void blinkTargetLED() {
  unsigned long now = millis();
  if ((now / 250) % 2 == 0) {
    digitalWrite(FSTLed + targetDirection, HIGH);
  } else {
    digitalWrite(FSTLed + targetDirection, LOW);
  }
}
