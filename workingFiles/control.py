import math
from numpy import *
from numpy.linalg import *
import numpy as np
import const as C
import matplotlib.pyplot as plt

plotBdot = [[],[],[],[]]

lastB = np.array([0, 0, 0])

controlCounter = 0
angleFactor = 2.0

def f(i):
    return "{:10.4f}".format(i)

def printV(name,V):
    #V = V / norm(V)
    #print(name + " = Vector((0, 0, 0), (" + f(V[0]) +", "+ f(V[1]) + ", " + f(V[2]) + "))")
    print(name + " (" + str(V[0]) +", "+ str(V[1]) + ", " + str(V[2]) + "))")

def detumbleMM(B, R):
    '''
    B:      Magnetic field vector
    R:      Rotation vector
    return: targert magnetic moment
    '''
    
    #component of R parallel to B
    R_parallel = dot(B, R) / norm(B) * (B /norm(B))
    #component of R perpendicular to B
    R_orth = R - R_parallel

    #only act if angle > 45 deg
    global controlCounter, angleFactor
    if (controlCounter > 0) or (norm(R_orth) >= angleFactor * norm(R_parallel)):
        torqueAxis = -R_orth/norm(R_orth)
        mm = cross(B, torqueAxis) / norm(B) * (norm(R_orth)**1) * C.PROPORTIONAL_COEFF
        if controlCounter <= 0:
            controlCounter = 10 #control time in seconds
        else:
            controlCounter -= C.DT
        angleFactor = C.ANGLE_FACTOR
    else:
        mm = np.array([0,0,0])
        angleFactor *= 0.999**C.DT
    '''
    printV("B", B)
    printV("Bdot", Bdot)

    printV("T", torque) 
    printV("mm", mm)
    print()

    #exit()
    '''
    return mm


    ''' last try: B-DOT CONTROL
    Bdot = (B - lastB) / C.DT
    if norm(lastB) == 0 or norm(Bdot) == 0:
        return np.array([0,0,0])
    
    plotBdot[0].append(Bdot[0])
    plotBdot[1].append(Bdot[1])
    plotBdot[2].append(Bdot[2])
    # B-Field rotates in invers direction compared to CubeSat rotatio
    torque = - cross(Bdot, B) / norm(Bdot) / norm(B) #invers dir to rot vector
    mm = cross(B, torque) / norm(B) * (norm(Bdot)**1) * C.PROPORTIONAL_COEFF

    '''


    ''' last try:
    #tries to remove controllable component of angularVel
    rotB = B * (dot(angularVel, B) / (norm(B)**2)) #rotVel projected onto B
    rotNotB = angularVel - rotB #other part of the angularVel, normal to rotB
    if(norm(rotNotB) > 0):
        print("rel rotB/rotNotB: ", norm(rotB)/norm(rotNotB))
        #print("rotNotB: ", rotNotB)
        plotRotNotB[0].append(rotNotB[0])
        plotRotNotB[1].append(rotNotB[1])
        plotRotNotB[2].append(rotNotB[2])
        t_target = -rotNotB / norm(rotNotB) # torque opposite to current rotation
        #mRequiredRel = cross(B, t_target) / (norm(B)**2) * (norm(rotNotB)**1) * C.PROPORTIONAL_COEFF
        mRequiredRel = cross(B, t_target) / (norm(B)) * (norm(rotNotB)**1) * C.PROPORTIONAL_COEFF
        #print("t_target: ", t_target)
        return mRequiredRel

    return np.array([0,0,0])
    '''

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
    global lastB
    # mmV: voltages from magnetometers
    # gyroV: voltages from gyros
    # return: magneTORQUERS voltage (array)
    if (not (norm(mmV) > 0 and norm(gyroV) > 0)):
        return np.array([0,0,0])

    B = fluxDensityByVoltage(mmV)
    angV = angVByVoltage(gyroV)



    targetMM = detumbleMM(B, angV)
    targetCurrent = solenoidNeededCurrent(targetMM)
    targetVoltage = getVoltageByTargetCurrent(targetCurrent)

    lastB = B
    #print("targetMM:", targetMM)

    if (norm(targetVoltage) > 5):
        targetVoltage = targetVoltage / norm(targetVoltage) * 5
        #print("max voltage")
    #return np.array([0,0,0])
    return targetVoltage
