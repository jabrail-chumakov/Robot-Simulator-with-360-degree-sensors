from __future__ import print_function

import time
from sr.robot import *

o_th = 2.0
""" float: Threshold for the control of the orientation """

d_th = 0.4
""" float: Threshold for the control of the linear distance """

g_th = 0.7
""" float: Threshold for the control of the distance to the nearest golden box """



R = Robot()
""" instance of the class Robot """

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist = 100
    dist_silver = dist
    for token in R.see():
        if token.dist < dist_silver and token.info.marker_type is MARKER_TOKEN_SILVER:
        	dist_silver = token.dist
        	rot_y = token.rot_y
        	rot_silver = rot_y
    if dist_silver == 100:
    	return -1, -1
    else:
    	return dist_silver, rot_silver

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist = 100
    dist_golden = dist
    for token in R.see():
        if token.dist < dist_golden and token.info.marker_type is MARKER_TOKEN_GOLD:
        	dist_golden = token.dist
        	rot_y = token.rot_y
        	rot_golden = rot_y
    if dist_golden == 100:
    	return -1, -1
    else:
    	return dist_golden, rot_golden

def place_silver_token():
	print("Silved box was grabbed")
	turn(40, 1.5)
	drive(20, 1)
	R.release()
	print("Silver box was released")
	drive(-20, 1)
	turn(-40, 1.5)

while 1:
	dist_silver, rot_silver = find_silver_token()
	dist_golden, rot_golden = find_golden_token()	
	if dist_silver < d_th:
		print("Token detected!")
		if R.grab():
			place_silver_token()
			
	if  dist_golden > g_th or abs(rot_golden) > 90.0:	
		if 100.0 > rot_silver > o_th and dist_silver < 1.0:
			turn(10, 0.01)
		elif -o_th > rot_silver > -100.0 and dist_silver < 1.0:
			turn(-10, 0.01)		
		else:
			#print("Moving in the search of silver box!")
			print("Golden angle: ", rot_golden)
			#print("Golden distance: ", dist_golden)
			print("Silver angle: ", rot_silver)
			#print("Silver ditance: ", dist_silver)
			drive(30, 0.1)	
			
	elif dist_golden < g_th and abs(rot_golden) < 90.0:
		if smth:
			turn(20 , 0.5)
			print("Когда угол положительный, но нам все равно налево нужно")
		elif smth:
			turn(-20, 0.5)
			print("Когда угол отрицательный, но нам все равно направо нужно")
		else:
			if rot_golden < 0.0:
				print("Left")
				turn(20, 0.5)
			elif rot_golden > 0.0:
				print("Right")
				turn(-20, 0.5)
