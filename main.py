import cv2 as cv
import numpy as np
import keyboard
from ultralytics import YOLO

cap = cv.VideoCapture("video.mp4")
model = YOLO('yolo11n.pt')

def open() -> bool:

    return cap.isOpened()

def border(x:int, y:int, width_max: int, height_max: int) -> tuple:

    if x < 0:
        x=0 
    if x>width_max:
        x=width_max
    if y<0:
        y=0
    if y>height_max:
        y=height_max

    return (x,y)

def move(x:int,y:int, input_key) -> tuple:

    velocity = 20

    if input_key == ord('w'):
        y-=velocity
    elif input_key == ord('s'):
        y+=velocity
    elif input_key==ord('d'):
        x+=velocity
    elif input_key==ord('a'):
        x-=velocity
    elif input_key==ord('q'):
        return (float('inf'), float('inf'))

    return (x,y)

def main():

    if open()==False: return
    width_max = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    heigth_max = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)) 
    width_crop,heigth_crop = int(0.2*width_max), int(0.2*heigth_max)
    
    x,y = (width_max-width_crop) // 2, (heigth_max-heigth_crop) // 2
    while True:
        ret, frame = cap.read()
        if ret == False: break
        crop_frame = frame[y:y+heigth_crop, x:x+width_crop]
        results = model.track(source=crop_frame,  tracker="bytetrack.yaml", persist=True)
        new_frame = results[0].plot()
        cv.imshow('cap', new_frame)
        input_key = cv.waitKey(30) & 0xFF
        x,y = move(x,y,input_key)

        if x==float('inf') and y==float('inf'):
            break

        x,y = border(x,y,width_max,heigth_max)
        
        if x==-1 and y==-1:
            break
        

    cap.release()
    cv.destroyAllWindows()

main()