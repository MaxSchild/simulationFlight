import math
import numpy as np


def getEstimatedDipoleMomentum(B, targetTorque, J):
    '''
    B: magnetic flux density 
    targetTorque: axis and amount of torque desired
    J: moment of inertia

    anglPerc: 1.0 -> B and targetTorque are perpendicular
             0.0 -> B and targetTorque are parallel
    
    global PROPORTIONAL_COEFF
    anglPerc = abs(acos(dot(B, targetTorque)/norm(B) / norm(targetTorque))-0.5*pi)/(0.5*pi);
    A = J * targetTorque * norm(targetTorque)^0.5 * 0.04 * (1.01 - anglPerc)^1.3; 
    if(norm(cross(B, A)) != 0):
        m = ( cross(B, A) / norm(cross(B, A)) ) * norm(A) / norm(B)  * PROPORTIONAL_COEFF;
    else
        m = [0,0,0];

    return m
    '''

def react(mmV, gyroV):
    # mmV: voltages from magnetometers
    # gyroV: voltages from gyros
    # return: magneTORQUERS voltage (array)

    return np.array([1,0,0])
