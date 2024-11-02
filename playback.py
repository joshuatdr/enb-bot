import pyautogui
from time import sleep, time
from random import random
import json
import os

def main():
    initialisePyAutoGui()
    countdownTimer()

    playActions('actions_test_01')
    
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

def playActions(filename):
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir,
        'recordings\\enb',
        f'{filename}.json'
        )
    with open(filepath, 'r') as jsonfile:
        # Parse the JSON
        data = json.load(jsonfile)

        # Loop over each action
        for index, action in enumerate(data):
            # Account for time taken to read each action
            action_start_time = time()

            # Look for escape input to exit
            if action['button'] == 'Key.esc':
                break

            # Perform the action
            if action['type'] == 'keyDown':
                key = convertKey(action['button'])
                pyautogui.keyDown(key)
                print(f'keyDown on {key}')
            elif action['type'] == 'keyUp':
                key = convertKey(action['button'])
                pyautogui.keyUp(key)
                print(f'keyUp on {key}')
            elif action['type'] == 'click':
                pyautogui.click(action['pos'][0], action['pos'][1], duration=0.25)
                print(f'click on {action['pos']}')

            # Then sleep until next action should occur
            try:
                next_action = data[index + 1]
            except IndexError:
                break
            elapsed_time = next_action['time'] - action['time']

            if elapsed_time < 0:
                raise Exception('Unexpected action ordering')
            
            # Subtract the execution time
            elapsed_time -= (time() - action_start_time)
            if elapsed_time < 0:
                elapsed_time = 0
            print(f'Sleeping for {elapsed_time}')
            sleep(elapsed_time)

# Convert pynput keys into pyautogui keys
def convertKey(button):
    PYNPUT_SPECIAL_CASE_MAP = {
        'alt_l': 'altleft',
        'alt_r': 'altright',
        'alt_gr': 'altright',
        'ctrl_l': 'ctrlleft',
        'ctrl_r': 'ctrlright',
        'shift_l': 'shiftleft',
        'shift_r': 'shiftright',
    }

    # eg: 'Key.F9' should return 'F9', 'w' should return 'w'
    cleaned_key = button.replace('Key.', '')

    if cleaned_key in PYNPUT_SPECIAL_CASE_MAP:
        return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]

    return cleaned_key

if __name__ == '__main__':
    main()
    