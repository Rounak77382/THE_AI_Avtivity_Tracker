# Activity Tracker

## Data Set

The data set used in this project can be found in the datas directory. It contains collected user process data over time, which the Activity Tracker uses to analyze user activity patterns.

## Introduction

**Activity Tracker** is a Python project designed to monitor and analyze user activity based on running processes. It collects data about user processes, organizes it, and provides tools for further analysis. The main script is `Activity_Tracker.py`, which runs the tracking operations.

This project is useful for understanding software usage patterns, detecting idle times, and can be extended for productivity analysis or user behavior studies.

## Technologies

This project is built with:

- **Python 3:** The primary programming language used for scripting and process management.
- **[OpenCV](https://opencv.org/):** An open-source computer vision library used for image and video processing.
- **[CVZone](https://github.com/cvzone/cvzone):** A computer vision library that simplifies tasks in OpenCV.
- **[Dlib](http://dlib.net/):** A toolkit for machine learning providing algorithms for facial recognition and other features.
- **Other Python Libraries:** Such as `os`, `json`, `time`, `random`, and more as specified in the code.

## Project Setup

To set up the project, follow these steps:

1. **Clone the Repository:**

```sh
git clone <repository_url>
```

2. **Navigate to the Project Directory:**

```sh
cd Activity_Tracker
```

3. **Install Required Dependencies:**

If there is a `requirements.txt` file, run:

```sh
pip install -r requirements.txt
```

If there's no `requirements.txt`, install dependencies manually:

```sh
pip install opencv-python cvzone dlib
```

4. **Install Dlib Wheel File (Windows Users):**

If you are using Windows and encounter issues installing Dlib, download the appropriate `dlib` wheel file (e.g., `dlib-19.22.99-cp37-cp37m-win_amd64.whl`) and install it using:

```sh
pip install dlib-19.22.99-cp37-cp37m-win_amd64.whl
```

5. **Run the Activity Tracker:**

Execute the main script to start tracking:

```sh
python Activity_Tracker.py
```

## Usage

The Activity Tracker script monitors running processes on your computer and collects data at regular intervals. It stores this data in the `datas` directory in JSON format.

### Scripts Overview

- **Activity_Tracker.py:** Main script for tracking user activity.
- **Activity_sorter.py:** Processes and sorts the collected data.
- **calcproductivity.py:** Calculates productivity metrics based on the data.
- **datachanger.py:** Modifies and formats the data for analysis.
- **datamerger.py:** Merges multiple data files into a single dataset.
- **afkdetector2.py:** Detects periods when the user is away from the keyboard.

### Data Directories and Files

- **datas:** Contains raw data files collected by the tracker.
- **new_datas:** Contains processed data files.
- **`final_data_set.json`:** The merged and cleaned dataset ready for analysis.
- **false_processes.txt & true_processes.txt:** Lists of processes categorized as non-productive and productive, respectively.

