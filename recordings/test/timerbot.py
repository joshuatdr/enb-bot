import pyautogui
from time import sleep
from random import random

def main():
    initialisePyAutoGui()
    countdownTimer()

    goToMerchant()
    tradeWithMerchant()
    returnToShip()
    flyToEarthStation()

    # Done
    print('Done')

def initialisePyAutoGui():
    # Initialised PyAutoGUI
    pyautogui.FAILSAFE = True

def countdownTimer():
    # Countdown timer
    print('Starting', end='')
    for i in range(0, 10):
        print('.', end='')
        sleep(1)
    print('Go')

def randomWait(minWait = 0.5):
    # Wait for (minWait) seconds with a random additional delay (0.0 - 0.5s)
    timeToWait = minWait + random() * 0.5
    if (minWait > 0.1):
        print(f'Waiting {timeToWait:.3f} seconds')
    sleep(timeToWait)

def holdKey(key, seconds=1):
    # Simulate random keypress duration
    keyDuration = seconds + random() * 0.01
    print(f'Pressing {key} key for {keyDuration:.3f} seconds')
    pyautogui.keyDown(key)
    sleep(keyDuration)
    pyautogui.keyUp(key)
    # Wait before next command
    randomWait()

def moveMouseAndClick(x_pos, y_pos):
    # Take 200-300ms to move the mouse
    moveDuration = 0.2 + random() * 0.1
    pyautogui.moveTo(x_pos, y_pos, moveDuration)
    # Wait 100-200ms before clicking
    clickDelay = 0.2 + random() * 0.1
    sleep(clickDelay)
    # Click at position
    print(f'Clicking at [{x_pos}, {y_pos}]')
    pyautogui.click()
    # Wait before next command
    randomWait()

def reportMousePosition(seconds=5):
    for i in range(0, seconds):
        print(pyautogui.position())
        sleep(1)

def goToMerchant():
    # Back away from Louden MacEwen
    holdKey('s', 6)
    # Face the entrance
    holdKey('a', 0.1)
    # Go through the entrance into the main lobby
    holdKey('w', 7)
    # Turn to the bazaar lobby
    holdKey('d', 0.65)
    # Go through the entrance into the bazaar lobby
    holdKey('w', 5.6)
    # Turn to the trade merchant
    holdKey('d', 1.16)
    # Walk up to the trade merchant
    holdKey('w', 1.5)

def tradeWithMerchant():
    # Interact with the merchant
    moveMouseAndClick(600, 260)
    # Wait for dialog to appear
    randomWait(3)
    # Click on trade
    moveMouseAndClick(375, 540)
    randomWait(1)

    # Buy the item
    numToBuy = 10
    pyautogui.moveTo(672, 277)
    pyautogui.keyDown('shiftleft')
    for i in range(0, numToBuy):
        pyautogui.click()
        randomWait(0.1)
    pyautogui.keyUp('shiftleft')

    # Click the close button
    moveMouseAndClick(785, 220)

    # Click the done button and wait for animation
    moveMouseAndClick(242, 514)
    randomWait(2.5)

def returnToShip():
    # Change our body angle
    holdKey('a', 0.2)
    # Backup to center of the bazaar
    holdKey('s', 2.65)
    # Turn to the exit
    holdKey('d', 0.08)
    # Go through the exit back into the main lobby
    holdKey('w', 5.76)
    # Turn to the hangar
    holdKey('a', 0.68)
    # Go through the exit into the hangar
    holdKey('w', 6.2)
    # Turn towards our ship
    holdKey('a', 0.3)
    # Click our ship to exit the station
    moveMouseAndClick(376, 199)
    # Allow time for the outside world to load
    randomWait(10)

def flyToEarthStation():
    # Open the navigation map
    moveMouseAndClick(84, 569)
    # Select the sector gate to Earth
    moveMouseAndClick(370, 325)
    # Wait for warp path to be calculated
    randomWait(1.5)
    # Initiate warp
    holdKey('z', 0.1)
    # Wait for warp to finish
    randomWait(36)
    # Enter the gate
    moveMouseAndClick(772, 427)
    # Wait for the sector change to load
    randomWait(17)
    # Open the navigation map
    moveMouseAndClick(84, 569)
    # Select Earth Station
    moveMouseAndClick(217, 318)
    # Wait for warp path to be calculated
    randomWait(1)
    # Initiate warp
    holdKey('z', 0.1)
    # Wait for warp to finish
    randomWait(17)
    # Dock at the station
    moveMouseAndClick(774, 427)

if __name__ == '__main__':
    main()
    