#attitude
import math
import numpy
class Attitude(object):
	"""docstring for Attitude"""
	#def __init__(self, u1, u2, u3, v1, v2, v3):
	def __init__(self, u, v):
		#self.u1 = u1
		#self.u2 = u2
		#self.u3 = u3
		self.u = u
		#self.v1 = v1
		#self.v2 = v2
		#self.v3 = v3
		self.v = v
		#self.w1 = self.u2 * self.v3 - self.u3 * self.v2
		#self.w2 = self.u3 * self.v1 - self.u1 * self.v3
		#self.w3 = self.u1 * self.v2 - self.u2 * self.v1
		self.w = numpy.cross(u,v)

	#def newAttitude(self, av1, av2, av3, dt):
	def newAttitude(self, av, dt):
		#newU1, newU2, newU3 = self.rotateVec(av1, av2, av3, self.u1, self.u2, self.u3, dt)
		#newV1, newV2 ,newV3 = self.rotateVec(av1, av2, av3, self.v1, self.v2, self.v3, dt)

		#newU = self.rotateVec(av, self.u, dt)
		#newV = self.rotateVec(av, self.v, dt)

		#self.u1, self.u2, self.u3 = newU1, newU2, newU3
		#self.v1, self.v2, self.v3 = newV1, newV2, newV3

		self.u = self.rotateVec(av, self.u, dt)
		self.v = self.rotateVec(av, self.v, dt)

		#self.w1 = self.u2 * self.v3 - self.u3 * self.v2
		#self.w2 = self.u3 * self.v1 - self.u1 * self.v3
		#self.w3 = self.u1 * self.v2 - self.u2 * self.v1

		self.w = numpy.cross(self.u, self.v)
		#r is the vector from cubesat to earth

	#def angleVectors(self, u1, u2, u3, r1, r2, r3):
	def angleVectors(self, u, r):
		#phi = math.acos(u1 * r1 + u2 * ur2 + u3 * r3 / (math.sqrt(u1**2 + u2**2 + u3**2) * math.sqrt(r1**2 + r2**2 + r3**2)))
		phi = math.acos(numpy.dot(u, r) / numpy.linalg.norm(u) * numpy.linalg.norm(r))
		return phi
		
	#def rotateVec(self, av1, av2, av3, vec1, vec2, vec3, dt):
	def rotateVec(self, av, vec, dt):
		#angle = math.sqrt(av[0]**2 + av2**2 + av3**2) * dt
		angle = numpy.linalg.norm(av) * dt
		#normating vector from angularVelocity
		#length = math.sqrt(av1**2 + av2**2 + av3**2)
		length = numpy.linalg.norm(av)
		#axis1 = av1 / length
		#axis2 = av2 / length
		#axis3 = av3 / length
		axis = av / length

		#crossproduct of axis and vec
		#cross_axis_vec1 = axis2 * vec3 - axis3 * vec2
		#cross_axis_vec2 = axis3 * vec1 - axis1 * vec3
		#cross_axis_vec3 = axis1 * vec2 - axis2 * vec1
		cross_axis_vec = numpy.cross(axis, vec)

		#dot_axis_vec = axis1 * vec1 + axis2 * vec2 + axis3 * vec3
		dot_axis_vec = numpy.dot(axis, vec)

		#vRot1 = vec1 * math.cos(angle) + cross_axis_vec1 * math.sin(angle) + axis1 * dot_axis_vec * (1 - math.cos(angle))
		#vRot2 = vec2 * math.cos(angle) + cross_axis_vec2 * math.sin(angle) + axis2 * dot_axis_vec * (1 - math.cos(angle))
		#vRot3 = vec3 * math.cos(angle) + cross_axis_vec3 * math.sin(angle) + axis3 * dot_axis_vec * (1 - math.cos(angle))

		vRot = vec * math.cos(angle) + cross_axis_vec * math.sin(angle) + axis * dot_axis_vec * (1- math.cos(angle))

		#return (vRot1, vRot2, vRot3)
		return vRot