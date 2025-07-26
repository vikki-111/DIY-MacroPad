// Simple Macropad Arduino Code
// Works with the Python controller

// Pin definitions - adjust these to match your wiring
const int BUTTON_PINS[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11}; // 10 buttons
const int POT_PINS[] = {A0, A1, A2, A3}; // 4 potentiometers
const int NUM_BUTTONS = 10;
const int NUM_POTS = 4;

// Button state tracking
bool buttonStates[NUM_BUTTONS];
bool lastButtonStates[NUM_BUTTONS];

// Potentiometer tracking
int potValues[NUM_POTS];
int lastPotValues[NUM_POTS];
const int POT_THRESHOLD = 10; // Minimum change to register

void setup() {
  Serial.begin(9600);
  
  // Setup button pins
  for (int i = 0; i < NUM_BUTTONS; i++) {
    pinMode(BUTTON_PINS[i], INPUT_PULLUP);
    buttonStates[i] = HIGH;
    lastButtonStates[i] = HIGH;
  }
  
  // Initialize potentiometer values
  for (int i = 0; i < NUM_POTS; i++) {
    potValues[i] = analogRead(POT_PINS[i]);
    lastPotValues[i] = potValues[i];
  }
  
  delay(1000);
  Serial.println("READY");
}

void loop() {
  // Check buttons
  for (int i = 0; i < NUM_BUTTONS; i++) {
    buttonStates[i] = digitalRead(BUTTON_PINS[i]);
    
    // Button pressed (goes from HIGH to LOW due to pullup)
    if (buttonStates[i] == LOW && lastButtonStates[i] == HIGH) {
      Serial.print("BTN:");
      Serial.println(i);
      delay(50); // Simple debounce
    }
    
    lastButtonStates[i] = buttonStates[i];
  }
  
  // Check potentiometers
  for (int i = 0; i < NUM_POTS; i++) {
    potValues[i] = analogRead(POT_PINS[i]);
    
    // Only send if change is significant
    if (abs(potValues[i] - lastPotValues[i]) > POT_THRESHOLD) {
      Serial.print("POT:");
      Serial.print(i);
      Serial.print(":");
      Serial.println(potValues[i]);
      lastPotValues[i] = potValues[i];
    }
  }
  
  delay(10); // Small delay to prevent flooding
}
