import webbrowser
import pyautogui
import time

# URL to open
url = 'https://offers-jo.khatawat.store/home/#/'

# Open URL in Google Chrome
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  # Windows path to Chrome
webbrowser.get(chrome_path).open(url)

# Wait for the page to load
time.sleep(5)  # Adjust this delay according to your internet speed

# Scroll down
pyautogui.scroll(-1000)  # Adjust the value to control the scroll distance
