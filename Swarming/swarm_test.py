import time

from djitellopy import TelloSwarm

drones = ['192.168.10.1', '192.168.10.2', '192.168.10.3', '192.168.10.4']

# Create a TelloSwarm object with 4 drones
swarm = TelloSwarm.fromIps(drones)

swarm.connect()

# all drones take off
swarm.takeoff()

time.sleep(2)
# run in parallel on all tellos
swarm.move_up(100)


time.sleep(2)
# run by one tello after the other
swarm.sequential(lambda i, tello: tello.move_forward(i * 20 + 20))

time.sleep(2)
# making each tello do something unique in parallel
swarm.parallel(lambda i, tello: tello.move_left(i * 100 + 20))


time.sleep(2)
swarm.land()
swarm.end()
