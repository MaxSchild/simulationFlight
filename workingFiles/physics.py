import math
import numpy
from attitude import Attitude
mu_0 = 4 * math.pi * 10e-7




#def getTorque(B1, B2, B3, m1, m2, m3):
def getTorque(B, m):
	#t1 = m2*B3 - B2*m3
	#t2 = B1*m3 - m1*B3
	#t3 = m1*B2 - B1*m2
	t = numpy.cross(B, m)

	#return (t1, t2, t3)
	return t

#def getDipolemoment(I1, I2, I3, attitude):
def getDipolemoment(I, attitude):

	#u is a vector from the middle of the cubesat to the camera
	#v is a vector from the middle of the cubesat to the middle of the open side of the cubesat
	#w is the cross product of u and v
	#u1, u2, u3 = attitude.u1, attitude.u2, attitude.u3
	#v1, v2, v3 = attitude.v1, attitude.v2, attitude.v3
	#w1, w2, w3 = attitude.w1, attitude.w2, attitude.w3

	u = attitude.u
	v = attitude.v
	w = attitude.w


	#m1 = I1 * u1 + I2 * v1 + I3 * w1 # Approximation from cubesatshop.com
	#m2 = I1 * u2 + I2 * v2 + I3 * w2
	#m3 = I1 * u3 + I2 * v3 + I3 * w3

	m = I[0] * u + I[1] * v + I[2] * w

	m *= 5
	

	#return (m1, m2, m3)
	return m
#getB			#x,y,z
#def mFluxDensity(r1, r2, r3):
def mFluxDensity(r):
	#m1 = 0
	#m2 = 0
	#m3 = 7.94e22
	m = numpy.array([0, 0, 7.94e22])
	# Get the magnetic flux density in distance r to dipole m
	#r_length = (r1**2 + r2**2 + r3**2)**0.5
	r_length = numpy.linalg.norm(r)
	#dotPr = r1*m1 + r2*m2 + r3*m3
	dotPr = numpy.dot(r, m)

	#B1 = mu_0 / (4 * math.pi) * ( 3 * r1 * dotPr / r_length**5 - m1 / r_length**3 )
	#B2 = mu_0 / (4 * math.pi) * ( 3 * r2 * dotPr / r_length**5 - m2 / r_length**3 )
	#B3 = mu_0 / (4 * math.pi) * ( 3 * r3 * dotPr / r_length**5 - m3 / r_length**3 )
	B1 = mu_0 / (4 * math.pi) * ( 3 * r[0] * dotPr / r_length**5 - m[0] / r_length**3 )
	B2 = mu_0 / (4 * math.pi) * ( 3 * r[1] * dotPr / r_length**5 - m[1] / r_length**3 )
	B3 = mu_0 / (4 * math.pi) * ( 3 * r[2] * dotPr / r_length**5 - m[2] / r_length**3 )
	B = numpy.array([B1, B2, B3])

	#return (B1, B2, B3)
	return B

#print(mFluxDensity(6310000, 0, 0))