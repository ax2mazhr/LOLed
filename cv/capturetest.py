import time
import cv2
import mss
import numpy as np

with mss.mss() as sct:
    # Part of the screen to capture
    # monitor = {"top": 1040, "left": 870, "width": 100, "height": 19}
    monitor = {"top": 200, "left": 575, "width": 775, "height": 600}

    while "Screen capturing":
        last_time = time.time()
        # Get raw pixels from the screen, save it to a Numpy array
        health_rgb = np.array(sct.grab(monitor))


        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", health)
        cv2.imshow("OpenCV/Numpy normal", health_rgb)

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break
