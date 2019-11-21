import pyautogui
import time
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, \
	kCGNullWindowID, kCGWindowListExcludeDesktopElements, CFArrayRef
from PIL import Image
from resizeimage import resizeimage
import math
import os
import numpy as np

screenWidth, screenHeight = pyautogui.size()

# Giving me time to navigate to Baba Is You window
time.sleep(2)

# Getting a list of active windows 
windowList  = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly | \
	kCGWindowListExcludeDesktopElements, kCGNullWindowID)

# Getting the baba is you window bounds
for window in windowList:
	if window['kCGWindowName'] == 'Baba Is You':
		windowBounds = window['kCGWindowBounds']

# Getting position and size of Baba window for screenshot
# For some inexplicable reason I have to multiply everything by 2
# I need to subtract 45 in order to not include the top bar
x = windowBounds['X'] * 2
y = (windowBounds['Y'] * 2) + 45
height = (windowBounds['Height'] * 2) - 45 
width = windowBounds['Width'] * 2

# Largest window bounds (based on my monitor):
maxH = 805*2
maxW = 1440*2

# making array of game state to later insert icons into
gameArray = np.zeros([int(height),int(width)])

# Making a dictionary of icons to ints
iconDict = {"Baba":16, "BabaText":1, "Rock": 2, "RockText": 3, "Flag": 4, "FlagText": 5, \
"IsText": 6, "PushText": 7, "YouText": 8, "WallText": 9, "WinText": 10, "StopText": 11, \
"WaterText": 12, "SinkText": 13, "Wall1": 14, "Wall2": 15, "Water": 15}

# this takes a screen shot of a specific region, the left, top, width, and height
im = pyautogui.screenshot(region=(x, y, width, height))
im.save(r"/Users/personal/Desktop/BabaIsYou/Screenshots/screenshot.png")

# scaling factors for icons (it seems like height changes as a function of width)
# This is fairly hacky but it basically seems to work
scaleW = width/maxW
scaleH = (height/maxH) * scaleW

directory = os.fsencode('/Users/personal/Desktop/BabaIsYou/Icons/')

def resizeIm(fn):
	with open('/Users/personal/Desktop/BabaIsYou/Icons/' + fn, 'r+b') as f:
		with Image.open(f) as image:
			imW, imH = image.size
			cover = resizeimage.resize_cover(image, [int(math.floor(imH*scaleH)), \
				int(math.floor(imW*scaleW))])
	return(cover, imH*scaleH, imW*scaleW)

# This finds all the instances of an icon within the game and adds them to an array
# It attempts to not duplicate the same object by keeping a 10 pixel threshold around each icon
def findInstances(pics):
	firstPic = pics[0]
	# For now, move to instances of icon to make sure the code is working
	pyautogui.moveTo(firstPic.left/2, firstPic.top/2)
	gameArray[math.ceil(firstPic.top/2),math.ceil(firstPic.left/2)] = int(iconDict[str.split(filename,'.')[0]])
	for pic in pics[1:]:
		if (pic.top >= firstPic.top + 10) or (pic.top <= firstPic.top - 10):
			# Move mouse to instance
			pyautogui.moveTo(pic.left/2, pic.top/2)
			gameArray[math.ceil(pic.top/2),math.ceil(pic.left/2)] = int(iconDict[str.split(filename,'.')[0]])
			firstPic = pic
		else:
			continue

# Creating array of objects from game state
for file in os.listdir(directory):
	filename = os.fsdecode(file)
	# Grab the image
	if filename.endswith(".png"):
		print(filename)
		# Rescale
		scaledIcon = resizeIm(filename)[0]
		sizeH, sizeW = resizeIm(filename)[1:]
		# Skipping these for now because it thinks the entire screen is an instance
		if filename == 'Wall2.png' or filename == 'Wall1.png' or filename == 'Water.png':
			continue
		# Find in game
		else:
			pics = list(pyautogui.locateAllOnScreen(scaledIcon, confidence = 0.7, \
				region = (int(x), int(y), int(width), int(height)), grayscale=False))
		# Insert into array, if it's in the game
		if pics:
			findInstances(pics)
			# pyautogui.moveTo(pic.left/2, pic.top/2)
	else:
		continue

# How to convert keypresses to pixel values?
def moveIcon(icon,steps=0):
	babaLoc = np.argwhere(gameArray==iconDict['Baba'])
	iconLoc = np.argwhere(gameArray==iconDict[icon])
	moves = babaLoc-iconLoc
	# need an if statement to handle whenever there isn't an icon
	move = moves[0,:]
	moveV = np.round_(move[0]/sizeH)
	moveH = np.round_(move[1]/sizeW)
	if moveV != 0.0:
		for i in range(int(np.abs(moveV))+steps):
			time.sleep(1)
			if moveV*(-moveV) == moveV**2:
				pyautogui.press('up')
			else:
				pyautogui.press('down')
	if moveH != 0.0:
		for i in range(int(np.abs(moveH))+steps):
			time.sleep(1)
			if moveH*(-moveH) == moveH**2:
				pyautogui.press('left')
			else:
				print('should go right')
				pyautogui.press('right')


moveIcon('Rock', steps=1)


np.savetxt("game.csv", gameArray, fmt = '%-.0e', delimiter=",")

# babas = pyautogui.locateAllOnScreen(cover, confidence = 0.8, \
# 	region = (int(x), int(y), int(width), int(height)), grayscale=True)
# for baba in babas:
# 	print(baba)
# 	pyautogui.moveTo(baba.left/2, baba.top/2)


