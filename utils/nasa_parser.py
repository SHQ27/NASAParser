#!NasaParser.py

import os
import time
from pprint import pprint
from PIL import Image, ImageDraw, ImageFilter
from selenium_base import selenium_base
from selenium.webdriver.common.action_chains import ActionChains

def failure_logging(func):
    #Prevents test failure and logs failed asteroids
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            nasaParser = args[0]
            failedAsteroidLog = './log/failed-asteroids.txt'
            with open(failedAsteroidLog, 'a') as log:
                log.write(nasaParser.asteroidFileName + "\n")

    return inner_func


class NASAParser():

    def __init__(self, asteroidName, sleepTime = 20):
        #Initializer
        self.asteroidName = asteroidName
        self.asteroidFileName = asteroidName.replace(' ', '_')[:-1]
        self.sleepTime = sleepTime
        self.getAsteroidImage()

    @failure_logging
    def getAsteroidImage(self):
        baseURL = "https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr="+self.asteroidName+"&view=VOP"

        #Get to iframe
        selenium = selenium_base.SeleniumBase()
        self.selenium = selenium
        selenium.driver.set_window_size(1400, 790)
        selenium.open(baseURL)
        time.sleep(self.sleepTime)
        frame = selenium.getElementBy('tag', 'iframe')
        actions = ActionChains(selenium.driver)
        actions.move_to_element(frame).perform();
        coords = {
            'x' :  82,
            'y' :  180,
            'width' :  1900,
            'height' :  1300
        }

        #Take screenshot
        self.screenshot = selenium.getElementScreenshot(frame, self.asteroidFileName, coords)
        selenium.close()
        #Edit screenshot
        self.eraseImperfections()

    def eraseImperfections(self):
        #Hamburger
        blackSmall = Image.open('./utils/black-small.png')
        blackBig = Image.open('./utils/black-big.png')
        self.screenshot.paste(blackSmall)
        orbitPath = './images/orbits/' + self.asteroidFileName + '.png'
        self.screenshot.save(orbitPath)

        #Canvas controls
        editedScreenshot = Image.open(orbitPath)
        editedScreenshot.paste(blackBig, (1442, 0), blackBig)
        editedScreenshot.show()
        editedScreenshot.save(orbitPath)

    def __del__(self):
        #Cleanup original screenshot
        originalScreenshotPath = './images/screenshots/' + self.asteroidFileName + '.png'
        screenshotExists = os.path.isfile(originalScreenshotPath)
        if (screenshotExists):
            os.remove(originalScreenshotPath)


