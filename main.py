import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import subprocess
import platform

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
start_time = None  # Initialize start_time as None

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=True)

    # Apply a very strong blur effect until a hand is detected
    if not hands:
        img = cv2.GaussianBlur(img, (95, 95), 0)  # Adjust the kernel size for a very strong blur

    if hands:
        print("Hand detected")

        if start_time is None:
            start_time = time.time()

    if start_time is not None:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 3:  # Reduce the time to 3 seconds
            print("Camera Activated")

            # Open the Zoom application
            if platform.system() == "Darwin":
                subprocess.run(["open", "-a", "zoom.us"])
            elif platform.system() == "Windows":
                subprocess.Popen("start zoom.us", shell=True)
            break

    # Make the window fullscreen
    cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Add larger "Welcome" text centered at the top
    text = "Welcome to VigilanTv"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    cv2.putText(img, text, (text_x, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)

    # Display video feed
    cv2.imshow("Image", img)

    # Check for key press to interrupt video capture
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
