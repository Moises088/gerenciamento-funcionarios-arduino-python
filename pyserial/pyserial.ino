/*
@autor K. Michalsky
 Created on 2015.07.12
 
 Keypad
 Display pushed key in serial monitor
*/

const int numRows = 4;       // Rows in keypad
const int numCols = 4;       // Columns in Tastatur
const int debounceTime = 50; // Time in milliseconds to stabilize key signal
const int ledPin =  13;
const int ledPinGreen =  10;

// Keymap defines chars for each key
const char keymap[numRows][numCols] = {
  { '1', '2', '3' },
  { '4', '5', '6' },
  { '7', '8', '9' },
  { '*', '0', '#' }
};

// Arrays definition for the Arduino Pins
const int rowPins[numRows] = {9, 8, 7, 6};
const int colPins[numCols] = {5, 4, 3, 2};

void setup() {
  Serial.begin(9600);                        // Open Serial Port
  for (int row = 0; row < numRows; row++) {
    pinMode(rowPins[row],INPUT);             // Switch Pins for Rows as input
    digitalWrite(rowPins[row],HIGH);         // Activate Pullups
  }
  for (int column = 0; column < numCols; column++) {
    pinMode(colPins[column],OUTPUT);         // Switch Pins for Columns as input
    digitalWrite(colPins[column],HIGH);      // Columns are inactive
  }

  pinMode(ledPin, OUTPUT);
  pinMode(ledPinGreen, OUTPUT);
  pinMode(11,OUTPUT);
}

void loop() {
  int valor_recebido;
  valor_recebido = Serial.read();
 
  if(valor_recebido == '1')
  {
      digitalWrite(ledPin, HIGH);
      tom(11,1500,400); //LA
      digitalWrite(ledPinGreen, LOW);
  }
  if(valor_recebido == '2')
  {
      digitalWrite(ledPin, LOW);
      digitalWrite(ledPinGreen, LOW);
  }
  if(valor_recebido == '3')
  {
      digitalWrite(ledPin, LOW);
      digitalWrite(ledPinGreen, HIGH);
      tom(11,1500,400); //LA
      delay(400);
      tom(11,1500,400); //LA
  }
  
  char key = getKey();
  if( key != 0) {                  // if key was pushed
    Serial.println(key);           // display key
    delay(10);                     // wait 10ms for next input
  }
}

// getKey() returns pushed key or 0 if no key was pushed
char getKey(){
  char key = 0;                                     // 0 means no key was pushed
  for(int column = 0; column < numCols; column++) {
    digitalWrite(colPins[column],LOW);              // Activate column. 
    for(int row = 0; row < numRows; row++){         // Test for all raws if key was pushed.
      if(digitalRead(rowPins[row]) == LOW){         // key pushed? 
        delay(debounceTime);                        // Stabilize signal 
        while(digitalRead(rowPins[row]) == LOW) ;   // Wait for key to be released
        key = keymap[row][column];                  // Put char of pushed key in variable key
      } 
    }
    digitalWrite(colPins[column],HIGH);             // Activate column 
  }
  return key;                                       // return key or 0
}

void tom(char pino, int frequencia, int duracao){
  float periodo = 1000.0/frequencia; //Periodo em ms
  for (int i = 0; i< duracao/(periodo);i++){ //Executa a rotina de dentro o tanta de vezes que a frequencia desejada cabe dentro da duracao
    digitalWrite(pino,HIGH);
    delayMicroseconds(periodo*500); //Metade do periodo em ms
    digitalWrite(pino, LOW);
    delayMicroseconds(periodo*500);
  }
}
