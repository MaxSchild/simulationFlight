import math
import numpy
from numpy import *
import const as C
from attitude import Attitude

def getTorque(B, m):
	t = numpy.cross(m, B)
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
	m = C.DIPOLE_EARTH
	# Get the magnetic flux density in distance r to dipole m
	r_length = numpy.linalg.norm(r)
	B = C.MU_0 / (4*math.pi) * ((3*r*dot(r,m)) / (r_length**5) - m / (r_length**3))
	return B
