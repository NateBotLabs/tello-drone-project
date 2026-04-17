# This file should connect your drone to a Wi-Fi network
# Run this file for every single drone
# Log into your Wi-Fi portal and retrieve the ip addresses (http://192.168.0.1/)

from djitellopy import Tello

ssid = "CGA2121_c2W3n6M"  # Replace with the name of the Wi-Fi network
password = "hnCygzRt7AB5Wc9V3W"  # Replace with the Wi-Fi password

# Create a Tello object
drone = Tello()

# Connect to the Tello drone's Wi-Fi network
drone.connect()

# Disconnect from the Tello drone's Wi-Fi network
drone.streamoff()

# Send the Wi-Fi credentials to the Tello drone
drone.connect_to_wifi(ssid, password)
