int LV1 = 47;
int LR1 = 49;
int BU1 = 51;
int ONOFF = 53;

void setup() {

  Serial.begin(9600);

  pinMode(LV1, OUTPUT);
  digitalWrite(LV1, HIGH);

  pinMode(LR1, OUTPUT);
  digitalWrite(LR1, HIGH);

  pinMode(BU1, OUTPUT);
  digitalWrite(BU1, HIGH);

  pinMode(ONOFF, OUTPUT);
  digitalWrite(ONOFF, HIGH);
  
}

void loop(){

  if (Serial.available()){
    // Lectura de caracteres
    int val = Serial.read();

    if (val == 'a') {
      digitalWrite(LV1, LOW);
    }

    else if (val == 'b') {
      digitalWrite(LR1, LOW);
    }

    else if (val == 'c') {
      digitalWrite(BU1, LOW);
    }

    else if (val == 'd') {
      digitalWrite(LV1, HIGH);
    }

    else if (val == 'e'){
      digitalWrite(LR1, HIGH);
    }

    else if (val == 'f'){
      digitalWrite(BU1, HIGH);
    }

    else if (val == 'x'){
      digitalWrite(ONOFF, LOW);
      delay(500)
      digitalWrite(ONOFF, HIGH);
    }

    else if (val == 'y'){
      digitalWrite(ONOFF, LOW);
    }

    else if (val == 'z'){
      digitalWrite(ONOFF, HIGH);
    }

    else{
      Serial.flush();
    }   
  }

};