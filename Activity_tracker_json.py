import time
import pygetwindow as gw
import os
import json
import datetime
from prettytable import PrettyTable
import threading
import subprocess
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import unicodedata
import ctypes
from wcwidth import wcwidth

app_dict = {}

global is_idle, idle_time
is_idle = False
idle_time = 0
global x

# variables
idle_threshold_seconds = 60
sleep_time = 1
no_of_confirmations = 5
exclusion_list = [None, "", "Start", "Windows Lock Screen"]

detector = FaceMeshDetector(maxFaces=1)

def afkDetector():
    cap = cv2.VideoCapture(0)
    success, img = cap.read()
    cap.release()

    if not success:
        return ("Failed to read frame from webcam")

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        lenghtVer, _ = detector.findDistance(faces[0][159], faces[0][23])
        lenghtHor, _ = detector.findDistance(faces[0][130], faces[0][243])

        ratio = int((lenghtVer / lenghtHor) * 100)

        return ("Sleeping" if ratio < 25 else "Working")
    else:
        return ("AFK")

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

def idle_detector():
    global idle_time, is_idle
    current_dir = os.path.dirname(os.path.abspath(__file__))
    laser_script_path = os.path.join(current_dir, "laser.py")
    command = ["pythonw", laser_script_path]

    while True:
        try:
            idle_time = get_idle_duration()
            if idle_time >= idle_threshold_seconds:
                for _ in range(no_of_confirmations):
                    if afkDetector() == "Working":
                        idle_signal = False
                        break
                    else:
                        idle_signal = True
                        time.sleep(sleep_time)
                if idle_signal:
                    is_idle = True
                    subprocess.Popen(command, shell=False).wait()
                else:
                    is_idle = False
                    time.sleep(idle_threshold_seconds)
            time.sleep(sleep_time)
        except Exception as e:
            print(e)
            time.sleep(sleep_time)
            continue

def track_activities():
    previous_window = None
    duration = 0
    global is_idle

    while True:
        try:
            active = gw.getActiveWindow()
            if active in exclusion_list or is_idle:
                if previous_window:
                    duration = (time.time() - start_time)
                    print_activities(previous_window, duration)
                    previous_window = None
                time.sleep(sleep_time)
                continue

            active_window = active.title.replace(',', '')

            previous_window = filer_data(previous_window) if previous_window else None

            active_window = filer_data(active_window)

            if active_window != previous_window:
                if previous_window:
                    duration = time.time() - start_time
                    print_activities(previous_window, duration)

                start_time = time.time()
                previous_window = active_window

            time.sleep(sleep_time)

        except Exception as e:
            print(e)
            if previous_window:
                duration = time.time() - start_time
                print_activities(previous_window, duration)
                previous_window = None
            time.sleep(sleep_time)
            continue

def filer_data(window_title):
    if window_title:
        window_title = str(window_title)
        opening_bracket_index = window_title.find("(")
        if opening_bracket_index != -1:
            closing_bracket_index = window_title.find(")", opening_bracket_index)
            if closing_bracket_index != -1:
                window_title = window_title[:opening_bracket_index] + window_title[closing_bracket_index + 1:].strip()
        return window_title
    return window_title

def get_display_width(s):
    width = 0
    for char in s:
        if unicodedata.east_asian_width(char) in ('F', 'W'):
            width += 2
        else:
            width += 1
    return width

import unicodedata
import wcwidth
import emoji

def adjust_app_name(app_name):
    max_width = 100
    truncated_width = 0
    truncated_name = ''
    app_name = ''.join(c for c in app_name if unicodedata.category(c)[0] != 'C' or emoji.is_emoji(c))
    for char in app_name:
        char_width = wcwidth.wcwidth(char)
        char_width = max(char_width, 1)
        if truncated_width + char_width > max_width - 3:
            break
        truncated_name += char
        truncated_width += char_width
    if truncated_width > 0 and truncated_width < len(app_name):
        app_name = truncated_name + "..."
    return app_name

def print_json_contents(path):
    global x
    print(path)
    if os.name == 'nt' and 'PROMPT' in os.environ:
        os.system('chcp 65001')

    try:
        with open(path, mode="r", encoding="ISO-8859-1") as file:
            data = json.load(file)
            print(data)
    except FileNotFoundError:
        print(f"The file {path} does not exist.")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {path}.")
        return

    data.sort(key=lambda x: float(x["time"]) if x["time"] is not None else 0, reverse=True)
    x = PrettyTable()
    x.field_names = ["Application Name", "Time Spent"]
    for entry in data:
        app_name = adjust_app_name(entry["name"].strip())
        total_seconds = int(float(entry["time"])) if entry["time"] is not None else 0
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_spent_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        x.add_row([app_name, time_spent_formatted])

    os.system('cls' if os.name == 'nt' else 'clear')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    total_time = sum(int(float(entry["time"])) if entry["time"] is not None else 0 for entry in data)
    hours = total_time // 3600
    minutes = (total_time % 3600) // 60
    seconds = total_time % 60
    total_time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    print(f"Total time spent on all applications: {total_time_formatted}")
    
    print(x)

def print_activities(app_name, duration):
    backup_name = app_name
    app_name = unicodedata.normalize('NFC', app_name)

    while True:
        try:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            path = "./new_datas/" + current_date + ".json"
        except Exception as e:
            print(e)
            print("Error fetching/creating file")
            time.sleep(sleep_time)
            continue
        break

    if not os.path.isfile(path):
        with open(path, mode="w", encoding="utf-8") as file:
            json.dump([], file)

    with open(path, mode="r+", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"1';'Error decoding JSON from the file {path}.")
            data = []

        found = False
        for entry in data:
            if entry["name"] == app_name:
                entry["time"] = str(float(entry["time"]) + duration)
                found = True
                break
        if not found:
            data.append({"name": app_name, "time": str(duration)})

        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)
    

    print_json_contents(path)

# Create threads for each function
track_thread = threading.Thread(target=track_activities)
idle_thread = threading.Thread(target=idle_detector)

# Set the threads as daemon threads
track_thread.daemon = True
idle_thread.daemon = True

# Start the threads
track_thread.start()
idle_thread.start()

# Wait for the main thread to finish
track_thread.join()
idle_thread.join()