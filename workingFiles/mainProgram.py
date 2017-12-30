#main program
import math
import numpy
from position import Position 
from attitude import Attitude
from angularVel import AngularVel
import physics as PHY


#set conditions (position, angular velocity, attitude, delta t, duration)
height = 400000#int(input("Set x-coordinate of the position in metres(this will be the height)"))

inclination = 0#float(input("Set the inclination in radians"))
dt = 0.1 #float(input("Set the time intervals"))
t = 0 #float(input("Set t0 (how many times dt should pass to start)"))
duration = (10000 + t) *dt #(int(input("how many times should calculations be made?")) + t) *dt
#setting the objects
position = Position(height, inclination)

#setting the angular velocity
avX = 2 * math.pi
avY = 0
avZ = 0
angularVelocity = AngularVel([avX, avY, avZ])
#insert some values here
u1 = -1
u2 = 0
u3 = 0

v1 = 0
v2 = 0
v3 = 1

#creating the attitude
attitude = Attitude(numpy.array([u1, u2, u3]) , numpy.array([v1, v2, v3]))


#enable manual steering?

while t < duration:
	#switch on magnetorquers -> funktion einsetzen

	#ask for three current -> input?
	i1 = 0.5#float(input("Set current1"))
	i2 = 0#float(input("Set current2"))
	i3 = 0#float(input("Set current3"))
	i = numpy.array([i1, i2, i3])
	#getM
	m = PHY.getDipolemoment(i, attitude)

	#getB 
	b = PHY.mFluxDensity(position.pos)

	#getTorque
	to = PHY.getTorque(b, m)

	#ausgeben

	#increase t
	t += (1 * dt)

	#calculate new position
	position.calcPosition(t)
	print(str(position))

	#calculate new angular velocity (use)
	I = 1
	angularVelocity.addTorque(to, I, dt)

	#calculate new attitude
	print("angularVelocity", angularVelocity.av, dt)
	attitude.newAttitude(angularVelocity.av, dt)




