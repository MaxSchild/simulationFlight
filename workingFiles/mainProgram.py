#main program
import math
import numpy as np
from position import Position 
from attitude import Attitude
from angularVel import AngularVel
import physics as PHY
import control as CONTROL
import fakeSensors as SENSORS
import const as C
import time
import matplotlib.pyplot as plt
if C.ANIMATE:
	from animation import Animation
	from vpython import *


#------ STARTING PARAMETERS ------
# angular velocity
avX = 0.01#2 * math.pi
avY = 0
avZ = 0.01
angularVelocity = AngularVel(np.array([avX, avY, avZ]))

#attitude vectors
u1 = 0
u2 = 1
u3 = 0

v1 = 1
v2 = 0
v3 = 0
#creating the attitude
attitude = Attitude(np.array([u1, u2, u3]) , np.array([v1, v2, v3]))
position = Position(C.HEIGHT, C.INCLINATION)
magnetorquersCurrent = np.array([0,0,0])

if C.ANIMATE:
	animation = Animation()

t = 0
position.calcPosition(t)
animation.update(position, attitude)

if C.ANIMATE:
	time.sleep(1)

plotTime = []
plotAngV = [[],[],[],[]]
plotV = [[],[],[],[]]
plotAngle = []

PLT = plt.figure()
ax1 = PLT.add_subplot(211)
ax2 = PLT.add_subplot(212)

while t < C.DURATION:
	#switch on magnetorquers -> funktion einsetzen
	if C.ANIMATE:
		rate(20)

	#-----SIMULATION: CALCULATE DATA------
	
	# global reference frame
	B = PHY.mFluxDensity(position.pos)
	# cubsat reference frame
	
	magnetometerVoltage = SENSORS.fakeMagnetometers(B, attitude)
	gyroVoltage = SENSORS.fakeGyros(angularVelocity, attitude)
	vectorToEarth = SENSORS.fakeAttitude(position.pos, attitude)


	#--------CALL CONTROL-SYSTEM--------
	if int(t/50) % 2 == 1:
		#vectorToEarth = SENSORS.fakeAttitude(np.array([0,1,0]), attitude)
		vectorToEarth *= -1

	magnetorquersVoltage = CONTROL.react(magnetometerVoltage, gyroVoltage, vectorToEarth)
	#if CONTROL.controlCounter == 1:
	#	print("controlling: ", t)

	#------- SIMULATION: CHANGE DATA---------
	magnetorquersCurrent = SENSORS.fakeMagnetorquerts(magnetorquersVoltage, magnetorquersCurrent, C.DT)
	m = PHY.getDipolemoment(magnetorquersCurrent, attitude)
	torque = PHY.getTorque(B, m)
	#print("torque: ", torque)
	#print("realtorque:", SENSORS.toCSRF(torque/np.linalg.norm(torque),attitude))
	position.calcPosition(t)
	angularVelocity.addTorque(torque, C.MOMENT_INERTIA, C.DT)
	attitude.newAttitude(angularVelocity.av, C.DT)
	

	#------- ANIMATION: UPDATE-------
	if C.ANIMATE:
		animation.update(position, attitude)

	
	#-------DEBUG-PRINT-----------
	if (t - int(t) < 1e-5) and (int(t) % 1 == 0) and (t >= 0):
		#print("m*B", np.dot(m,B))
		#print("angularVelocity", np.linalg.norm(angularVelocity.av))
		#print("magnetorquersCurrent: ", magnetorquersCurrent)
	
		plotTime.append(t)
		plotAngle.append(CONTROL.angleEarth)
		plotAngV[0].append(np.linalg.norm(angularVelocity.av))
		plotV[0].append(np.linalg.norm(magnetorquersVoltage))
		plotV[1].append(magnetorquersVoltage[0])
		plotV[2].append(magnetorquersVoltage[1])
		plotV[3].append(magnetorquersVoltage[2])
		'''
		plotAngV[1].append(abs(SENSORS.toCSRF(angularVelocity.av, attitude)[0]))
		plotAngV[2].append(abs(SENSORS.toCSRF(angularVelocity.av, attitude)[1]))
		plotAngV[3].append(abs(SENSORS.toCSRF(angularVelocity.av, attitude)[2]))
		'''
		'''
		plotAngV[1].append(angularVelocity.av[0])
		plotAngV[2].append(angularVelocity.av[1])
		plotAngV[3].append(angularVelocity.av[2])
		'''

		if C.PLOT and (int(t) % 1 == 0):
			#plotAngV[0][round(t/50)] = angularVelocity.av[0]
			plt.clf()
			plt.cla()
			#magnitude, 	= plt.semilogy(plotTime, plotAngV[0], label = 'magnitude')
			angle, 	= ax1.plot(plotTime, plotAngle, label = 'angle error')
			voltage, 	= ax2.plot(plotTime, plotV[0], label = 'voltage')
			
			ax1.legend(handles=[angle],loc='upper right')
			ax2.legend(handles=[voltage],loc='upper right')
			'''
			voltage1, 	= plt.plot(plotTime, plotV[1], label = 'voltage1')
			voltage2, 	= plt.plot(plotTime, plotV[2], label = 'voltage2')
			voltage3, 	= plt.plot(plotTime, plotV[3], label = 'voltage3')
			xAxis, 		= plt.semilogy(plotTime, plotAngV[1], label = 'x-Axis')
			yAxis, 		= plt.semilogy(plotTime, plotAngV[2], label = 'y-Axis')
			zAxis, 		= plt.semilogy(plotTime, plotAngV[3], label = 'z-Axis')
			plt.legend(handles=[magnitude, xAxis, yAxis, zAxis],loc='upper right')
			'''
			plt.pause(0.001)

	t += C.DT;

if not C.ANIMATE:
	#'''
	magnitude, 	= ax1.semilogy(plotTime, [max(1e-8, abs(x)) for x in plotAngV[0]], label = 'magnitude')
	xAxis, 		= ax1.semilogy(plotTime, [max(1e-8, abs(x)) for x in plotAngV[1]], label = 'x-Axis')
	yAxis, 		= ax1.semilogy(plotTime, [max(1e-8, abs(x)) for x in plotAngV[2]], label = 'y-Axis')
	zAxis, 		= ax1.semilogy(plotTime, [max(1e-8, abs(x)) for x in plotAngV[3]], label = 'z-Axis')
	plt.legend(handles=[magnitude, xAxis, yAxis, zAxis],loc='upper right')

	xAxis2, 	= ax2.plot(plotTime, [x for x in plotAngV[1]], label = 'x-Axis')
	yAxis2, 	= ax2.plot(plotTime, [x for x in plotAngV[2]], label = 'y-Axis')
	zAxis2, 	= ax2.plot(plotTime, [x for x in plotAngV[3]], label = 'z-Axis')
	ax2.legend(handles=[xAxis2, yAxis2, zAxis2],loc='upper right')

	plt.show()


