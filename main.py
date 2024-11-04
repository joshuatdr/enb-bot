import pyautogui
import os
from time import sleep, time
from random import random
from playback import playActions, getStartingPos

def main():
    initialisePyAutoGui()

    STARTING_STATION = 'earth'
    LOOP_REPETITIONS = 1

    # Start from character selection screen
    # playActions('control\\charselect_start')

    for i in range(0, LOOP_REPETITIONS):
        if STARTING_STATION == 'loki':
            # Wait for interior to load
            waitLoadingScreen('dock')

            # Get to our universal starting position
            # get_starting_pos() returns an integer which corresponds to the action script to be played
            try:
                starting_pos = getStartingPos()
                sleep(10) # DEBUG: Check the position was recognised correctly
                playActions(f'lokistation\\start\\pos_{starting_pos}')
            except:
                # This is where we should run the reset script
                # ie. Log out to char select, log back in
                print('Starting position not recognised')
                sleep(10)
                playActions('control\\reset_position')
                continue

            # Playback the steps to go to the trader, do the buying/selling, go back to the ship
            randomWait(2)
            playActions('lokistation\\goto_trader')
            randomWait(2)
            playActions('lokistation\\do_trading')
            randomWait(2)
            playActions('lokistation\\goto_ship')

            # Wait for station exterior to load
            waitLoadingScreen()
            
            # Navigate to sector gate
            navigateInSpace('earth_sector_gate', (315, 308, 103, 27))

            # Watch for the gate jump icon to become active
            # Click it, then wait for the loading screen
            waitCondition('can_take_gate')
            pyautogui.click(771, 422, duration=0.25)
            waitLoadingScreen()

            # Navigate to Earth station
            navigateInSpace('earth_station', (207, 307, 21, 20))

            # Watch for the docking icon, click it
            waitCondition('can_dock')
            pyautogui.click(771, 422, duration=0.25)

        # Wait for interior to load
        # waitLoadingScreen('dock')

        # Now docked at Earth Station, get to that starting position
        try:
            starting_pos = getStartingPos()
            sleep(10) # DEBUG: Check the position was recognised correctly
            playActions(f'earthstation\\start\\pos_{starting_pos}')
        except:
            # This is where we should run the reset script
            # ie. Log out to char select, log back in
            print('Starting position not recognised')
            sleep(10)
            playActions('control\\reset_position')
            STARTING_STATION = 'earth'
            continue

        # Playback the steps to go to the trader, do the buying/selling, go back to the ship
        randomWait(2)
        playActions('earthstation\\goto_trader')
        randomWait(2)
        playActions('earthstation\\do_trading')
        randomWait(2)
        playActions('earthstation\\goto_ship')

        # Wait for station exterior to load
        waitLoadingScreen()
            
        # Navigate to sector gate
        navigateInSpace('loki_sector_gate', (217, 365, 98, 24))

        # Watch for the gate jump icon to become active
        # Click it, then wait for the loading screen
        waitCondition('can_take_gate')
        pyautogui.click(771, 422, duration=0.25)
        waitLoadingScreen()

        # Navigate to Loki station
        navigateInSpace('loki_station', (108, 334, 50, 50))

        # Watch for the docking icon, click it
        waitCondition('can_dock')
        pyautogui.click(771, 422, duration=0.25)

        # Completed loop
        STARTING_STATION = 'loki'
        print('Completed loop')

def initialisePyAutoGui():
    # Initialised PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0

def randomWait(minWait = 0.5):
    # Wait for (minWait) seconds with a random additional delay (0.0 - 0.5s)
    timeToWait = minWait + random() * 0.5
    print(f'Waiting {timeToWait:.3f} seconds')
    sleep(timeToWait)

def waitLoadingScreen(screen = None):
    loading = True
    # We call this immediately after finishing a script,
    # The loading screen might not have appeared yet, so we wait for it
    waitCondition('loading')
    print('Loading')
    while loading:
        sleep(0.1)
        if not pyautogui.pixelMatchesColor(679, 359, (99, 251, 255), tolerance=10):
            # Done loading
            break
    # Wait for ship landing animation
    if screen == 'dock':
        print('Waiting for ship to land')
        sleep(7)

def waitCondition(condition):
    if condition == 'loading':
        x, y = (679, 359)
        rgb = (99, 251, 255)
    elif condition == 'can_take_gate':
        x, y = (773, 424)
        rgb = (249, 249, 214)
    elif condition == 'can_dock':
        x, y = (771, 422)
        rgb = (250, 250, 216)
    else:
        raise Exception('Condition not recognised')
    found = False
    search_start_time = time()
    while not found:
        sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, rgb, tolerance = 10):
            break
        if (time() - search_start_time) > 60:
            debug_str = f'Pos: {(x, y)} RGB expected: {rgb} RGB actual: {pyautogui.pixel(x, y)}'
            raise Exception(f'Condition not met within timeout. Debug: {debug_str}')
        
def locateAndClick(needle, region):
    script_dir = os.path.dirname(__file__)
    location = pyautogui.locateOnScreen(f'{script_dir}\\needles\\{needle}.png', confidence = 0.8, region=region)
    coords = (int(location.left), int(location.top))
    print(f'{needle} located at {coords}')
    pyautogui.click(location)

def navigateInSpace(target, region):
    # Open navigational map, locate icon on screen within specified region and click it
    pyautogui.click(82, 569, duration=0.25)
    sleep(2)
    locateAndClick(f'{target}', region)
    # Wait for warp route to calculate, enter warp
    sleep(2.5)
    playActions('control\\enter_warp')

if __name__ == '__main__':
    main()