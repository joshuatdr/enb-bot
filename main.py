import pyautogui
from time import sleep
from random import random
from playback import playActions, getStartingPos

def main():
    initialisePyAutoGui()
    countdownTimer()

    LOOP_REPETITIONS = 1
    for i in range(0, LOOP_REPETITIONS):
        if i > 0:
            # Wait for station interior to load, reset starting_pos
            randomWait(15)
            starting_pos = None

        # Start docked at Loki Station, get to our universal starting position
        # get_starting_pos() returns an integer which corresponds to the action script to be played
        starting_pos = getStartingPos('lokistation')
        if starting_pos == None:
            break
        playActions(f'lokistation\\start\\pos_{starting_pos}')
        randomWait(5)

        # Playback the steps to go to the trader, do the buying/selling, go back to the ship, fly to Earth Station
        playActions('lokistation\\goto_trader')
        randomWait(5)
        playActions('lokistation\\do_trading')
        randomWait(5)
        playActions('lokistation\\goto_ship')
        # Wait for station exterior to load
        randomWait(15)
        playActions('lokistation\\goto_earthstation')
        # Wait for interior to load
        randomWait(15)

        # Now docked at Earth Station, get to that starting position
        starting_pos = getStartingPos('earthstation')
        if starting_pos == None:
            break
        playActions(f'earthstation\\start\\pos_{starting_pos}')
        randomWait(5)

        # Playback the steps (as above), fly back to Loki Station
        playActions('earthstation\\goto_trader')
        randomWait(5)
        playActions('earthstation\\do_trading')
        randomWait(5)
        playActions('earthstation\\goto_ship')
        # Wait for station exterior to load
        randomWait(15)
        playActions('earthstation\\goto_lokistation')

        # Completed loop
        print('Completed loop')

def countdownTimer():
    # Countdown timer
    print('Starting', end='')
    for i in range(0, 5):
        print('.', end='')
        sleep(1)
    print('Go')

def initialisePyAutoGui():
    # Initialised PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0

def randomWait(minWait = 0.5):
    # Wait for (minWait) seconds with a random additional delay (0.0 - 0.5s)
    timeToWait = minWait + random() * 0.5
    print(f'Waiting {timeToWait:.3f} seconds')
    sleep(timeToWait)

if __name__ == '__main__':
    main()