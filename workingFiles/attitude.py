#attitude
import math
import numpy
class Attitude(object):
	"""docstring for Attitude"""
	def __init__(self, u, v):
		self.u = u
		self.v = v
		self.w = numpy.cross(u,v)

	def newAttitude(self, av, dt):

		self.u = self.rotateVec(av, self.u, dt)
		self.v = self.rotateVec(av, self.v, dt)
		self.w = numpy.cross(self.u, self.v)
		#r is the vector from cubesat to earth


	def angleVectors(self, u, r):
		phi = math.acos(numpy.dot(u, r) / numpy.linalg.norm(u) * numpy.linalg.norm(r))
		return phi
		
	def rotateVec(self, av, vec, dt):
		length = numpy.linalg.norm(av)
		angle = length * dt
		#normalize vector from angularVelocity
		axis = av / length

		#crossproduct of axis and vec
		cross_axis_vec = numpy.cross(axis, vec)

		dot_axis_vec = numpy.dot(axis, vec)

		vRot = vec * math.cos(angle) + cross_axis_vec * math.sin(angle) + axis * dot_axis_vec * (1- math.cos(angle))

		return vRot