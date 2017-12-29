#main program
import math
from position import Position 

#set conditions (position, angular velocity, attitude, delta t, duration)
height =int(input("Set x-coordinate of the position in metres(this will be the height)"))

inclination = float(input("Set the inclination in radians"))
dt = float(input("Set the time intervals"))
t = float(input("Set t0 (how many times dt should pass to start)"))
duration = (int(input("how many times should calculations be made?")) + t) *dt
#setting the objects
position = Position(height, inclination)

while t < duration:
	#switch on magnetorquers

	#increase t
	t += (1 * dt)

	#calculate new position
	position.calcPosition(t)
	print(str(position))
	#calculate new angular velocity (use)

	#calculate new attitude