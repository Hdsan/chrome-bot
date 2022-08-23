import time
import numpy as np
import pyautogui
import mss
import cv2
import statistics
from PIL import ImageGrab

alive = True
threshold = 0.9
timeout = 2
    

sleep = 0.55

XDino = 0
YDino = 0

XGround = 0
YGround = 0
    
XPtero = 0
YPtero = 0

def main():
    global XDino
    global YDino 
    global XGround
    global YGround
    global XPtero
    global YPtero
    global alive
    Dino = 0
    YDino = 0

    XGround = 0
    YGround = 0
    
    XPtero = 0
    YPtero = 0

    set_references()
    while alive:   
     screen = capture_screen()
     detect_enemy(screen)
    

def set_references():
    global XDino
    global YDino 
    global XGround
    global YGround
    global XPtero
    global YPtero
    
   
    screen = getScreen
    #localiza o dino 
    has_timed_out = False
    start = time.time()
    dino = cv2.imread('images/dino.png')
    while(not has_timed_out):
      matches = positions(dino)
      if(len(matches)==0):
       has_timed_out = time.time()-start > timeout
       continue
     
      x,y,w,h = matches[0]
      XDino = x+w/2
      YDino = y+h/2
      #define as coordenadas base de verificação aérea e terrestre
      XGround = (XDino + 150)
      YGround = (YDino + 30)

      YPtero = (YDino - 40)
      XPtero = (XGround - 10)
     
      return True
    
 
def getScreen():
    #printa tela
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = np.array(sct.grab(monitor))
       
        return sct_img[:,:,:3]

def positions(target,img = None):
    if img is None:
        img = getScreen()
    result =  cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1] 
    h = target.shape[0]
    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def load_images(dir_path='./images/'):
   
    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

def capture_screen():
    screen = ImageGrab.grab()
    return screen


def detect_enemy(screen):
  
    global XGround
    global YGround
    global XPtero
    global YPtero
    #pixel branco de comparação 
    whitePixel = screen.getpixel((int(XGround), int(YGround-100)))
    #pyautogui.moveTo(XGround,YGround+200,0)
    #verificação de ameaça terreste
    for x in range(int(XGround), int(XGround+15)):
        color = screen.getpixel((x, YGround))
        # 50 pixels de tolerancia
        if color[1] <  whitePixel[1]-50 :
         
           print(color,whitePixel)
           jump()
           break
           
     #verificação de ameaça aérea
    for x in range(int(XPtero-5), int(XPtero+10)):
        color = screen.getpixel((x, YPtero))
        # 50 pixels de tolerancia
        if color[1] <  whitePixel[1]-50 :
          # pyautogui.moveTo(x,YPtero)
           print(color,whitePixel)
           crouch()
           break
                           

# Dino Jumps
def jump():
    global XGround
    pyautogui.press("up")
    XGround += 0.9
    time.sleep(0.20)

def crouch():
    
    pyautogui.keyDown('down')
    time.sleep(sleep)
    pyautogui.keyUp('down')

    

main()