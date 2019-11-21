import pyautogui
import time
from AppKit import NSWorkspace, NSScreen, NSArray, NSRect, NSWindow, \
	NSSize
from AppKit import NSMutableArray
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, \
	kCGNullWindowID, kCGWindowListExcludeDesktopElements, CFArrayRef

screenWidth, screenHeight = pyautogui.size()
print(screenWidth,screenHeight)

time.sleep(1)

windowList  = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly | \
	kCGWindowListExcludeDesktopElements, kCGNullWindowID)

for window in windowList:
	if window['kCGWindowName'] == 'Baba Is You':
		print(window['kCGWindowName'])
		windowBounds = window['kCGWindowBounds']
		print(windowBounds)

# Getting position and size of Baba window for screenshot
# For some inexplicable reason I have to multiply everything by 2
x = windowBounds['X'] * 2
y = windowBounds['Y'] * 2
height = windowBounds['Height'] * 2
width = windowBounds['Width'] * 2

# this takes a screen shot of a specific region, the left, top, width, and height
# I need to subtract 45 in order to not include the top bar
im = pyautogui.screenshot(region=(x,y+45, width, height - 45))
im.save(r"/Users/personal/Desktop/BabaIsYou/Screenshots/screenshot.png")

# activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
# print(activeAppName)

# allAppNames = NSWorkspace.sharedWorkspace().runningApplications()
# for app in allAppNames:
# 	if app.localizedName() == "Baba Is You":
# 		baba = app

# print(app.size)

# allAppNames = NSWorkspace.sharedWorkspace().runningApplications()[1]
# print(allAppNames)

# screen = activeAppName = NSWorkspace.sharedWorkspace().activeApplication()
# screenRect = [screen.visibleFrame]
# print(screenRect.size.width)

# screens = [(s.frame().size.width, s.frame().size.height) \
# for s in NSScreen.screens()]
# print(screens)

# screenbaba = NSScreen.mainScreen()
# print(screenbaba.frame().size)


# NSArray *screenArray = [NSScreen screens];

# - (NSString*) screenResolution {

#     NSRect screenRect;
#     NSArray *screenArray = [NSScreen screens];
#     unsigned screenCount = [screenArray count];
#     unsigned index  = 0;

#     for (index; index < screenCount; index++)
#     {
#         NSScreen *screen = [screenArray objectAtIndex: index];
#         screenRect = [screen visibleFrame];
#     }

#     return [NSString stringWithFormat:@"%.1fx%.1f",screenRect.size.width, screenRect.size.height];
# }

# NSSize myNSWindowSize = [ [ myNSWindow contentView ] frame ].size
# @interface NSWindow : NSResponder
# screen = NSWindow.screen
# rect = screen.frame
# height = rect.size.height
# width = rect.size.width

# print(height, width)