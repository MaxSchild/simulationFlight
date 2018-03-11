#main program
import math
import numpy as np
from position import Position 
from attitude import Attitude
from angularVel import AngularVel
from animation import Animation
import physics as PHY
import control as CONTROL
import fakeSensors as SENSORS
import const as C
import time
import matplotlib.pyplot as plt
from vpython import *



#------ STARTING PARAMETERS ------
# angular velocity
avX = 0.2#2 * math.pi
avY = 0.1
avZ = 0
angularVelocity = AngularVel(np.array([avX, avY, avZ]))

#attitude vectors
u1 = 1
u2 = 0
u3 = 0

v1 = 0
v2 = 1
v3 = 0
#creating the attitude
attitude = Attitude(np.array([u1, u2, u3]) , np.array([v1, v2, v3]))
position = Position(C.HEIGHT, C.INCLINATION)
magnetorquersCurrent = np.array([0,0,0])
animation = Animation()

t = 0;
plotAngV = [[],[],[]]

while t < C.DURATION:
	#switch on magnetorquers -> funktion einsetzen
	rate(100)

	#-----SIMULATION: CALCULATE DATA------
	
	# global reference frame
	B = PHY.mFluxDensity(position.pos)

	# cubsat reference frame
	
	inducedVoltage = SENSORS.fakeMagnetometers(B, attitude)
	gyroVoltage = SENSORS.fakeGyros(angularVelocity, attitude)
	# TODO: fake other senors for ATTITUDE determination as well


	#--------CALL CONTROL-SYSTEM--------
	magnetorquersVoltage = CONTROL.react(inducedVoltage, gyroVoltage)


	#------- SIMULATION: CHANGE DATA---------
	magnetorquersCurrent = SENSORS.fakeMagnetorquerts(magnetorquersVoltage, magnetorquersCurrent, C.DT)
	m = PHY.getDipolemoment(magnetorquersCurrent, attitude)
	torque = PHY.getTorque(B, m)
	t += C.DT;
	position.calcPosition(t)
	angularVelocity.addTorque(torque, C.MOMENT_INERTIA, C.DT)
	attitude.newAttitude(angularVelocity.av, C.DT)
	

	#------- ANIMATION: UPDATE-------
	animation.update(position, attitude)


	#-------DEBUG-PRINT-----------
	print("angularVelocity", np.linalg.norm(angularVelocity.av))
	#print("attitude: ", attitude.u)

	plotAngV[0].append(angularVelocity.av[0])
	plotAngV[1].append(angularVelocity.av[1])
	plotAngV[2].append(angularVelocity.av[2])

plt.plot(plotAngV[0])
plt.plot(plotAngV[1])
plt.plot(plotAngV[2])
plt.show()