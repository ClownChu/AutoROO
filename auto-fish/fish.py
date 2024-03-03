# -*- coding: utf-8 -*-
from helpers.logger import logger, loggerMapClicked
from os import listdir, makedirs, path
from random import randint
from random import random
import cv2 as cv2
import numpy as np
import mss
import time
import sys
import yaml
import pydirectinput
import win32api, win32con, win32gui, win32ui
import ctypes, os

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

if isAdmin() == False:
    print('Running script as administrator')
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    exit(0)

if not path.exists('logs'):
    makedirs('logs')

# Load config file.
stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)
ct = c['threshold']
interval_between_moves_and_clicks = c['time_intervals']['interval_between_moves_and_clicks']
pydirectinput.PAUSE = interval_between_moves_and_clicks

fish = """
==============================================================================================================================
████████████████████████████████████████████████████▓▓▓▓▓▓▓▓██████████▓▓██████████████████████████████████████████████████████
████████████████████████████████████████████████████▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▒▒▓▓▓▓▓▓▓▓██████████████████████████████████████
████████████████████████████████████████████████▓▓▓▓▓▓▒▒▒▒▒▒▓▓▒▒▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒▓▓▓▓▓▓▓▓████████████████████████████▓▓▓▓
████▓▓▓▓████████████████████████████████████▓▓▓▓▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████████████▓▓▓▓▓▓
██▓▓▓▓▓▓▓▓████████████████████████████▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒████████████████▓▓▓▓████
▓▓▓▓▓▓▓▓▓▓▓▓██████████████████████▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▒▒░░░░░░▒▒████████████▓▓▓▓▓▓████
▓▓▓▓▓▓▓▓▓▓▓▓████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▒▒  ▒▒▓▓▓▓██▓▓████████▓▓▓▓▓▓██████
▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████████▓▓▒▒▒▒▒▒▒▒░░▒▒▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒░░░░▒▒▒▒▓▓▓▓██▓▓▓▓▓▓████▓▓▓▓██
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████████▓▓▒▒▒▒▒▒▒▒░░░░░░▓▓▓▓▓▓▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒░░▒▒▒▒▒▒░░▓▓░░██████▓▓▓▓▓▓▓▓▓▓████████████
██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▒▒▒▒░░░░▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒  ░░▓▓████████▓▓▒▒▓▓██████████████
████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████▓▓▒▒▓▓▒▒▓▓▓▓░░░░▓▓░░▓▓▓▓▒▒░░░░▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░    ░░░░░░▒▒▒▒░░▒▒▓▓████████▓▓▒▒▓▓▓▓████▓▓██████
██▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████▒▒▓▓▒▒████████░░▒▒  ▓▓▒▒▒▒░░░░  ░░░░▒▒▒▒░░░░░░▒▒▒▒░░░░░░░░░░▒▒▓▓▓▓▒▒▒▒████████▓▓▒▒▓▓██████████████
████▓▓██▓▓▓▓▓▓▓▓▓▓▒▒██████▓▓░░▓▓██████████▓▓▒▒  ▒▒▓▓▒▒░░░░  ░░░░▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▓▓▓▓▒▒▓▓▓▓████▓▓▒▒██▓▓████████▓▓██
██████▓▓██▓▓▓▓▓▓▓▓▓▓▓▓████▓▓░░▓▓████████████▒▒  ▓▓▓▓▒▒░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▓▓▓▓▓▓░░████████▒▒▓▓████▓▓████████
██▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒██▓▓░░▓▓██████████▒▒▓▓░░▓▓▓▓▒▒░░  ░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒░░░░░░▓▓▓▓▓▓▓▓░░░░▒▒▓▓▒▒██▓▓████████████
████▓▓████▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░██████████▓▓▒▒▓▓▒▒▓▓▓▓▒▒░░░░▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▓▓▓▓▒▒▓▓▒▒▒▒▒▒▓▓████████████████
██████▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓░░▓▓██████▒▒▒▒▓▓▒▒▓▓▓▓▓▓▒▒░░░░▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░░░▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓██████████████
██████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▒▒▒▒▓▓▓▓▒▒▒▒▓▓▓▓▓▓░░░░░░▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒░░▒▒▓▓▓▓▒▒▒▒▒▒▓▓▓▓████▓▓▓▓▓▓██▓▓▓▓
████▓▓████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓▓▒▒▒▒▓▓██▓▓▒▒    ░░▒▒▒▒░░░░░░░░░░  ░░░░░░░░░░░░░░░░▒▒░░░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████
████████▓▓▓▓██▓▓▓▓▓▓▓▓▓▓████▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓░░    ▓▓░░░░░░░░░░░░░░      ░░▒▒▒▒░░░░░░▒▒▒▒  ░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
██▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▒▒▒▒▒▒▓▓▓▓▓▓██▓▓▒▒░░  ▒▒▒▒░░░░▒▒▓▓██▓▓▓▓    ▓▓▓▓▓▓▒▒▒▒░░░░▒▒▒▒  ░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████
██████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████▓▓▓▓████████▓▓░░    ▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░░░    ░░░░▒▒▒▒  ░░▒▒▓▓▓▓▒▒▓▓▓▓▓▓▓▓████████████
██▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████████████████▓▓▒▒░░░░  ▒▒▒▒░░░░                          ░░░░▒▒  ░░░░▒▒▓▓▒▒▓▓▓▓▓▓██████████████
████▓▓▓▓▓▓██▓▓▓▓▓▓▓▓████████▓▓██████████████▓▓▒▒░░░░░░▒▒░░░░░░░░                        ░░░░░░    ░░▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓██████████
██████████▓▓▓▓████████████▓▓▓▓▓▓██▓▓▒▒████▓▓▒▒▒▒░░░░░░░░░░░░                      ░░░░░░░░░░░░  ░░░░▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████
████████████▓▓▓▓██████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▒▒▒▒▒▒░░░░░░░░░░░░░░░░  ░░░░        ░░░░░░▒▒░░░░░░░░  ░░░░▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
████████████████████████████▓▓▓▓▓▓▓▓▒▒▓▓▓▓▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒░░░░░░  ░░░░░░▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
████████████████████████▓▓██▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▒░░░░░░▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒░░░░░░  ░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████
██████████████████████▓▓▓▓▓▓████▓▓▓▓▓▓▓▓██▓▓▒▒░░▒▒░░░░░░▒▒▒▒░░░░▒▒▒▒▒▒▒▒▓▓▒▒▒▒░░░░░░░░  ░░░░░░░░▒▒▒▒▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓████████
██████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒░░  ░░▒▒░░▒▒░░░░▒▒▒▒▒▒▒▒░░░░░░  ░░░░░░░░░░░░░░░░▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓██████████
████████████▓▓▓▓▓▓██▓▓▓▓▒▒▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████
████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓▓▓▓▓▓▓▓██████▓▓▒▒▒▒▒▒▒▒░░░░▒▒▒▒░░░░░░░░░░░░░░░░░░░░▒▒░░▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████
██████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████▓▓██████▓▓▒▒▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓████▓▓▓▓▓▓▓▓██████████████
████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████████████████▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓██████▓▓▓▓▓▓▓▓██████████████
██████▓▓▓▓▓▓▓▓▓▓▒▒▓▓██████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓████████▓▓▓▓▓▓▓▓██████████████
████▓▓▓▓▓▓▓▓▒▒▓▓██████████████████████████████████▓▓▓▓▓▓▓▓▓▓▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒▓▓▓▓▓▓▓▓▓▓████████████▓▓▓▓▓▓████████████████
██▓▓▓▓▓▓▓▓▓▓██████████████████████████████████████▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████████▓▓▓▓████████████████
▓▓▓▓▓▓▓▓▓▓██████████████████████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████████████████████████████████████████
==============================================================================================================================
=========================================== ✨ I will not spend diamonts to fish! 😊 ========================================
==============================================================================================================================


>>---> Press ctrl + c to kill the bot.

>>---> Some configs can be found in the config.yaml file."""


def remove_suffix(input_string, suffix):
    """Returns the input_string without the suffix"""

    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images(dir_path='./targets/'):
    """ Programatically loads all images of dir_path as a key:value where the
        key is the file name without the .png suffix

    Returns:
        dict: dictionary containing the loaded images as key:value pairs.
    """

    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

def show(rectangles, img = None):
    """ Show an popup with rectangles showing the rectangles[(x, y, w, h),...]
        over img or a printSreen if no img provided. Useful for debugging"""

    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    # cv2.rectangle(img, (result[0], result[1]), (result[0] + result[2], result[1] + result[3]), (255,50,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)

def moveTo(x, y):
    """Moves the mouse to the x,y position"""
    logger('Moving mouse to ({x}, {y})...')
    pydirectinput.moveTo(x, y)

def click():
    """Clicks the mouse"""
    logger('Clicking...')
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def screenshot(hwnd = None):
    primary_desktop_hwnd=win32gui.GetDesktopWindow()
    if hwnd is None:
        hwnd = primary_desktop_hwnd
    # else:
    #     try:
    #         win32gui.SetForegroundWindow(hwnd)
    #         time.sleep(.2) #lame way to allow screen to draw before taking shot
    #     except:
    #         pass

    l,t,r,b=win32gui.GetWindowRect(hwnd)
    h=b-t
    w=r-l

    hDC = win32gui.GetWindowDC(primary_desktop_hwnd)
    myDC=win32ui.CreateDCFromHandle(hDC)

    myBitMap = win32ui.CreateBitmap()
    myBitMap.CreateCompatibleBitmap(myDC, w, h)

    newDC=myDC.CreateCompatibleDC()
    newDC.SelectObject(myBitMap)

    newDC.BitBlt((0,0),(w, h) , myDC, (0,0), win32con.SRCCOPY)
    myBitMap.Paint(newDC)
    myBitMap.SaveBitmapFile(newDC, 'tmp.bmp')

    sct_img = cv2.imread('tmp.bmp')
    return sct_img[:,:,:3]

def _get_windows_bytitle(title_text, exact = False):
    def _window_callback(hwnd, all_windows):
        all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    windows = []
    win32gui.EnumWindows(_window_callback, windows)
    if exact:
        return [hwnd for hwnd, title in windows if title_text == title]
    else:
        return [hwnd for hwnd, title in windows if title_text in title]

def positions(target, threshold=ct['default'], img = None):
    if img is None:
        global game_hwnd
        img = screenshot(game_hwnd)

    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def scroll():
    commoms = positions(images['commom-text'], threshold = ct['commom'])
    if (len(commoms) == 0):
        return
    x,y,w,h = commoms[len(commoms)-1]

    moveTo(x, y)

    if not c['use_click_and_drag_instead_of_scroll']:
        pydirectinput.scroll(-c['scroll_size'])
    else:
        pydirectinput.dragRel(0,-c['click_and_drag_amount'],duration=1, button='left')

def waitForBite():
    global fishing_pos

    start_time =time.time()
    found_position = []
    while len(found_position) == 0:
        if time.time() - start_time > c['time_intervals']['max_time_to_wait_for_bite']:
            logger('🎣 No fish bite in a while...', 'red')
            click()
            start_time =time.time()
            continue

        logger('🎣 Waiting for fish to bite...')
        found_position = positions(images['reel'])
        if len(found_position) == 0:
            logger('Still waiting...')
        else:
            if len(fishing_pos) == 0:
                fishing_pos = found_position
            logger('🎣 Fish bite!', 'green')
            reelFish()


def toggleFishingAction():
    # global fishing_pos

    # x, y, w, h = fishing_pos[len(fishing_pos)-1]

    # moveTo(x, y)
    click()

def reelFish():
    logger('🎣 Reeling fish')

    toggleFishingAction()

    # TODO : results
    time.sleep(2)
    click()

    time.sleep(2)

def startFishing():
    logger('🎣 Starting to fish...')
    toggleFishingAction()

def main():
    """Main execution setup and loop"""
    # ==Setup==
    global images
    global fished_times
    global success_times
    global failed_times

    images = load_images()
    fished_times = 0
    success_times = 0
    failed_times = 0

    print(fish)
    # ==Startup==    
    startup_delay = c['time_intervals']['startup_delay']
    while startup_delay > 0:
        print(f"Starting in {startup_delay} seconds...")
        time.sleep(1)
        startup_delay -= 1
    # =========

    global fishing_pos
    global game_hwnd

    fishing_pos = []
    game_hwnd = _get_windows_bytitle('Ragnarok Origin', exact=False)[0]
    while True:

        startFishing()
        waitForBite()

        # logger(None, progress_indicator=True)
        sys.stdout.flush()
        time.sleep(int(c['time_intervals']['interval_between_fishing']))


if __name__ == '__main__':
    main()