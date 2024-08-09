import win32api
import win32con
import cv2
import numpy as np
import time
import pytesseract
import pydirectinput
from mss import mss

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
bounding_box = {'top': 540, 'left': 1632, 'width': 260, 'height': 230}
sct = mss()
found = False
checker_box = {'top': 800, 'left': 1750, 'width': 32, 'height': 32}
inventory_box = {'top': 725, 'left': 1750, 'width': 165, 'height': 290}
lower = np.array([57, 54, 184])
upper = np.array([120, 125, 229])
lower1 = np.array([90, 247, 133])
upper1 = np.array([91, 248, 138]) 
item_template = cv2.imread("item.png")
item_template = cv2.cvtColor(np.array(item_template), cv2.COLOR_BGR2RGB)

# Give some time to set up
time.sleep(2)
#win32api.SetCursorPos((1765,790))
while not found:
    img = sct.grab(checker_box)
    img1 = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower1, upper1)
    masked = cv2.bitwise_and(img1, img1, mask=mask) 
    points = cv2.findNonZero(masked[:,:,0])
    inventory_rec = sct.grab(inventory_box)
    inventory_rec = cv2.cvtColor(np.array(inventory_rec), cv2.COLOR_BGR2RGB) 
    #SE AINDA TEM ITEM FAZ ISTO EM BAIXO
    if points is None:
        #TODO pro caso de nao ter item selecionado
        res = cv2.matchTemplate(inventory_rec, item_template, cv2.TM_CCOEFF_NORMED)
        if np.any(res > 0.9):
            item_location = np.where( res >= 0.9)
            transposed = list(zip(*item_location))
            if transposed:
                win32api.SetCursorPos((transposed[0][1] + 1755, transposed[0][0] + 740))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                win32api.SetCursorPos((1765,790))
                time.sleep(0.1)
        else:
            break
    else:
        # Capture screen
        img = sct.grab(bounding_box)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.resize(mask, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        text = pytesseract.image_to_string(mask)
        split_text = text.split("\n")
        for i in range(40, 60):
            if f"Dano Média: {i}%" in split_text or f"Dano Medio: {i}%" in split_text or f"Dano Media: {i}%" in split_text or f"Dano Médio: {i}%" in split_text:
                found = True
                break
        # Simulate mouse click
        if not found:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            time.sleep(0.25)
        cv2.imshow("test", inventory_rec)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break