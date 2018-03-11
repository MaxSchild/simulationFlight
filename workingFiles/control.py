import math
from numpy import *
from numpy.linalg import *
import numpy as np
import const as C


def getEstimatedDipoleMomentum(B, targetTorque, J):
    '''
    B: magnetic flux density 
    targetTorque: axis and amount of torque desired
    J: moment of inertia

    anglPerc: 1.0 -> B and targetTorque are parallel
             0.0 -> B and targetTorque are perpendicular
    '''
    anglPerc = abs(math.acos(1.0*dot(B, targetTorque)/norm(B) / norm(targetTorque))-0.5*math.pi)/(0.5*math.pi)
    A = np.matmul(J, targetTorque) * norm(targetTorque)**0.5 * 0.04 * (1.01 - anglPerc)**1.3
    if (norm(cross(B, A)) != 0):
        m = ( cross(B, A) / norm(np.cross(B, A)) ) * norm(A) / norm(B)  * C.PROPORTIONAL_COEFF
    else:
        m = np.array([0,0,0])

    return m

def solenoidNeededCurrent(m):
#   m: magnitude of dipole momentum
    return m * C.MU_0 / (C.MU * C.COIL_WHORLS * C.COIL_CROSSAREA)

def getVoltageByTargetCurrent(I):
#   I: target current of the magnetorquers
    return C.COIL_RESISTANCE * I


def fluxDensityByVoltage(V):
    return V * 100

def angVByVoltage(V):
    return V * 100

def react(mmV, gyroV):
    # mmV: voltages from magnetometers
    # gyroV: voltages from gyros
    # return: magneTORQUERS voltage (array)
    if (not (norm(mmV) > 0 and norm(gyroV) > 0)):
        return np.array([0,0,0])

    B = fluxDensityByVoltage(mmV)
    angV = angVByVoltage(gyroV)

    targetMM = getEstimatedDipoleMomentum(B, -angV, C.MOMENT_INERTIA)
    targetCurrent = solenoidNeededCurrent(targetMM)
    targetVoltage = getVoltageByTargetCurrent(targetCurrent)


    if (norm(targetVoltage) > 5):
        targetVoltage = targetVoltage / norm(targetVoltage) * 5

    return targetVoltage
