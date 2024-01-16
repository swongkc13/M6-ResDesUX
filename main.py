import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import subprocess

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
start_time = time.time()

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        print("Hand detected")

    elapsed_time = time.time() - start_time
    if elapsed_time >= 5:
        print("Camera Activated")

        # Open the website using Chrome
        subprocess.run(["open", "-a", "Google Chrome", "https://www.politie.nl/"])
        break

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
