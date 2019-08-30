import math
import numpy as np

from rlbot.agents.base_agent import SimpleControllerState

OUTPUT_SIZE = 4

# Encode output as numpy array
def encode_output(cs: SimpleControllerState):
	n = np.zeros(OUTPUT_SIZE)
	n[0] = cs.throttle
	n[1] = cs.steer
	n[2] = 1 if cs.boost else 0
	n[3] = 1 if cs.handbrake else 0
	# n[2] = cs.pitch
	# n[3] = cs.yaw
	# n[4] = cs.roll
	# n[2] = 1 if cs.boost else 0
	# n[6] = 1 if cs.jump else 0
	# n[7] = 1 if cs.use_item else 0
	return n

def clamp1(n):
	return math.max(-1, math.min(1, n))

# Decode output from numpy array to controller state
def decode_output(arr):
	s = SimpleControllerState()
	s.throttle = clamp1(n[0])
	s.steer = clamp1(n[1])
	s.boost = n[2] > 0.5
	s.handbrake = n[3] > 0.5
	# s.pitch = clamp1(n[2])
	# s.yaw = clamp1(n[3])
	# s.roll = clamp1(n[4])
	# s.jump = n[6] > 0.5
	# s.use_item = n[7] > 0.5
	return s

