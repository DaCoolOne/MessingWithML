# Expect more in the near future ;)

import math

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3

def clamp1(n):
    return min(1, max(n, -1))

class PythonExample(BaseAgent):

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        ball_location = Vec3(packet.game_ball.physics.location)
        goal_location = Vec3(self.get_field_info().goals[not self.team].location)

        my_car = packet.game_cars[self.index]
        car_location = Vec3(my_car.physics.location)

        push_vec = (ball_location - goal_location).rescale(-70)

        car_to_ball = ball_location - car_location # - push_vec

        # Find the direction of our car using the Orientation class
        car_orientation = Orientation(my_car.physics.rotation)
        car_direction = car_orientation.forward

        steer_correction_radians = find_correction(car_direction, car_to_ball)

        self.controller_state.throttle = 1.0
        self.controller_state.steer = clamp1(steer_correction_radians * -3)

        self.controller_state.handbrake = abs(steer_correction_radians) > math.pi * 0.5
        self.controller_state.boost = abs(steer_correction_radians) < 0.15

        draw_debug(self.renderer, my_car, packet.game_ball)

        return self.controller_state


def find_correction(current: Vec3, ideal: Vec3) -> float:
    # Finds the angle from current to ideal vector in the xy-plane. Angle will be between -pi and +pi.

    # The in-game axes are left handed, so use -x
    current_in_radians = math.atan2(current.y, -current.x)
    ideal_in_radians = math.atan2(ideal.y, -ideal.x)

    diff = ideal_in_radians - current_in_radians

    # Make sure that diff is between -pi and +pi.
    if abs(diff) > math.pi:
        if diff < 0:
            diff += 2 * math.pi
        else:
            diff -= 2 * math.pi

    return diff


def draw_debug(renderer, car, ball):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    renderer.end_rendering()
