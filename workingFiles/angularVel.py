# vWinkel
class AngularVel(object):
	#def __init__(self, avX, avY, avZ):
	def __init__(self, av):
		#self.avX = avX
		#self.avY = avY
		#self.avZ = avZ
		self.av = av
	# addDrehmoment
	#def addTorque(self, t1, t2, t3, I, dt):
	def addTorque(self, t, I, dt):
		#self.avX += 1 / I * t1 * dt
		#self.avY += 1 / I * t2 * dt
		#self.avZ += 1 / I * t3 * dt
		self.av += t * dt / I
	def __str__(self):
		return "avX: " + str(self.av[0]) + "\n" + "avY: " + str(self.av[1]) + "\n" + "avZ: " + str(self.av[2])