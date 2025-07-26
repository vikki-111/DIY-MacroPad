---

#  DIY Macropad with Potentiometers

Hey!
This is a little project I made using some extra parts I had from my TEP class in college. It’s a simple macropad with mechanical switches and potentiometers that you can fully control via Python.

---

## What This Project Does

Basically, it’s a USB device made using an Arduino that:

* Detects button presses (like `BTN:0` when you press button 0)
* Reads analog values from potentiometers (like `POT:2:734` when pot 2 is moved)
* Sends all of that over serial to your computer

Then, a Python script on your computer interprets to the serial port and does whatever you want — like control system volume, launch stuff, or trigger keyboard shortcuts.

> This project was majorly inspired by **Project Deej**, which I first saw in a video by **Linus Tech Tips**.
---

## Hardware

* **Arduino Uno**
* **10 mechanical switches (I used Gateron reds)**
* **4 potentiometers**
* **Jumper wires(lots of 'em)**
* **breadboard**
* **PBT keycaps**

No soldering. No hot glue. The buttons just fit tightly into cut holes. Jumper wires can stay on well enough without glue, but you can add some if you want it more solid.

---

## 🛠️ Software Requirements

You'll need just a few things to get this running:

* **Arduino IDE** – To flash the `.ino` code to your Arduino

* **Python 3.8+** – For the script that interprets to serial and runs macros
  → Check by running `python --version` in your terminal

* **pip** – For installing dependencies listed in `requirements.txt`

---

---

##  How It Works

### Arduino Code

The microcontroller reads all the inputs and sends readable serial messages.

#### Buttons

* Wired with `INPUT_PULLUP`, so no external resistors needed
* Debounced using `delay(50)`
* Sends `BTN:0`, `BTN:1`, etc. when buttons are pressed

#### Potentiometers

* Connected to analog pins (A0–A3)
* Range: 0–1023
* Sends `POT:x:value` only when the value changes significantly (difference >10)

---
## Python Script 

The Python script:

    Listens to the serial port

    Parses lines like BTN:4 or POT:1:678

    Triggers functions or macros based on the input

You can bind these to:

    Volume controls

    App switching

    Copy/paste

    Media playback

    Any other custom macro

(You can customize this easily if you know Python)
---
## Setup & Usage

1. Flash the Arduino using the code in `macropad.ino`
2. Plug in your Macropad via USB
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
### Also checkout the wiring_guide for the connections they are really simple.
---
