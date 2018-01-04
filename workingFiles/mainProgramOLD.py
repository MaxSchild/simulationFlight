#main program
import math
from position import Position 
from attitude import Attitude
from angularVel import AngularVel
import physics as PHY

from vpython import *

earth = sphere(pos = vector(0, 0, 0), radius = 6371000, color = color.blue)
cubesat = box(pos = vector(7000000, 0, 0), color = color.red, length=1000000, height=1000000, width=1000000)


#set conditions (position, angular velocity, attitude, delta t, duration)
height = 400000#int(input("Set x-coordinate of the position in metres(this will be the height)"))

inclination = 0.7#float(input("Set the inclination in radians"))
dt = 10 #float(input("Set the time intervals"))
t = 0 #float(input("Set t0 (how many times dt should pass to start)"))
duration = (100 + t) *dt #(int(input("how many times should calculations be made?")) + t) *dt
#setting the objects
position = Position(height, inclination)

#setting the angular velocity
avX = 2 * math.pi
avY = 0
avZ = 0
angularVelocity = AngularVel(avX, avY, avZ)
#insert some values here
u1 = -1
u2 = 0
u3 = 0
v1 = 0
v2 = 0
v3 = 1

#creating the attitude
attitude = Attitude(u1, u2, u3, v1, v2, v3)


#enable manual steering?

while True:
	rate(50)
	#switch on magnetorquers -> funktion einsetzen

	#ask for three current -> input?
	i1 = 0#float(input("Set current1"))
	i2 = 0#float(input("Set current2"))
	i3 = 0#float(input("Set current3"))

	#getM
	m1, m2, m3 = PHY.getDipolemoment(i1, i2, i3, attitude)

	#getB 
	b1, b2, b3 = PHY.mFluxDensity(position.pX, position.pY, position.pZ)

	#getTorque
	t1, t2, t3 = PHY.getTorque(b1, b2, b3, m1, m2, m3)

	#ausgeben

	print("Torque", t1, t2, t3)
	#increase t
	t += (1 * dt)

	#calculate new position
	position.calcPosition(t)
	print(str(position))

	#calculate new angular velocity (use)
	I = 1
	angularVelocity.addTorque(t1, t2, t3, I, dt)

	#calculate new attitude
	print("angularVelocity", angularVelocity.avX, angularVelocity.avY, angularVelocity.avZ, dt)
	attitude.newAttitude(angularVelocity.avX, angularVelocity.avY, angularVelocity.avZ, dt)

	cubesat.pos = vector(position.pX, position.pY, position.pZ)
	cubesat.axis = vector(attitude.)




