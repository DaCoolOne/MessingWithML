import math
import numpy as np

from utils.structs import Packet, Vec3, Rotation, Transform
from rlbot.utils.structures.game_data_struct import GameTickPacket

INPUT_SIZE = 3

def vec_to_list(v, l):
	l.append(v.x)
	l.append(v.y)
	l.append(v.z)

# Encode the input from the game tick packet into a format that the machine learning algorithm can understand.
def encode_input(packet: Packet, field_info, car_index):
	
	car = packet.game_cars[car_index]
	team = car.team
	
	# May not end up being used
	flip = 1 if car.team else -1
	
	# Send everything to local coordinates
	t = Transform(car.physics.location, car.physics.rotation)
	
	# Todo: Add moar
	input = []
	# vec_to_list(t.translate_point(packet.game_ball.physics.location), input)
	vec_to_list(t.transform_point(packet.game_ball.physics.location), input)
	
	n = np.asarray(input)
	return n



