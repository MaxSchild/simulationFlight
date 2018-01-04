import math
import numpy
from attitude import Attitude
mu_0 = 4 * math.pi * 10e-7

def getTorque(B, m):
	t = numpy.cross(B, m)

	return t

def getDipolemoment(I, attitude):

	#u is a vector from the middle of the cubesat to the camera
	#v is a vector from the middle of the cubesat to the middle of the open side of the cubesat
	#w is the cross product of u and v

	u = attitude.u
	v = attitude.v
	w = attitude.w

	# Approximation from cubesatshop.com
	m = I[0] * u + I[1] * v + I[2] * w
	m *= 5
	
	return m
#getB			#x,y,z
def mFluxDensity(r):
	m = numpy.array([0, 0, 7.94e22])
	# Get the magnetic flux density in distance r to dipole m
	r_length = numpy.linalg.norm(r)
	dotPr = numpy.dot(r, m)

	B1 = mu_0 / (4 * math.pi) * ( 3 * r[0] * dotPr / r_length**5 - m[0] / r_length**3 )
	B2 = mu_0 / (4 * math.pi) * ( 3 * r[1] * dotPr / r_length**5 - m[1] / r_length**3 )
	B3 = mu_0 / (4 * math.pi) * ( 3 * r[2] * dotPr / r_length**5 - m[2] / r_length**3 )
	B = numpy.array([B1, B2, B3])

	return B
