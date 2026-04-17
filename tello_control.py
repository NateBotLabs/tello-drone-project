from djitellopy import tello

drone = tello.Tello()  # Intantiate a drone class as a usable variable for your code
drone.connect()  # This should establish a connection to your drone using the wifi network
# drone.takeoff()
# drone.land()
print(drone.get_battery())
