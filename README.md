# pyAutoDroid

## Description
Android UI Testing Module for Nox App Player

## Requirements
Nox App Player (V3.8.0.0 or later)  
OpenCV 3.0

## Usage
`import pyautodroid`

## Example
```
import pyautodroid as pad

device = '127.0.0.1:62001'

while True:

    # Take a screenshot and save it to a shared folder.
    pad.get_screen(device)

    # Identify the device file number to send the tap event.
    event_num = pad.get_input_event_num(device)

    # Tap the screen by pattern matching with the template image.
    # send_tap_event() can tap faster than tap().
    if pad.find_img(device, './img/title.png'):
        pad.send_tap_event(device, pad.LATEST_MATCH_LOC, event_num)

    if pad.find_img(device, './img/ok.png'):
        pad.send_tap_event(device, pad.LATEST_MATCH_LOC, event_num)

    if pad.find_img(device, './img/skip.png'):
        pad.send_tap_event(device, pad.LATEST_MATCH_LOC, event_num)

    if pad.find_img(device, './img/next.png'):
        pad.send_tap_event(device, pad.LATEST_MATCH_LOC, event_num)
```
