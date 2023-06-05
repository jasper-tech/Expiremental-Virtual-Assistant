import pywhatkit as pw
from time import sleep
import pyautogui as pt
import pyperclip as pc


# mouse click workaround
class Wp:
    # Defines the starting values
    def __init__(self, speed=.5, click_speed=.3):
        self.speed = speed
        self.click_speed = click_speed
        self.message = ''
        self.last_message = ''

    # Navigate the green dot for new messages
    def nav_green_dot(self):
        try:
            position = pt.locateOnScreen('green_dot.png', confidence=.7)
            pt.moveTo(position[0:2], duration=self.speed)
            pt.moveRel(-100, 0, duration=self.speed)
            pt.doubleClick(interval=self.click_speed)
        except Exception as e:
            print('Exception(nav_green_dot): ', e)

    wa_bot = Wp(speed=.5, click_speed=.4)
    sleep(5)
    wa_bot.nav_green_dot()
