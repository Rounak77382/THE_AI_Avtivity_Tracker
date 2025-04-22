'''
The code uses the cvzone library to detect the face landmarks of the user using the webcam.
The FaceMeshDetector class is used to detect the face landmarks.
The afkDetector function captures a frame from the webcam and uses the FaceMeshDetector to find the face landmarks.
It then calculates the vertical and horizontal distances between specific face landmarks.
The ratio of the vertical distance to the horizontal distance is calculated and used to determine if the user is sleeping or working.
If the ratio is less than 25, the user is considered to be sleeping, otherwise, they are considered to be working.
The function returns the status of the user (Sleeping, Working, or AFK) based on the calculated ratio.
'''

import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import time

detector = FaceMeshDetector(maxFaces=1)

def afkDetector():  
    cap = cv2.VideoCapture(0)
    success, img = cap.read()
    cap.release()
    
    

    if not success:
        return ("Failed to read frame from webcam")

    img, faces = detector.findFaceMesh(img, draw=True)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    
    if faces:
        
        lenghtVer, _ = detector.findDistance(faces[0][159], faces[0][23])
        lenghtHor, _ = detector.findDistance(faces[0][130], faces[0][243])

        ratio = int((lenghtVer / lenghtHor) * 100)

        return ("Sleeping" if ratio < 25 else "Working")
        # return ratio
        
    else:
        return ("AFK")
    
    
if __name__ == "__main__":
    
    while True:
        status = afkDetector()
        print(status)





    
    
    
    