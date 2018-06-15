import math
from numpy import *
from numpy.linalg import *
import numpy as np
import const as C
import matplotlib.pyplot as plt


lastB = np.array([0, 0, 0])

controlCounter = 0
angleFactor = 2.0

angleEarth = 180.0

status = 1 # 0 -> detumble, 1 -> aligning with B-Field, 2 -> final phase

def f(i):
    return "{:10.4f}".format(i)

def printV(name,V):
    #V = V / norm(V)
    #print(name + " = Vector((0, 0, 0), (" + f(V[0]) +", "+ f(V[1]) + ", " + f(V[2]) + "))")
    print(name + " (" + str(V[0]) +", "+ str(V[1]) + ", " + str(V[2]) + "))")

def component(V, a):
    '''
    V: vector
    a: axis
    return: vector parallel to a
    '''
    return dot(V, a) / norm(a) * (a /norm(a))

def orthComp(V, a):
    '''
    V: vector
    a: axis
    return: vector perpendicular to a, V = component(V, a) + orthComp(V, a)
    '''
    return V - component(V, a)

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

def active(B, R, v):
    '''
    B:      Magnetic field vector
    R:      Rotation vector
    V:      Vector pointing to Earth (normalized)
    return: targert magnetic moment
    '''

    '''
    We want to find a rotation axis which rotates a = (1,0,0) onto v.
    There is a plane of rotation axis which do that. We know two vectors in this plane:
        - a x v -> rotating around the cross product is the even the 'shortest' method
        - a + v -> rotating around this vector takes a rotation of 180° (only valid if |a| = |v|)

    Out of this plane, we want to find the vector which we can actually control, which lies in
    a plane perpendicular to the B-Vector. So we need to find the intersection of those two planes:

    E_1:    | B * x = 0                 |
    E_2:    | β*(a x v) + α*(a + v) = x |

    as we only need one vector, not a whole line, we set β = 1.
    B * E_2:    B*(a x v) + α*B*(a + v) = B * x

    We know from the first equation that the right side is zero. So we solve for α
        
                B*(a x v) + α*B*(a + v) = 0

                            α*B*(a + v) = -B*(a x v)

                            α           = - (B*(a x v)) / (B*(a + v))

    If we plug in our equation E_2 we have our vector x.
    '''
    a = np.array([1,0,0])

    # catch a || v
    if norm(cross(a, v)) == 0 or dot(B, a + v) == 0:
        return np.array([1,0,0])

    global angleEarth
    angleEarth = math.degrees(math.acos(dot(v, a)/norm(a) /norm(v)));
    print("angleEarth: ", angleEarth)

    alpha = - dot(B, cross(a, v)) / dot(B, a + v)

    x = cross(a, v) + alpha * (a + v)

    x = x /norm(x)
    
    '''
    We have the axis; now we need to find the direction and angle to construct our goal rotation vector.
    So we take the perpendicular components of a and v to x and calculate the angle.

    '''
    a_px = orthComp(a, x)
    v_px = orthComp(v, x)
    angle = math.acos(dot(a_px, v_px)/(norm(a_px)*norm(v_px)))

    goalRot = x * angle * 1e-1

    #flip the vector if wrong direction
    # right dir is a -> v (cubesat to earth). So a_px x v_px should point in the same dir as x 
    # this means |(a_px x v_px) - x| < |(v_px x a_px) - x|
    if norm(cross(a_px, v_px) - x) > norm(cross(v_px, a_px) - x):
        goalRot *= -1

    # try to reach this goal:
    torque = goalRot - R
    #
    mm = cross(B, torque) / norm(B)/norm(torque) * (norm(torque)**1) * C.PROPORTIONAL_COEFF

    return mm


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

def react(mmV, gyroV, toEarth):
    global lastB
    # mmV: voltages from magnetometers
    # gyroV: voltages from gyros
    # toEarth: normalized vector to earth in Cube reference frame
    # return: magneTORQUERS voltage (array)

    B = fluxDensityByVoltage(mmV)
    angV = angVByVoltage(gyroV)

    #TODO controlsystem must deceide on its own if detumbling is active
    if C.DETUMBLE:
        if (not (norm(mmV) > 0 and norm(gyroV) > 0)):
            return np.array([0,0,0])
        targetMM = detumbleMM(B, angV)
    else:
        # goal: 1. align (1,0,0) to B
        #       2. align (1,0,0) to toEarth
        if (not (norm(mmV) > 0 and norm(toEarth) > 0)):
            return np.array([0,0,0])
        targetMM = active(B, angV, toEarth)

    targetCurrent = solenoidNeededCurrent(targetMM)
    targetVoltage = getVoltageByTargetCurrent(targetCurrent)

    lastB = B
    #print("targetMM:", targetMM)

    if (norm(targetVoltage) > 5):
        targetVoltage = targetVoltage / norm(targetVoltage) * 5
        #print("max voltage")
    #return np.array([0,0,0])
    return targetVoltage
