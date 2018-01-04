from vpython import *

earth = sphere(pos = vector(0, 0, 0), radius = 6371000, color = color.blue)
cubesat = box(pos = vector(7000000, 0, 0), color = color.red, length=1000000, height=1000000, width=1000000)

x = 0
while True:
	rate(50)
	cubesat.pos = vector(7000000+x, 0, 0)
	x += 10000