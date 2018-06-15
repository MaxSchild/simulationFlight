import math
import numpy as np
#--------PARAMETERS-------------
# all dimensions in m, time in s

#Control system
PROPORTIONAL_COEFF = 1e2;#[1e-1; 1e2]
ANGLE_FACTOR = 2.0

DETUMBLE = False

# CubeSat:
CUBE_SIZE = 1
CUBE_VISUAL_SIZE = 200000
MOMENT_INERTIA = np.array([ [1.0/600, 0, 0], [ 0, 1.0/600, 0], [0, 0, 1.0/600]]); 
	
MU = 0.006 # depends on core material
# Magnetorquers
COIL_WHORLS = 1000
COIL_LENGTH = 0.05 # 5cm
COIL_CROSSAREA = 0.000001 # 1cm x 1cm
COIL_RESISTANCE = 30
COIL_INDUCTANCE = COIL_CROSSAREA * COIL_WHORLS**2 * MU / COIL_LENGTH

# Constants:
EARTH_RADIUS = 6371000
DIPOLE_EARTH = np.array([0, 0, 7.94e22])
EARTH_MASS = 5.972e24;
GAMMA = 6.674e-11;
MU_0 = math.pi*4e-7;

# Orbit:
HEIGHT = 400000 					# 400km
INCLINATION = 0.5 * math.pi / 2		# 

# Simulation
DT = 0.25	 							# smallest time step [1s]
DURATION = 5000						# 5500s ~= 1 orbit

PLOT = True
ANIMATE = True
