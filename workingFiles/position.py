import math
import numpy
class Position(object):
	def __init__(self, height, inclination):
		#super(Velocity, self).__init__()
		self.pos = numpy.array([height + 6371000, 0, 0])
		#self.pX = height + 6371000
		#self.pY = 0
		#self.pZ = 0
		self.inclination = inclination
		#vector from middle of cubesat to middle of earth
		self.l = numpy.array([self.pos[0], 0, 0])
		#self.l1 = self.pX
		#self.l2 = 0
		#self.l3 = 0
		#vector from middle to cubesat in direction to where it's moving
		self.d = numpy.array([0, math.cos(inclination) * self.pos[0], math.sin(inclination) * self.pos[0]])
		#self.d1 = 0
		#self.d2 = math.cos(inclination) * self.pX
		#self.d3 = math.sin(inclination) * self.pX

		#calculate omega
		#constant of gravitation
		gamma =  6.673848 * (10**(-11)) #(m**3)/(kg * s**2)
		print("gamma:", gamma)
		#mass of the earth
		mEarth = 5.972 * 10**24 #kilogramm
		print("mEarth:", mEarth)
		self.omega = math.sqrt(gamma * mEarth / self.pos[0]) / self.pos[0]  # maybe wrong formula 0.0009
		print("omega:", self.omega)
	def __str__(self):
		return "pX: " + str(self.pos[0]) + "   " + "pY: " + str(self.pos[1]) + "   " + "pZ: " + str(self.pos[2])

	def calcPosition(self, t):
		r = math.cos(self.omega * t) 
		s = math.sin(self.omega * t)
		#self.position[0] = r * self.l[0] + s * self.d[0]
		#self.position[1] = r * self.l[1] + s * self.d[1]
		#self.position[2] = r * self.l[2] + s * self.d[2]
		self.pos = r * self.l + s * self.d





