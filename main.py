import cv2 as cv
import numpy as np
from ultralytics import YOLO
import joblib
from huggingface_hub import hf_hub_download

cap = cv.VideoCapture("video.mp4")
REPO_ID = "YOUR_REPO_ID"
FILENAME = "sklearn_model.joblib"

model = joblib.load(
    hf_hub_download(repo_id="mshamrai/yolov8n-visdrone", 
                    filename="best.pt")
)
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
        results = model.predict(
            source=crop_frame,
            conf=0.25,          # NMS confidence threshold
            iou=0.45,           # NMS IoU threshold
            agnostic_nms=False, # NMS class-agnostic
            max_det=1000,       # maximum number of detections
            verbose=False       # Ukrywa spam w konsoli dla każdej klatki
        )

        new_frame = results[0].plot()
        cv.imshow('Dron', new_frame)
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