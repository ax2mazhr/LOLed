# *By: Ahmed Amgad :: http://ax2mproductions.com :: https://github.com/ax2mazhr/LOLed *
                            
import copy
import re
import cv2
import numpy as np
import time
import mss
import pytesseract
import serial

# Serial Comms
arduino = serial.Serial('COM4', 9600, timeout=1)

# Screen Capture
with mss.mss() as sct:
    eventsCrop = {"top": 240, "left": 1820, "width": 100, "height": 300}
    healthCrop = {"top": 1040, "left": 870, "width": 100, "height": 19}

# Templates
templateBaron = cv2.imread('template/baron.jpg', 0)
templateRift = cv2.imread('template/rift.jpg', 0)
templateCloud = cv2.imread('template/cloud.jpg', 0)
templateInfernal = cv2.imread('template/infernal.jpg', 0)
templateMountain = cv2.imread('template/mountain.jpg', 0)
templateOcean = cv2.imread('template/ocean.jpg', 0)
templateElder = cv2.imread('template/elder.jpg', 0)

# Vars
w, h = templateBaron.shape[::-1]
loc = -1
threshold = 0.8
currentEvent = [-1, -1]
lastEvent = [-1, -1]
lastEventTime = 0
hp = [0, 0]
lastHp = [0, 0]
dead = False

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

while "Screen capturing":

    # Screen Img Processing
    events_rgb = np.array(sct.grab(eventsCrop))
    events_gray = cv2.cvtColor(events_rgb, cv2.COLOR_BGR2GRAY)

    health_rgb = np.array(sct.grab(healthCrop))
    health_gray = cv2.cvtColor(health_rgb, cv2.COLOR_BGR2GRAY)
    width = int(health_gray.shape[1] * 200 / 100)
    height = int(health_gray.shape[0] * 200 / 100)
    health_gray = cv2.resize(health_gray, (width, height), interpolation = cv2.INTER_LINEAR)
    (thresh, health) = cv2.threshold(health_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    health = cv2.bitwise_not(health)
    kernel = np.ones((1, 1), np.uint8)
    health = cv2.erode(health, kernel, iterations=1)
    healthTxt = pytesseract.image_to_string(health)
    healthTxt = healthTxt.lower()
    if ("/" in healthTxt) and (not healthTxt.islower()):
        healthTxt = healthTxt.replace(" ", "")
        healthTxt = healthTxt.split("/")
        healthTxt[0] = re.sub("\D", "", healthTxt[0])
        healthTxt[1] = re.sub("\D", "", healthTxt[1])
        if len(healthTxt) == 2 and len(healthTxt[0]) > 0 and len(healthTxt[1]) > 0 :
            print(hp)
            hp[0] = int(healthTxt[0])
            hp[1] = int(healthTxt[1])
            if hp[0] == 0:
                dead = True
            else:
                dead = False

    # Template Matching
    resBaron = cv2.matchTemplate(events_gray, templateBaron, cv2.TM_CCOEFF_NORMED)
    resRift = cv2.matchTemplate(events_gray, templateRift, cv2.TM_CCOEFF_NORMED)
    resCloud = cv2.matchTemplate(events_gray, templateCloud, cv2.TM_CCOEFF_NORMED)
    resInfernal = cv2.matchTemplate(events_gray, templateInfernal, cv2.TM_CCOEFF_NORMED)
    resMountain = cv2.matchTemplate(events_gray, templateMountain, cv2.TM_CCOEFF_NORMED)
    resOcean = cv2.matchTemplate(events_gray, templateOcean, cv2.TM_CCOEFF_NORMED)
    resElder = cv2.matchTemplate(events_gray, templateElder, cv2.TM_CCOEFF_NORMED)

    # Assign Event
    if np.amax(resBaron) > threshold:
        currentEvent[1] = 0
        loc = np.where(resBaron >= threshold)

    if np.amax(resRift) > threshold:
        currentEvent[1] = 1
        loc = np.where(resRift >= threshold)

    if np.amax(resCloud) > threshold:
        currentEvent[1] = 2
        loc = np.where(resCloud >= threshold)

    if np.amax(resInfernal) > threshold:
        currentEvent[1] = 3
        loc = np.where(resInfernal >= threshold)

    if np.amax(resMountain) > threshold:
        currentEvent[1] = 4
        loc = np.where(resMountain >= threshold)

    if np.amax(resOcean) > threshold:
        currentEvent[1] = 5
        loc = np.where(resOcean >= threshold)

    if np.amax(resElder) > threshold:
        currentEvent[1] = 6
        loc = np.where(resElder >= threshold)

    # Check Team
    if loc != -1:
        for pt in zip(*loc[::-1]):
            if events_rgb[pt[1], pt[0] - 2, 0] > 100 and events_rgb[pt[1], pt[0] - 2, 2] < 80:
                # print("Blue")
                currentEvent[0] = 1
            elif events_rgb[pt[1], pt[0] - 2, 0] < 80 and events_rgb[pt[1], pt[0] - 2, 2] > 120:
                # print("Red")
                currentEvent[0] = 0
    loc = -1

    # Serial Write  1: FadeD / 2: FadeF / 3: FadeOn / 4: Glow / 10: Still

    # Death
    if dead:
        arduino.write("10,255,0,0.".encode())
        print("Dead ", hp)

    # Damage
    if hp[0] - lastHp[0] < 0 and abs(hp[0] - lastHp[0]) > 0.1 * hp[1]:
        arduino.write("2,255,0,0.".encode())
        print("Damage ", lastHp[0] - hp[0])
        lastHp = copy.deepcopy(hp)


    # Heal
    # if hp[0] - lastHp[0] > 0 and hp[0] - lastHp[0] > 0.2 * hp[1]:
    #     arduino.write("2,0,255,50.".encode())
    #     print("Heal ", hp[0] - lastHp[0])
    #     lastHp = copy.deepcopy(hp)


    # Objectives
    if (int(currentEvent[0]) != int(lastEvent[0]) or time.time() - lastEventTime > 3) and int(currentEvent[1]) != int(
            lastEvent[1]):
        # Blue Team
        if currentEvent[0] == 1:

            # Baron aad baron timer
            if currentEvent[1] == 0:
                arduino.write("3,255,0,255.".encode())
                arduino.write("4,255,0,255.".encode())
                print("Baron")

            # Rift
            if currentEvent[1] == 1:
                arduino.write("2,255,0,255.".encode())
                print("Rift")

            # Cloud
            elif currentEvent[1] == 2:
                arduino.write("1,255,255,255.".encode())
                print("Cloud")

            # Infernal
            elif currentEvent[1] == 3:
                arduino.write("1,255,10,0.".encode())
                print("Infernal")

            # Mountain
            elif currentEvent[1] == 4:
                arduino.write("1,255,150,0.".encode())
                print("Mountain")

            # Ocean
            elif currentEvent[1] == 5:
                arduino.write("1,0,150,255.".encode())
                print("Ocean")

            # Elder
            
            elif currentEvent[1] == 6:
                arduino.write("3,255,150,255.".encode())
                arduino.write("4,255,150,255.".encode())
                print("Elder")
     
            lastEvent = copy.deepcopy(currentEvent)
            lastEventTime = time.time()
