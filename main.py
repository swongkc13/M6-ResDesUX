import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import subprocess
import platform

class CallInitiator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.start_time = None

    def run(self):
        """
        The main method that runs the detection loop.
        """
        while True:
            success, img = self.cap.read()
            hands, img = self.detector.findHands(img, flipType=True)

            if not hands:
                img = cv2.GaussianBlur(img, (95, 95), 0)

            if hands:
                self.handleHandDetection()

            self.showImage(img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        self.releaseResources()

    def handleHandDetection(self):
        """
        Handles the logic when a hand is detected.
        """
        print("Hand detected")
        if self.start_time is None:
            self.start_time = time.time()

        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 3:
                print("Call Initiated!")
                self.launchCall()

    def launchCall(self):
        """
        Launches the call application based on the platform.
        """
        if platform.system() == "Darwin":
            subprocess.run(["open", "-a", "zoom.us"])
        elif platform.system() == "Windows":
            subprocess.Popen("start zoom.us", shell=True)
        exit()

    def showImage(self, img):
        """
        Displays the image with text.
        """
        cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        text = "Welcome to VigilanTv"
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
        text_x = (img.shape[1] - text_size[0]) // 2
        cv2.putText(img, text, (text_x, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv2.LINE_AA)

        cv2.imshow("Image", img)

    def releaseResources(self):
        """
        Releases the resources (camera and windows).
        """
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    callInitiator = CallInitiator()
    callInitiator.run()
