#define redPin 9
#define greenPin 6
#define bluePin 5

#include <FastLED.h>
#define LED_PIN     7
#define NUM_LEDS    70
CRGB leds[NUM_LEDS];

void setup() {
  pinMode(redPin,OUTPUT);
  pinMode(greenPin,OUTPUT);
  pinMode(bluePin,OUTPUT);
  digitalWrite(redPin,HIGH);
  digitalWrite(greenPin,HIGH);
  digitalWrite(bluePin,HIGH);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  for (int i = 0; i <= 69; i++) {
  leds[i] = CRGB ( 0, 0, 255);
  FastLED.show();
  delay(20);
  }
  delay(1000);
  reset();
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()){
      int cmd = Serial.parseInt();
      if(cmd == 10){
        still();
      }
      else if(cmd == 1){
        fadeD();
      }
      else if(cmd == 2){
        fadeF();
      }
      else if(cmd == 3){
        fadeOn();
      }
      else if(cmd == 4){
        glow();
      }
    }
}

void still() {
   int Rval = Serial.parseInt(); 
   int Gval = Serial.parseInt(); 
   int Bval = Serial.parseInt(); 
   fill_solid(leds, NUM_LEDS, CRGB(Rval,Gval,Bval));
   FastLED.show();
   analogWrite(redPin,Rval);
   analogWrite(greenPin,Gval);
   analogWrite(bluePin,Bval);
   
  }
  
void reset() {
  analogWrite(redPin,0);
  analogWrite(greenPin,0);
  analogWrite(bluePin,0);
  FastLED.clear();
  FastLED.show();
  }

 void fadeD(){
  double i = double(Serial.parseInt())/255;
  double j = double(Serial.parseInt())/255;
  double k = double(Serial.parseInt())/255;
  for(double c = 0;c<255;c++){
    analogWrite(redPin,c*i);
    analogWrite(greenPin,j*c);
    analogWrite(bluePin,k*c);
    fill_solid(leds, NUM_LEDS, CRGB(c*i,c*j,c*k));
    FastLED.show();
    delay(1);
  }
  delay(500);
  for(double c = 255;c>0;c--){
    analogWrite(redPin,i*c);
    analogWrite(greenPin,j*c);
    analogWrite(bluePin,k*c);
    fill_solid(leds, NUM_LEDS, CRGB(c*i,c*j,c*k));
    FastLED.show();
    delay(10);
  } 
}

void fadeOn(){
  double i = double(Serial.parseInt())/255;
  double j = double(Serial.parseInt())/255;
  double k = double(Serial.parseInt())/255;
  for(double c = 0;c<255;c++){
    analogWrite(redPin,c*i);
    analogWrite(greenPin,j*c);
    analogWrite(bluePin,k*c);
    fill_solid(leds, NUM_LEDS, CRGB(c*i,c*j,c*k));
    FastLED.show();
    delay(5);
  }
}

void fadeF(){
  double i = double(Serial.parseInt())/255;
  double j = double(Serial.parseInt())/255;
  double k = double(Serial.parseInt())/255;
  for(double c = 0;c<255;c++){
    analogWrite(redPin,c*i);
    analogWrite(greenPin,j*c);
    analogWrite(bluePin,k*c);
    fill_solid(leds, NUM_LEDS, CRGB(c*i,c*j,c*k));
    FastLED.show();
    delay(1);
  }
  delay(100);
  for(double c = 255;c>0;c--){
    analogWrite(redPin,i*c);
    analogWrite(greenPin,j*c);
    analogWrite(bluePin,k*c);
    fill_solid(leds, NUM_LEDS, CRGB(c*i,c*j,c*k));
    FastLED.show();
    delay(1);
  } 
  reset();
}

void glow(){
  double i = double(Serial.parseInt())/255;
  double j = double(Serial.parseInt())/255;
  double k = double(Serial.parseInt())/255;
  while(Serial.available()< 3){
    for(double c = 255;c>55;c--){
      analogWrite(redPin,i*c);
      analogWrite(greenPin,j*c);
      analogWrite(bluePin,k*c);
      fill_solid(leds, NUM_LEDS, CRGB(c*i,c*j,c*k));
      FastLED.show();
      delay(5);
    } 
    for(double c = 55;c<255;c++){
      analogWrite(redPin,c*i);
      analogWrite(greenPin,j*c);
      analogWrite(bluePin,k*c);
      fill_solid(leds, NUM_LEDS, CRGB(c*i,c*j,c*k));
      FastLED.show();
      delay(5);
    }
  }
}
