from vpython import *
import const as C
'''
IMPORTANT
numpy arrays / vectors: normal coord. system (z axis up)
output vectors: vpython cord. system (y axis up)
**numpToVec transforms the vectors accordingly**
'''

def numpToVec(a):
	return vec(a[1], a[2], a[0])

class Animation(object):

	def __init__(self):
		self.scene2 = canvas(width=1500, height=940)
		self.earth = sphere(pos = vector(0, 0, 0), radius = C.EARTH_RADIUS, color = color.white, texture="https://i.imgur.com/KwPyMW1.jpg")
		self.cubesat = box(color = color.red, length=C.CUBE_VISUAL_SIZE, height=C.CUBE_VISUAL_SIZE, width=C.CUBE_VISUAL_SIZE, make_trail=True)
		self.pointer = arrow();

	def update(self, position, attitude):
		self.cubesat.pos = numpToVec(position.pos)
		self.cubesat.axis = numpToVec(attitude.u * C.CUBE_VISUAL_SIZE)
		self.cubesat.up = numpToVec(attitude.v)
		self.pointer.pos = numpToVec(position.pos)
		self.pointer.axis = numpToVec(attitude.u * C.CUBE_VISUAL_SIZE * 1.5)