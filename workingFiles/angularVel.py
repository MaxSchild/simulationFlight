# vWinkel
from numpy.linalg import inv
import numpy as np

class AngularVel(object):
	def __init__(self, av):
		self.av = av
	# addDrehmoment
	def addTorque(self, t, I, dt):
		self.av += dt * np.matmul(inv(I), t)
	def __str__(self):
		return "avX: " + str(self.av[0]) + "\n" + "avY: " + str(self.av[1]) + "\n" + "avZ: " + str(self.av[2])