---

##  Wiring Guide for the DIY Macropad

This guide explains how to wire the buttons and potentiometers to your Arduino. It’s simple, and doesn’t require soldering.

### General Notes

* All buttons use `INPUT_PULLUP`, so no resistors are needed.
* Potentiometers connect to analog pins and give a 0–1023 value.
* You can use jumper wires and a breadboard. No soldering required.

---

### Buttons

* **Pins used:** `2` to `11` (digital)
* **Connection:**

  * One side of each button → Ground (GND)
  * Other side → Arduino digital pin (D2–D11)
* In code: set as `INPUT_PULLUP`

```
GND ----[Button]---- D2
GND ----[Button]---- D3
```

---

### 🎚️ Potentiometers

* **Pins used:** `A0` to `A3` (analog)
* **Connection:**

  * Middle pin → Analog pin (A0–A3)
  * One side pin → 5V
  * Other side pin → GND

```
5V ---- A0 ---- GND
```

---

### 🖼️ Diagram

---
