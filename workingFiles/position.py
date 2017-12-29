import math

class Position(object):
	def __init__(self, height, inclination):
		#super(Velocity, self).__init__()
		self.pX = height + 6371000
		self.pY = 0
		self.pZ = 0
		self.inclination = inclination
		#vector from middle of cubesat to middle of earth
		self.l1 = self.pX
		self.l2 = 0
		self.l3 = 0
		#vector from middle to cubesat in direction to where it's moving
		self.d1 = 0
		self.d2 = math.cos(inclination) * self.pX
		self.d3 = math.sin(inclination) * self.pX

		#calculate omega
		#constant of gravitation
		gamma =  6.673848 * (10**(-11)) #(m**3)/(kg * s**2)
		print("gamma:", gamma)
		#mass of the earth
		mEarth = 5.972 * 10**24 #kilogramm
		print("mEarth:", mEarth)
		self.omega = math.sqrt(gamma * mEarth / self.pX) / self.pX  # maybe wrong formula 0.0009
		print("omega:", self.omega)
	def __str__(self):
		return "pX: " + str(self.pX) + "   " + "pY: " + str(self.pY) + "   " + "pZ: " + str(self.pZ)

	def calcPosition(self, t):
		r = math.cos(self.omega * t) 
		s = math.sin(self.omega * t)
		self.pX = r * self.l1 + s * self.d1
		self.pY = r * self.l2 + s * self.d2
		self.pZ = r * self.l3 + s * self.d3