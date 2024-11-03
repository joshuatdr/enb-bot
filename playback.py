import pyautogui
from time import sleep, time
from natsort import natsorted
import json
import os

def main():
    # Initialised PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0
    playActions('actions_test_01')
    print('Done')

def playActions(filename):
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir,
        'recordings',
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

def getStartingPos(station):
    script_dir = os.path.dirname(__file__)
    # Get list of needle image filenames by station
    needles = os.listdir(f'{script_dir}\\needles\\{station}\\start')
    # Sort the filenames numerically (by default python sorts lexicographically: 1, 10, 11, 2 etc...)
    images_to_check = natsorted(needles)
    
    # Loop over images until one is found, then return the index (+1)
    for index, image_filename in enumerate(images_to_check):
        needle_path = os.path.join(
            script_dir,
            f'needles\\{station}\\start',
            image_filename
            )
        try:
            image_pos = pyautogui.locateOnScreen(image=needle_path, confidence=0.99, region=(0,0,806,629))
            if image_pos:
                print(f'found starting position: pos_{index + 1}')
                return index + 1
        # This is necessary to prevent pyautogui from stopping the script by throwing an ImageNotFoundException
        except:
            pass
    print('unable to determine starting position')
    return None

if __name__ == '__main__':
    main()
    