import win32api
import win32con
import cv2
import numpy as np
import pytesseract
from mss import mss

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

bounding_box = {'top': 550, 'left': 1650, 'width': 220, 'height': 230}
sct = mss()
found = False

while True:
    # Read image from which text needs to be extracted
    img = sct.grab(bounding_box)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    #Masking to detect green and red
    lower = np.array([57,54,184])
    upper = np.array([120,125,229])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.resize(mask, None, fx = 3, fy = 3, interpolation = cv2. INTER_CUBIC)
    text = pytesseract.image_to_string(mask)
    split_text = text.split("\n")
    for i in range (10,80):
        if f"Dano Média: {i}%" or f"Dano Médio: {i}%" in split_text:
            found = True
    if found:
        break
    else:
        #rodar again
        print("rodar outra vez")
    cv2.imshow('screen', mask)
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break