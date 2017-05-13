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
# Identify the device file number to send the tap event.
event_num = pad.get_input_event_num(device)

while True:

    # Take a screenshot and save it to a shared folder.
    pad.get_screen(device)

    # Tap the screen by pattern matching with the template image.
    # send_tap_event() can tap faster than tap().
    if pad.find_img(device, './img/title.png'):
        pad.send_tap_event(device, pad.LATEST_MATCH_LOC, event_num)

    # It is possible to set a threshold value of pattern matching.
    if pad.find_img(device, './img/ok.png', threshold=0.998):
        pad.send_tap_event(device, pad.LATEST_MATCH_LOC, event_num)

    # It is also possible to trim template images for faster processing.
    if pad.find_img(device, './img/next.png', trim=(240, 100, 360, 220)):
        pad.send_tap_event(device, pad.LATEST_MATCH_LOC, event_num)
```
