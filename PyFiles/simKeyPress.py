import pyautogui
import time

screenWidth, screenHeight = pyautogui.size()

# Getting into the first level of the game
# for i in range(7):
# 	pyautogui.press('enter')
# 	time.sleep(3)

time.sleep(5)
pyautogui.keyUp('up')
# pyautogui.press('up')
# time.sleep(1)
# pyautogui.press('up')
# time.sleep(1)
# pyautogui.press('left')