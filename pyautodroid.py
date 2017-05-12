# -*- coding: utf-8 -*-
'''Android UI Testing Module for Nox App Player'''

import os
from subprocess import Popen, PIPE, call
import cv2

ADB_PATH = 'C:/Program Files (x86)/Nox/bin/nox_adb.exe'
SHARED_DIR = os.getenv('HOMEPATH')+'/Nox_share'
LATEST_MATCH_LOC = [0, 0]

def find_img(device, temp, threshold=0.97, trim=(0, 0, 0, 0)):
    file_id = device.replace(':', '_')
    img = cv2.imread(SHARED_DIR+'/Image/screen'+file_id+'.png', 1)

    if trim != (0, 0, 0, 0):
        img = img[trim[1]:trim[3], trim[0]:trim[2]]

    template = cv2.imread(temp, 1)
    (h, w, d) = template.shape

    # Apply template Matching
    try:
        matches = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matches)
    except:
        print('## OpenCV Error ##')
        return False

    if max_val > threshold:
        LATEST_MATCH_LOC[0] = trim[0] + int(max_loc[0] + w/2)
        LATEST_MATCH_LOC[1] = trim[1] + int(max_loc[1] + h/2)
        #print "  ", temp, "= (", LATEST_MATCH_LOC, ")"
        #print "  max_val", max_val
        return True
    else:
        return False

def find_imgs(device, temp, maxLen=10, threshold=0.97, trim=(0, 0, 0, 0)):
    matchList = []
    file_id = device.replace(':', '_')
    img = cv2.imread(SHARED_DIR+'/Image/screen'+file_id+'.png', 1)

    if trim != (0, 0, 0, 0):
        img = img[trim[1]:trim[3], trim[0]:trim[2]]

    template = cv2.imread(temp, 1)
    (h, w, d) = template.shape

    # Apply template Matching
    matches = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)

    for y in range(matches.shape[0]):
        for x in range(matches.shape[1]):
            if matches[y][x] > threshold:
                flag = True
                for element in matchList:
                    distance = (element[0]-x)**2 + (element[1]-y)**2
                    if 5**2 > distance:
                        flag = False
                        break
                if flag:
                    matchList.append((x, y))
                if len(matchList) >= maxLen:
                    return map(lambda p: (trim[0] + int(p[0] + w/2), trim[1] + int(p[1] + h/2)), matchList)
    return map(lambda p: (trim[0] + int(p[0] + w/2), trim[1] + int(p[1] + h/2)), matchList)

def tap(device, loc, duration=''):
    call(ADB_PATH+' -s '+device+' shell input tap '+str(loc[0])+' '+str(loc[1])+' '+str(duration))
    return

def swipe(device, src, dst, duration=500):
    call(ADB_PATH+' -s '+device+' shell input swipe '+str(src[0])+' '+str(src[1])+' '+str(dst[0])+' '+str(dst[1])+' '+str(duration))
    return

def send_tap_event(device, loc, event_num):
    call(ADB_PATH+' -s '+device+' shell "'
        +'sendevent /dev/input/event'+str(event_num)+' 1 330 1;'
        +'sendevent /dev/input/event'+str(event_num)+' 3 58 1;'
        +'sendevent /dev/input/event'+str(event_num)+' 3 53 '+str(loc[0])+';'
        +'sendevent /dev/input/event'+str(event_num)+' 3 54 '+str(loc[1])+';'
        +'sendevent /dev/input/event'+str(event_num)+' 0 2 0;'
        +'sendevent /dev/input/event'+str(event_num)+' 0 0 0;'
        +'sendevent /dev/input/event'+str(event_num)+' 0 2 0;'
        +'sendevent /dev/input/event'+str(event_num)+' 0 0 0;'
        +'sendevent /dev/input/event'+str(event_num)+' 1 330 0;'
        +'sendevent /dev/input/event'+str(event_num)+' 3 58 0;'
        +'sendevent /dev/input/event'+str(event_num)+' 3 53 '+str(loc[0])+';'
        +'sendevent /dev/input/event'+str(event_num)+' 3 54 '+str(loc[1])+';'
        +'sendevent /dev/input/event'+str(event_num)+' 0 2 0;'
        +'sendevent /dev/input/event'+str(event_num)+' 0 0 0;"'
    )
    return

def open_activity(device, url_scheme):
    call(ADB_PATH+' -s '+device+' shell am start '+url_scheme)
    return

def pull(device, remote, local='.'):
    call(ADB_PATH+' -s '+device+' pull "'+remote+'" "'+local+'"')
    return

def push(device, local, remote):
    call(ADB_PATH+' -s '+device+' push "'+local+'" "'+remote+'"')
    return

def stop_app(device, package):
    call(ADB_PATH+' -s '+device+' shell am force-stop '+package)
    return

def get_screen(device, path='/mnt/shared/Image/'):
    file_id = device.replace(':', '_')
    call(ADB_PATH+' -s '+device+' shell screencap -p '+path+'screen'+file_id+'.png')
    return

def get_input_event_num(device):
    p = Popen([ADB_PATH, '-s', device, 'shell', 'getevent'], stdout=PIPE)

    line = ""
    while True:
        line = p.stdout.readline().strip()
        if "Android Input" in line.decode('utf-8'):
            break
        buf = line
    p.kill()
    return buf.decode('utf-8')[-1]
