import math
import datetime

def get_hand_position(center, length, angle_degrees):
    angle_radians = math.radians(angle_degrees - 90)

    x = center[0] + length * math.cos(angle_radians)
    y = center[1] + length * math.sin(angle_radians)

    return (int(x), int(y))

def get_current_time_data():
    date_now = datetime.datetime.now()

    sec_angle = date_now.second * 6

    min_angle = date_now.minute * 6 + date_now.second * 0.1

    return sec_angle, min_angle