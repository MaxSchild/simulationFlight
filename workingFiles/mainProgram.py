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
from vpython import *



#------ STARTING PARAMETERS ------
# angular velocity
avX = 0.0#2 * math.pi
avY = 0
avZ = 0
angularVelocity = AngularVel(np.array([avX, avY, avZ]))

#attitude vectors
u1 = -1
u2 = 0
u3 = 0

v1 = 0
v2 = 0
v3 = 1
#creating the attitude
attitude = Attitude(np.array([u1, u2, u3]) , np.array([v1, v2, v3]))
position = Position(C.HEIGHT, C.INCLINATION)
magnetorquersCurrent = np.array([0,0,0])
animation = Animation()

t = 0;

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
	m = PHY.getDipolemoment(magnetorquersVoltage, attitude)
	torque = PHY.getTorque(B, m)
	t += C.DT;
	position.calcPosition(t)
	inertiaMatrix = 1 # TODO
	angularVelocity.addTorque(torque, inertiaMatrix, C.DT)
	attitude.newAttitude(angularVelocity.av, C.DT)
	

	#------- ANIMATION: UPDATE-------
	animation.update(position, attitude)


	#-------DEBUG-PRINT-----------
	print("angularVelocity", angularVelocity.av)
	print("attitude: ", attitude.u)