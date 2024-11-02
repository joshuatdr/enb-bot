from pynput import mouse, keyboard
from time import time
import json
import os

OUTPUT_FILENAME = 'actions_test_01'
# Declare mouse_listener globally so that keyboard on_release can stop it
mouse_listener = None
# Declare our start_time globally so that the callback functions can reference it
start_time = None
# Keep track of unreleased keys to prevent over-reporting press events
unreleased_keys = []
# Store all input events
input_events = []

class EventType():
    KEYDOWN = 'keyDown'
    KEYUP = 'keyUp'
    CLICK = 'click'

def main():
    runListeners()
    print('Recording duration: {:.3f} seconds'.format(elapsed_time()))
    global input_events
    print(json.dumps(input_events))

    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(
        script_dir,
        'recordings',
        '{}.json'.format(OUTPUT_FILENAME)
        )
    with open(filepath, 'w') as outfile:
        json.dump(input_events, outfile, indent=4)

def elapsed_time():
    global start_time
    return time() - start_time

def record_event(event_type, event_time, button, pos=None):
    global input_events
    input_events.append({
        'time': event_time,
        'type': event_type,
        'button': str(button),
        'pos': pos
    })

    if event_type == EventType.CLICK:
        print('{} on {} pos {} at {}'.format(event_type, button, pos, event_time))
    else:
        print('{} on {} at {}'.format(event_type, button, event_time))

def on_press(key):
    # Ignore if key already pressed
    global unreleased_keys
    if key in unreleased_keys:
        return
    else:
        unreleased_keys.append(key)

    try:
        record_event(EventType.KEYDOWN, elapsed_time(), key.char)
    except AttributeError:
        record_event(EventType.KEYDOWN, elapsed_time(), key)

def on_release(key):
    # Mark key as no longer pressed
    global unreleased_keys
    try:
        unreleased_keys.remove(key)
    except ValueError:
        print('ERROR: {} not in unreleased_keys'.format(key))

    try:
        record_event(EventType.KEYUP, elapsed_time(), key.char)
    except AttributeError:
        record_event(EventType.KEYUP, elapsed_time(), key)

    if key == keyboard.Key.esc:
        # Stop mouse listener
        global mouse_listener
        mouse_listener.stop()
        # Stop keyboard listener
        raise keyboard.Listener.StopException()
    
def on_click(x, y, button, pressed):
    if not pressed:
        record_event(EventType.CLICK, elapsed_time(), button, (x, y))

def runListeners():
    # Collect mouse input events
    global mouse_listener
    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()
    mouse_listener.wait() # Run listener in a separate thread (non-blocking)

    # Collect keyboard inputs until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        global start_time
        start_time = time()
        listener.join()

if __name__ == '__main__':
    main()