import serial
import subprocess
import time
import psutil
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER


# Customise Button controls in handle_buttons function
# Customise Potentiometer controls in handle_pot




# Note: Active apps can only be detected on Windows in my code
# Checking the OS
try:
    import win32gui
    import win32process

    WIN32_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    WIN32_AVAILABLE = False
    print("win32gui not available - active app detection disabled")

# Configuration - Change these to match your setup
SERIAL_PORT = 'COM10'  # Check Device Manager for your Arduino port
BAUD_RATE = 9600

print("Simple Macropad Controller")
print("Make sure you have: pip install pyserial psutil pycaw comtypes pywin32")


class MacropadController:
    def __init__(self):
        self.last_volumes = {}  # Track volumes to prevent jitter
        self.setup_audio()

    # Button Actions
    def handle_button(self, button_id):
        #Handle button presses
        actions = {
            0: lambda: self.toggle_program("notepad", "notepad"),
            1: lambda: self.toggle_program("calc", "calc"),
            2: lambda: self.launch_program("explorer"),
            3: lambda: self.toggle_program("chrome", "chrome"),
            4: lambda: self.toggle_program("discord", "discord"),
            5: lambda: self.toggle_program("spotify", "spotify"),
            6: lambda: self.launch_program("cmd"),
            7: lambda: self.toggle_program("mspaint","mspaint"),
            8: lambda: print("Button 8 - Add your action here"),
            9: lambda: print("Button 9 - Add your action here")
        }

        if button_id in actions:
            try:
                actions[button_id]()
            except Exception as e:
                print(f"Button {button_id} error: {e}")
        else:
            print(f"Unknown button: {button_id}")

    
    def handle_potentiometer(self, pot_id, value):
        # Handle volume knobs
        # Convert 0-1023 to 0-100 percentage
        percentage = int((value / 1023) * 100)

        # Reduce jitter - only update if change is significant
        if pot_id in self.last_volumes:
            if abs(percentage - self.last_volumes[pot_id]) < 2:
                return

        self.last_volumes[pot_id] = percentage

        # Pot assignments
        if pot_id == 0:
            # Pot 0: Master Volume
            self.set_master_volume(percentage)

        elif pot_id == 1:
            # Pot 1: Brave Browser
            self.set_app_volume("brave", percentage)

        elif pot_id == 2:
            # Pot 2: Current Active App
            active_app = self.get_active_app()
            if active_app:
                self.set_app_volume(active_app, percentage)
            else:
                print(f"Pot 2 ({percentage}%): No active app detected")

        elif pot_id == 3:
            # Pot 3: Available for custom assignment
            print(f"Pot 3: {percentage}% (assign to your preferred app)")

        else:
            print(f"Potentiometer {pot_id}: {percentage}% (not assigned)")    
    
    def setup_audio(self):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.master_volume = cast(interface, POINTER(IAudioEndpointVolume))
            print("Audio control ready")
        except Exception as e:
            print(f"Audio setup failed: {e}")
            self.master_volume = None

    def set_master_volume(self, percentage):
        """Set master volume (0-100)"""
        if self.master_volume and 0 <= percentage <= 100:
            volume_level = percentage / 100.0
            self.master_volume.SetMasterVolumeLevelScalar(volume_level, None)
            print(f"Master Volume: {percentage}%")

    def set_app_volume(self, app_name, percentage):
        #Set volume for specific app (0-100)
        if not (0 <= percentage <= 100):
            return

        sessions = AudioUtilities.GetAllSessions()
        found = False

        for session in sessions:
            if session.Process and session.Process.name():
                process_name = session.Process.name().lower()
                if app_name.lower() in process_name:
                    try:
                        # Use ISimpleAudioVolume for per-app control
                        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        volume_level = percentage / 100.0
                        volume.SetMasterVolume(volume_level, None)
                        print(f"{app_name.title()} Volume: {percentage}%")
                        found = True
                        break
                    except Exception as e:
                        print(f"Error setting {app_name} volume: {e}")
                        continue

        if not found:
            print(f"{app_name.title()} not found or not playing audio")

    def get_active_app(self):
        #Get the currently active application
        if not WIN32_AVAILABLE:
            return None

        try:
            # Get current window
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                # Get process ID
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                # Get process name
                process = psutil.Process(pid)
                return process.name().lower().replace('.exe', '')
        except Exception:
            return None
        return None

    def is_program_running(self, program_name):
        # Check if a program is running
        for proc in psutil.process_iter(['name']):
            try:
                if program_name.lower() in proc.info['name'].lower():
                    return True
            except:
                continue
        return False

    def kill_program(self, program_name):
        # Close a program
        killed = False
        for proc in psutil.process_iter(['name']):
            try:
                if program_name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    killed = True
            except:
                continue
        return killed

    def launch_program(self, command):
        # Launch a program
        try:
            subprocess.Popen(command, shell=True)
            return True
        except:
            return False

    def toggle_program(self, program_name, launch_command):
        # Toggle a program on/off
        if self.is_program_running(program_name):
            if self.kill_program(program_name):
                print(f"Closed {program_name}")
            else:
                print(f"Failed to close {program_name}")
        else:
            if self.launch_program(launch_command):
                print(f"Opened {program_name}")
            else:
                print(f"Failed to open {program_name}")




def main():
    controller = MacropadController()

    try:
        print("Connecting to Arduino...")
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected on {SERIAL_PORT}")
        time.sleep(2)  # Let Arduino initialize
        print("Macropad ready! Press buttons or turn knobs.")

        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()

                    if line.startswith("BTN:"):
                        button_id = int(line.split(":")[1])
                        print(f"Button {button_id} pressed")
                        controller.handle_button(button_id)

                    elif line.startswith("POT:"):
                        parts = line.split(":")
                        pot_id = int(parts[1])
                        value = int(parts[2])
                        controller.handle_potentiometer(pot_id, value)

                    elif line == "READY":
                        print("Arduino connected and ready")

                except (ValueError, IndexError):
                    print(f"Invalid data: {line}")

    except serial.SerialException as e:
        print(f"Connection error: {e}")
        print("Check your COM port and Arduino connection")

    except Exception as e:
        print(f"Unexpected error: {e}")



if __name__ == "__main__":
    main()
