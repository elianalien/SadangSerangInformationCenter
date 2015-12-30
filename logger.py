__author__ = 'Chairun R Siregar'

import time
import datetime

class Logger():

    def __init__(self):
        self.crntDate = time.strftime("%Y-%m-%d")

        # log app start
        self.log("\nas", " ---- APP STARTED ---")

    def log(self, type = "..", string = ""):
        self.f = open('./log/' + self.crntDate + '.txt', 'a')

        self.f.write(type + " " + time.strftime("%H:%M:%S") + string + "\n")
        self.la = datetime.datetime.now() # record last activity

        self.f.close()

    # log autochek pas idle
    def log_check(self):
        self.log("..", "      .")

    # log tiap screen berubah
    def log_screen_change(self, screen):
        self.log("\nsc", " -- :" + screen + " --")

    # log kalo suatu button ditekan
    # masukin string untuk namanya
    def log_button(self, button = "unnamed"):
        self.log("bp", "      pressed :" + str(button))

    # log tiap ada touch
    def log_touch(self, pos):
        self.log("td", "      touched on :" + str(pos))

    # log tiap touch diangkat
    # cuma dicatet kalo touch lebih lama dari 0.2 detik
    def log_touch_up(self, pos):
        dif = datetime.datetime.now() - self.la
        dif = dif.total_seconds()
        if dif > 0.2:
            self.log("tu", "      -> up after " + str(dif) + " s on :"+ str(pos))

    # log tiap auto standby (karena idle 1 menit)
    def log_standby(self):
        self.log("as", " -- Auto Standby --")
