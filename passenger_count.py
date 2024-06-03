import cv2
import threading
import time
from datetime import datetime, timedelta
from ultralytics import YOLO
from utils.vision_utils import CountDatabaseManager, load_config  

def process_video(camera_id, roi, db_manager):
    conf_threshold = 0.3
    model = YOLO("weights/yolov8n.pt")  # Adjust model path
    
    # Object classes
    classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                  "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                  "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                  "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                  "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                  "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                  "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                  "teddy bear", "hair drier", "toothbrush"]

    cap = cv2.VideoCapture(camera_id)
    rect_start = (roi['x1'], roi['y1'])
    rect_end = (roi['x2'], roi['y2'])
    last_save_time = datetime.now()

    while True:
        success, img = cap.read()
        if not success:
            break

        results = model(img, stream=True)
        cv2.rectangle(img, rect_start, rect_end, (0, 255, 0), 2)
        count = 0

        for r in results:
            boxes = r.boxes
            for box in boxes:
                if box.conf[0] >= conf_threshold and classNames[int(box.cls[0])] == "person":
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    if x1 > rect_start[0] and y1 > rect_start[1] and x2 < rect_end[0] and y2 < rect_end[1]:
                        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                        count += 1

        # cv2.putText(img, f'Count: {count}', (rect_start[0], rect_start[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # cv2.imshow(f'Camera {camera_id}', img)    

        # Save the count every 5 minutes
        if datetime.now() - last_save_time >= timedelta(minutes=5):
            db_manager.insert_count(camera_id, count)
            last_save_time = datetime.now()

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    config = load_config('camera_config.yaml')
    if not config or 'cameras' not in config:
        print("No camera configuration found.")
        return

    with CountDatabaseManager() as db_manager:
        threads = []
        for camera in config['cameras']:
            camera_id = camera['camera_id']
            roi = camera['roi']
            t = threading.Thread(target=process_video, args=(camera_id, roi, db_manager))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

if __name__ == "__main__":
    main()
