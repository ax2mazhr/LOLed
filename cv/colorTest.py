import cv2
import numpy as np
import time
import mss


with mss.mss() as sct:
  monitor = {"top": 240, "left": 1820, "width": 100, "height": 300}

while "Screen capturing":

        img_rgb = np.array(sct.grab(monitor))
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

        templateBaron = cv2.imread('template/baron.jpg',0)
        templateRift = cv2.imread('template/rift.jpg',0)
        templateCloud = cv2.imread('template/cloud.jpg',0)
        templateInfernal = cv2.imread('template/infernal.jpg',0)
        templateMountian = cv2.imread('template/mountain.jpg',0)
        templateOcean = cv2.imread('template/ocean.jpg',0)
        templateElder = cv2.imread('template/elder.jpg',0)
        w, h = templateBaron.shape[::-1]

        resBaron = cv2.matchTemplate(img_gray,templateBaron,cv2.TM_CCOEFF_NORMED)
        resRift = cv2.matchTemplate(img_gray,templateRift,cv2.TM_CCOEFF_NORMED)
        resCloud = cv2.matchTemplate(img_gray,templateCloud,cv2.TM_CCOEFF_NORMED)
        resInfernal = cv2.matchTemplate(img_gray,templateInfernal,cv2.TM_CCOEFF_NORMED)
        resMountain = cv2.matchTemplate(img_gray,templateMountian,cv2.TM_CCOEFF_NORMED)
        resOcean = cv2.matchTemplate(img_gray,templateOcean,cv2.TM_CCOEFF_NORMED)
        resElder = cv2.matchTemplate(img_gray,templateElder,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8

        if np.amax(resBaron) > threshold:
                print("Baron!")

        if np.amax(resRift) > threshold:
                print("Rift!")

        if np.amax(resCloud) > threshold:
                print("Cloud!")

        if np.amax(resInfernal) > threshold:
                print("Infernal!")

        if np.amax(resMountain) > threshold:
                print("Mountain!")

        if np.amax(resOcean) > threshold:
                print("Ocean!")

        if np.amax(resElder) > threshold:
                print("Elder!")

        loc = np.where(resBaron >= threshold )

        for pt in zip(*loc[::-1]):
            # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            print(img_rgb[pt[1], pt[0]-2, 2])
            print(img_rgb[pt[1], pt[0]-2, 1])
            print(img_rgb[pt[1], pt[0]-2, 0])

        #Blue = 59,93,130

        # team = img_rgb[pt[1],pt[0]-1]
        # cv2.imshow('Detected',team)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # cv2.imshow('Detected',img_rgb)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()