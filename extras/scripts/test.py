import ctypes
import os
from time import sleep

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint),
                ("dwTime", ctypes.c_ulong)]

def get_idle_duration():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        raise ctypes.WinError()
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

# Example usage
if __name__ == "__main__":
    while True:
        os.system('cls') if os.name == 'nt' else os.system('clear')
        idle_time = get_idle_duration()
        print(f"Time since last keyboard or mouse activity: {idle_time:.2f} seconds")
        sleep(1)
