import math

#--------PARAMETERS-------------
# all dimensions in m, time in s

# CubeSat:
CUBE_SIZE = 1
CUBE_VISUAL_SIZE = 1000000

MU = 0.006 # depends on core material
# Magnetorquers
COIL_WHORLS = 500
COIL_LENGTH = 0.05 # 5cm
COIL_CROSSAREA = 0.000001 # 1cm x 1cm
COIL_RESISTANCE = 30
COIL_INDUCTANCE = COIL_CROSSAREA * COIL_WHORLS**2 * MU / COIL_LENGTH

# Constants:
EARTH_RADIUS = 6371000

# Orbit:
HEIGHT = 400000 					# 400km
INCLINATION = 0.5 * math.pi / 2		# 45°

# Simulation
DT = 1 								# smallest time step [1s]
DURATION = 10000 					# 5500s ~= 1 orbit
