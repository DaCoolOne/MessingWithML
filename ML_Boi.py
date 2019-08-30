import math
import numpy as np
import keras
import sys
import os
from keras.models import Sequential
from keras.layers import Dense

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from utils.structs import *
from utils.Input_Encoder import *
from utils.Output_Decoder import *

# Add the teacher to the path
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path+"/teacher")

# Now it is safe to import the teacher
from teacher.main import Teacher as teacher

# torch.from_numpy

class ML_Boi(BaseAgent):
	
	def initialize_agent(self):
		
		self.field_info = FieldInfo(self, self.get_field_info())
		self.model = Sequential()
		self.model.add(Dense(units=5, activation="relu", input_dim=INPUT_SIZE))
		self.model.add(Dense(units=OUTPUT_SIZE, activation="softmax"))
		self.model.compile(loss=keras.losses.categorical_crossentropy, \
			optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))
		
		self.teacher = teacher(self.name, self.team, self.index)
		
		self.teacher.get_field_info = self.get_field_info
		self.teacher.renderer = self.renderer
		
		self.teacher.initialize_agent()
	
	def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
		
		# Get the teacher's output
		cs = encode_output(self.teacher.get_output(packet))
		
		# Decode the packet
		p = Packet(packet)
		
		# Encode the packet into a more bot-friendly format
		input = encode_input(p, self.field_info, self.index)
		
		# Train the packet on our teacher's data
		print(input.shape)
		self.model.train_on_batch(input, cs)
		
		# Predict our teacher's output
		ml_o = self.model.predict(input, batch_size=1)
		
		# Decode the numpy array into a SimpleControllerState
		return decode_output(ml_o)
		
	


