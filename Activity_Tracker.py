'''
The code is a productivity tracker that tracks the active window on the user's computer and the time spent on each window.
It uses the pygetwindow library to get the active window and the time spent on each window.
The code also uses the ctypes library to get the idle time of the user.
The code uses the FaceMeshModule from the cvzone library to detect if the user is looking at the screen.
The code uses the subprocess library to run a laser.py script when the user is idle.
The code uses the csv library to read and write data to a CSV file.
The code uses the datetime library to get the current date and time.
The code uses the prettytable library to display the data in a tabular format.
'''

import time
import pygetwindow as gw
import os
import csv
import datetime
from prettytable import PrettyTable
import threading
import subprocess
import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import unicodedata
import csv
import os
import unicodedata
import ctypes
from wcwidth import wcwidth




app_dict = {}


global is_idle, idle_time
is_idle = False
idle_time = 0
global x


#variables
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
                #print(idle_signal)
                
                if idle_signal:
                    is_idle = True
                    subprocess.Popen(command, shell=False).wait()
                else:
                    is_idle = False
                    #user is just watching the screen
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
                    # Calculate the duration the previous window was active
                    duration = (time.time() - start_time) # - idle_threshold_seconds
                    print_activities(previous_window, duration)
                    previous_window = None  
                time.sleep(sleep_time)
                continue
            
            
            active_window = active.title.replace(',', '')
            
            previous_window = filer_data(previous_window) if previous_window else None
            
            active_window = filer_data(active_window)
                

            if active_window != previous_window: # If the active window has changed
                
        
                if previous_window:
                    duration = time.time() - start_time
                    print_activities(previous_window, duration)
                    
                start_time = time.time()
                previous_window = active_window
                
            time.sleep(sleep_time)
            
        except Exception as e:
            print(e)
            if previous_window:
                # Calculate the duration the previous window was active
                duration = time.time() - start_time
                print_activities(previous_window, duration)
                previous_window = None
            time.sleep(sleep_time)
            continue
        

def filer_data(window_title):
    # Find the index of the first opening bracket

    if window_title:
        window_title = str(window_title)
        opening_bracket_index = window_title.find("(")
        #print (window_title)

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
            width += 2  # Wide characters
        else:
            width += 1
    return width

def adjust_app_name(app_name):
    max_width = 100  # Adjust as needed
    
    truncated_width = 0
    truncated_name = ''
    for char in app_name:
        char_width = wcwidth(char)
        # Treat characters with a width of -1 as having a width of 1
        char_width = max(char_width, 1)
        if truncated_width + char_width > max_width - 3:  # Reserve space for ellipsis
            break
        truncated_name += char
        truncated_width += char_width
    if truncated_width > 0 and truncated_width < len(app_name):
        app_name = truncated_name + "..."
    return app_name

def print_csv_contents(path):
    global x
    
    if os.name == 'nt' and 'PROMPT' in os.environ:
        os.system('chcp 65001')
        
    with open(path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        rows = [row for row in reader if len(row) > 1]
        rows.sort(key=lambda x: float(x[1]), reverse=True)
        x = PrettyTable()
        x.field_names = ["Application Name", "Time Spent"]
        for row in rows:

            app_name = row[0]
            app_name = adjust_app_name(app_name)

              
            total_seconds = int(float(row[1]))
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            time_spent_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            x.add_row([app_name, time_spent_formatted])
    

    os.system('cls' if os.name == 'nt' else 'clear')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))    
    print(x)
            
        

def print_activities(app_name, duration):
    
    backup_name = app_name
    app_name = unicodedata.normalize('NFC', app_name)#.encode('ascii', 'ignore').decode('utf-8')
    
    while True:
        try:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            path = "./datas/" + current_date + ".csv"
            
        except Exception as e:
            print(e)
            print("Error fetching/creating file")
            time.sleep(sleep_time)
            continue
        break
    
    if not os.path.isfile(path):
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['name','time'])
    
    with open(path, mode="r+", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        writer = csv.writer(file)
        
        lines = list(reader)
        lines = [line for line in lines if line and not line[0].isdigit()]
        found = False
        for i, row in enumerate(lines):
            if len(row) > 0 and row[0] == app_name:
                duration += float(row[1])
                lines[i] = [app_name, duration]
                found = True
                break
        if not found:
            writer.writerow([app_name, duration])

        file.seek(0)
        writer.writerows(lines)
        
        
        print_csv_contents(path) 
        
                
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



