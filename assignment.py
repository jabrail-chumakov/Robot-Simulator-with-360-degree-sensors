from __future__ import print_function

import time
from sr.robot import *

o_th = 2.0
""" float: Threshold for the control of the orientation """

d_th = 0.4
""" float: Threshold for the control of the linear distance """

g_th = 0.7
""" float: Threshold for the control of the distance to the nearest golden token """

golden_angle_max = 105.0
""" float: Threshold for the maximum golden angle for the special case """

golden_angle_min = 75.0
""" float: Threshold for the minimum goolden angle for the special case """	

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
	"""
	Function to place silver token behind when it's successfully grabbed
	"""
	print("Silved token was grabbed")
	turn(40, 1.5)
	drive(20, 1)
	R.release()
	print("Silver token was released")
	drive(-20, 1)
	turn(-40, 1.5)
	print("Robot returned to the initial position")

def special_avoiding_case():
	"""
	Function to check whether there is an obtacle in approximately 90 degree radius (from 75 to 105 degrees)
	If distance to the golden token is closer from the left, then robot turns right
	While in case if distance to the goldex token is closer from the right, then robot turns left
	
	Return:
		0 (False): Robot turs right
		1 (True): Robot turns left
	"""
	dist = 100
	# Robot scans for the golden token from the left side
    	for token in R.see():
    		if golden_angle_min < token.rot_y < golden_angle_max and token.dist < dist:
    			dist = token.dist
   	 		dist_golden = dist
   	 		rot_y = token.rot_y
        		rot_golden = rot_y
   	left_side = dist_golden

	# Robot scans for the golden token from the right side
   	for token in R.see():
   	 	if -golden_angle_max < token.rot_y < -golden_angle_min and token.dist < dist:
   	 		dist = token.dist
   	 		dist_golden = dist
   	 		rot_y = token.rot_y
        		rot_golden = rot_y
   	right_side = dist_golden

   	return left_side > right_side
   	
""" 		
Working principle

(1) If you are far away from the nearest golden token or angle to the nearest golden token is more than 90 degrees
then robot moves straight

(2) If the robot detects a silver token on the distance closer than 1.00, then robot aligns and moves towards it

(3) If the robot on the distance of 0.4 from the silver token, then grabs it, puts it behind and returns to the initial position

(4) If the robot on the distance of 0.7 from the golden token and absolute golden angle is less than 90 degress, then:
	(a) If angle is more or equal to 25: Robot turns left
	(b) If angle is less or equal to -25: Robot turns right
	(c) Otherwise, a special avoiding case is executed which checks where to turn depending on the closest golden token distance
"""

while 1:
	dist_silver, rot_silver = find_silver_token()
	dist_golden, rot_golden = find_golden_token()	
	
	# When silver token is near and ready to be grabbed (2) and (3)
	if dist_silver < d_th:
		print("Silver token detected!")
		if R.grab():
			place_silver_token()
	
	# Robot moves straight (1)
	if  dist_golden > g_th or abs(rot_golden) > 90.0:	
		if 100.0 > rot_silver > o_th and dist_silver < 1.0:
			turn(10, 0.01)
		elif -o_th > rot_silver > -100.0 and dist_silver < 1.0:
			turn(-10, 0.01)		
		else:
			print("Moving in the search of silver box!")
			drive(30, 0.1)	
			
	# When golden token is near (4)
	elif dist_golden < g_th and abs(rot_golden) < 90.0:
		if rot_golden <= -25.0:
			print("Turn right")
			turn(10, 0.5)
		elif rot_golden >= 25.0:
			print("Turn left")
			turn(-10, 0.5)
		else:
			if special_avoiding_case(): 
				print("Special case: Right!")
				turn(10, 0.5)
			else:
				print("Special case: Left!")
				turn(-10, 0.5)
