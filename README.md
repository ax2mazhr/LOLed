
## Description

League of Legends reactive immersion LED Lights based on-screen game action recognition using openCV.

With a combination of software and hardware, lights are triggered by the following events:
  * Team Drake kills (Cloud / Ocean / Infernal / Mountain)
  * Team Dragon kills
  * Team Baron kills
  * Team Rift Herald kills
  * Healing
  * Damage
  * Death


## Requirements
* PyCharm w/ openCV, numpy & pytesseract
* Arduino IDE
* LEDs 
* Arduino 


## Game Settings

* Borderless video mode
* 1920x1080
* Lowest HUD scale (0 or 1)
* Game notifications on the right (default)


## Instructions
1. Modify arduino code to match your IO and upload
2. Import "cv" project in pycharm
3. Modify arduino com port and other variables if necessary  
4. Run "recog"
5. Start the game and play normally 


## More info

* Watch: https://www.youtube.com/embed/RRQId2x32yo
* The arduino code uses plain pwm signals for the led strip and the FastLED library to control the other addressable LEDs 


## Notes

* The scripts are not in any way , shape or form a deployable stable product.
* The scripts where coded to match my devices preferences, thus it has a big chance it wont perform as expected for you.
![enter image description here](https://i.redd.it/63hule73jam01.jpg)
 * Dont point out bugs or bad practices , ik there are alot and i am sure you are great at whatever you want to complain about.

* (◕‿◕✿)



#ax2mproductions

