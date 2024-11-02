import pyautogui
from time import sleep
from random import random
from playback import playActions

def main():
    initialisePyAutoGui()
    countdownTimer()

    # playActions('lokistation_goto_start')
    # randomWait(2)
    playActions('lokistation_goto_trader')
    randomWait(2)
    playActions('lokistation_do_trading')
    randomWait(2)
    playActions('lokistation_goto_ship')
    randomWait(15)
    playActions('lokistation_goto_earthstation')
    randomWait(2)

    # playActions('earthstation_goto_start')
    # randomWait(2)
    playActions('earthstation_goto_trader')
    randomWait(2)
    playActions('earthstation_do_trading')
    randomWait(2)
    playActions('earthstation_goto_ship')
    randomWait(15)
    playActions('earthstation_goto_lokistation')
    randomWait(2)

    # Done
    print('Done')

def initialisePyAutoGui():
    # Initialised PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0

def countdownTimer():
    # Countdown timer
    print('Starting', end='')
    for i in range(0, 5):
        print('.', end='')
        sleep(1)
    print('Go')

def randomWait(minWait = 0.5):
    # Wait for (minWait) seconds with a random additional delay (0.0 - 0.5s)
    timeToWait = minWait + random() * 0.5
    if (minWait > 0.1):
        print(f'Waiting {timeToWait:.3f} seconds')
    sleep(timeToWait)

if __name__ == '__main__':
    main()
    