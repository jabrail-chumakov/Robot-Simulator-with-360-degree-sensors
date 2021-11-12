from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 3 python script

We start from the solution of the exercise 2
Put the main code after the definition of the functions. The code should make the robot:
	- 1) find and grab the closest silver marker (token)
	- 2) move the marker on the right
	- 3) find and grab the closest golden marker (token)
	- 4) move the marker on the right
	- 5) start again from 1

The method see() of the class Robot returns an object whose attribute info.marker_type may be MARKER_TOKEN_GOLD or MARKER_TOKEN_SILVER,
depending of the type of marker (golden or silver).
Modify the code of the exercise2 to make the robot:

1- retrieve the distance and the angle of the closest silver marker. If no silver marker is detected, the robot should rotate in order to find a marker.
2- drive the robot towards the marker and grab it
3- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
4- retrieve the distance and the angle of the closest golden marker. If no golden marker is detected, the robot should rotate in order to find a marker.
5- drive the robot towards the marker and grab it
6- move the marker forward and on the right (when done, you can use the method release() of the class Robot in order to release the marker)
7- start again from 1

	When done, run with:
	$ python run.py exercise3.py

"""


a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

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



while 1:
	dist_silver, rot_silver = find_silver_token()
	dist_golden, rot_golden = find_golden_token()	
	if dist_silver == -1:
		print("Token is not detected!")
		turn(10,1)
	elif dist_silver < d_th:
		print("Token detected!")
		if R.grab():
			print("Token grabbed")
			turn(29.6, 2)
			drive(20,1)
			R.release()
			drive(-20,1)
			print("Token released")
			turn(-29.6,2)
	elif 45.0 > rot_silver > -45.0:	
		if rot_silver > a_th:
			turn(2, 0.5)
		elif rot_silver < -a_th:
			turn(-2, 0.5)
		else:
			print("Silver box is somewhere towards me")
        		drive(30, 0.01)
	elif rot_silver > 150.0 or rot_silver < -150.0:
		if dist_golden != -1 and dist_golden < 0.5 and rot_golden < 0:
			print("Ooops! Golden. Turn right!")
			turn(2, 0.5)
		elif dist_golden != -1 and dist_golden < 0.5 and rot_golden > 0:
			print("Ooops! Golden. Turn left!")
			turn(-2, 0.5)
		else:
			print("I see above 150")
			drive(30, 0.01)
	elif 45.0 < rot_silver < 89.9 or 90.1 < rot_silver < 150.0 or -89.9 < rot_silver < -45 or -150.0 < rot_silver < -90.1:
		if dist_golden != -1 and dist_golden < 0.5 and rot_golden < 0:
			print("Ooops! Golden. Turn right!")
			turn(2, 0.5)
		elif dist_golden != -1 and dist_golden < 0.5 and rot_golden > 0:
			print("Ooops! Golden. Turn left!")
			turn(-2, 0.5)
		else:
			print("I see between 45 and 90")
			drive(30, 0.01)
	elif 89.9 < rot_silver < 90.1:
		print("Turn right a bit!")
		turn(15, 2)
	elif -90.1 <  rot_silver < -89.9:
		print("Turn left a bit!")
		turn(-15, 2)	
