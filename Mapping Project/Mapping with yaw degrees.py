# Import necessary modules
from djitellopy import tello
import KeyModule as kp
import numpy as np
from time import sleep
import cv2
import math
import threading


def stream_drone(me):
    try:
        while True:
            img = me.get_frame_read().frame
            img = cv2.resize(img, (360, 240))
            cv2.imshow('Drone Video Streaming', img)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        exit(1)
    finally:
        print("Streaming has been ended")


# Define parameters for drone movement
fSpeed = 117 / 10  # Forward Speed in cm/s   (15cm/s)
aSpeed = 360 / 10  # Angular Speed Degrees/s  (50d/s)
interval = 0.25
dInterval = fSpeed * interval
aInterval = aSpeed * interval

# Set initial values for drone movement
x, y = 500, 500
a = 0
yaw = 0

# Initialize key module for taking keyboard inputs
kp.init()

# Create drone object and connect to it
me = tello.Tello()
me.connect()
me.streamon()

streamer = threading.Thread(target=stream_drone, args=(me,))
streamer.start()

# Print battery percentage of drone
print(me.get_battery())

# Create list for storing points
points = [(0, 0), (0, 0)]


# Define function for taking keyboard inputs and moving the drone


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    aspeed = 50
    global x, y, yaw, a
    d = 0
    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180
    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270
    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90
    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed
    if kp.getKey("a"):
        yv = -aspeed
        yaw -= aInterval
    elif kp.getKey("d"):
        yv = aspeed
        yaw += aInterval
    if kp.getKey("q"):
        me.land()
        sleep(3)
    if kp.getKey("e"):
        me.takeoff()
    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))
    return [lr, fb, ud, yv, x, y]


# Define function for drawing points on an image


def drawPoints(img, points, yawAngle):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
                (points[-1][0] + 10, points[-1]
                [1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)
    # yaw_angle = me.get_yaw()
    cv2.putText(img, f'Actual Yaw angle: {yawAngle} degrees',
                (points[-1][0] + 10, points[-1][1] + 50), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)
   

while True:

    vals = getKeyboardInput()

    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)

    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))

    yaw_angle = me.get_yaw()
    yaw_degrees = math.degrees(yaw_angle) % 360

    if yaw_angle < 0:
        yaw_degrees *= -1

    drawPoints(img, points, yaw_degrees)

    cv2.imshow("Output", img)

    cv2.waitKey(1)
