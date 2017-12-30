# vWinkel
class AngularVel(object):
	def __init__(self, avX, avY, avZ):
		self.avX = avX
		self.avY = avY
		self.avZ = avZ
	# addDrehmoment
	def addTorque(self, t1, t2, t3, I, dt):
		self.avX += 1 / I * t1 * dt
		self.avY += 1 / I * t2 * dt
		self.avZ += 1 / I * t3 * dt
	def __str__(self):
		return "avX: " + str(self.avX) + "\n" + "avY: " + str(self.avY) + "\n" + "avZ: " + str(self.avZ)