import const as C
import numpy as np
import math

def projectOnAxis(v, axis):
	# projects vector v onto vetcor axis
	return np.dot(v, axis) / np.linalg.norm(axis)

def tranformVector(v, a, b):
	# v   : vector to be composed
	# a, b: the vectors which describe the axis of the relative coordinate system
	return np.array([projectOnAxis(v, a),
					 projectOnAxis(v, b),
					 projectOnAxis(v, np.cross(a, b))]);

def toCSRF(v, attitude):
	return tranformVector(v, attitude.u , attitude.v)

def fakeMagnetometers(B, attitude):
	return toCSRF(B, attitude) * 0.01;
	
def fakeGyros(angularVelocity, attitude):
	return toCSRF(angularVelocity.av, attitude) * 0.01;

def fakeMagnetorquerts(mtV, mtC, dt):
	#return mtV / C.COIL_RESISTANCE - (mtV / C.COIL_RESISTANCE - mtC) * math.exp( - dt * C.COIL_RESISTANCE / C.COIL_INDUCTANCE);
	return mtV / C.COIL_RESISTANCE