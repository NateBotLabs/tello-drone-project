import math
import cv2
import cvzone
from ultralytics import YOLO
from djitellopy import TelloSwarm

# Classnames for classification
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light",
              "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
              "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
              "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
              "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
              "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
              "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard",
              "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

# Object to search
targetObject = "toothbrush"

drones = ['192.168.10.1']

# Create a TelloSwarm object
swarm = TelloSwarm.fromIps(drones)

# Connect to the drones and start stream
swarm.connect()
swarm.streamon()

# Create the model
model = YOLO("yolov8n.pt")

while True:
    for drone in swarm:
        # Get the image from the drone
        img = drone.get_frame_read().frame
        # Resize the image window
        img = cv2.resize(img, (720, 480))

        # Get results
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Draw bounding box around each object
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2-x1, y2-y1
                cvzone.cornerRect(img, (x1, y1, w, h))

                # Confidence of object classification
                conf = math.ceil((box.conf[0]*100))/100
                cvzone.putTextRect(img, f'{conf}', (max(0, x1), max(0, y1)))

                # Class index
                clsIndex = int(box.cls[0])
                # Class name
                cls = classNames[clsIndex]

                # Display class name and confidence
                cvzone.putTextRect(img, f'{cls} {conf}', (max(0, x1), max(35, y1)))

                # Check if target object is found
                if cls == targetObject:
                    print("Object found")


        # Show live feed with detected objects
        cv2.imshow("Image", img)
        cv2.waitKey(1)