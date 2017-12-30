import math
import numpy
class Position(object):
	def __init__(self, height, inclination):
		self.pos = numpy.array([height + 6371000, 0, 0])
		self.inclination = inclination
		#vector from middle of cubesat to middle of earth
		self.l = numpy.array([self.pos[0], 0, 0])
		#vector from middle to cubesat in direction to where it's moving
		self.d = numpy.array([0, math.cos(inclination) * self.pos[0], math.sin(inclination) * self.pos[0]])

		#calculate omega
		#constant of gravitation
		gamma =  6.673848 * (10**(-11)) #(m**3)/(kg * s**2)
		print("gamma:", gamma)
		#mass of the earth
		mEarth = 5.972 * 10**24 #kilogramm
		print("mEarth:", mEarth)
		self.omega = math.sqrt(gamma * mEarth / self.pos[0]) / self.pos[0]  
		print("omega:", self.omega)
	def __str__(self):
		return "pX: " + str(self.pos[0]) + "   " + "pY: " + str(self.pos[1]) + "   " + "pZ: " + str(self.pos[2])

	def calcPosition(self, t):
		r = math.cos(self.omega * t) 
		s = math.sin(self.omega * t)
		self.pos = r * self.l + s * self.d





