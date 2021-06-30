#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time


def poseCallback(position_msg):
	global x, y, theta 
	x = position_msg.x
	y = position_msg.y
	theta = position_msg.theta

def move_straight(velocity_pub, speed, distance, is_forward):
	velocity_msg = Twist()
	global x, y
	x0 = x
	y0 = y
	
	if(is_forward):
		velocity_msg.linear.x = abs(speed)
	else:
		velocity_msg.linear.x = -abs(speed)
	
	loop_rate = rospy.Rate(10)
	while True:
		rospy.loginfo("Travelling straight")
		velocity_pub.publish(velocity_msg)
		loop_rate.sleep()
		distance_moved = abs(math.sqrt((x-x0)**2 + (y-y0)**2))
		print(distance_moved)
		
		if (distance_moved>distance):
			break	
	velocity_msg.linear.x = 0.0
	velocity_pub.publish(velocity_msg)
	print("reached")

def rotate(velocity_pub, angular_vel, angular_disp, clockwise):
	velocity_msg = Twist()
	global theta 
	theta0 = theta
	angular_vel = (math.pi/180.0)*angular_vel
	angular_disp = (math.pi/180.0)*angular_disp
	
	if(clockwise):
		velocity_msg.angular.z = -abs(angular_vel)
	else:
		velocity_msg.angular.z = abs(angular_vel)
	
	loop_rate = rospy.Rate(10)
	while True:
		rospy.loginfo("Rotating")
		velocity_pub.publish(velocity_msg)
		loop_rate.sleep()
		angle_rotated = abs(theta - theta0)
		print(angle_rotated)
		if(angle_rotated>angular_disp):
			break
	velocity_msg.angular.z = 0.0
	velocity_pub.publish(velocity_msg)
	print("Rotated")

def go_to_goal(velocity_pub, x_goal, y_goal):
	velocity_msg = Twist()
	global x, y, theta
	
	loop_rate = rospy.Rate(10)
	while True:
		distance = abs(math.sqrt((x_goal-x)**2+(y_goal-y)**2))
		k_vel = 0.5
		linear_vel = distance * k_vel
		k_angular_vel = 4.0
		angular_disp = math.atan2(y_goal-y, x_goal-x)
		angular_vel = (angular_disp - theta) * k_angular_vel
		
		velocity_msg.linear.x = linear_vel
		velocity_msg.angular.z = angular_vel
		velocity_pub.publish(velocity_msg)
		
		print("x=", x,", y=", y, ", distance=",distance)
		if(distance<0.01):
			break
	velocity_msg.linear.x = 0.0
	velocity_msg.angular.z = 0.0
	velocity_pub.publish(velocity_msg)
	print("Reached")
	
def set_desired_orientation(velocity_pub, angular_vel, angle):
	velocity_msg = Twist()
	global theta
	theta_degree = (180.0/math.pi) * theta
	angle_disp = theta_degree - angle
	
	if angle_disp > 0:
		clockwise = True
	else:
		clockwise = False
	
	angle_disp = abs(angle_disp)
	rotate(velocity_pub, angular_vel, angle_disp, clockwise)
	
def spiral_motion(velocity_pub, wk, rk):
	velocity_msg = Twist()
	loop_rate = rospy.Rate(10)
	while (x<10.5 and y<10.5):
		velocity_msg.linear.x = rk
		velocity_msg.angular.z = wk
		velocity_pub.publish(velocity_msg)
		rk = rk + 1
		loop_rate.sleep()
	velocity_msg.linear.x = 0.0
	velocity_msg.angular.z = 0.0
	velocity_pub.publish(velocity_msg)
	
def grid_cleaning(velocity_pub):
	global x,y
	go_to_goal(velocity_pub, 1.0, 1.0)
	
	while (x<10.5 and y<10.5):
		set_desired_orientation(velocity_pub, 30, 90)
		move_straight(velocity_pub, 1.0, 9.0, True)
		rotate(velocity_pub, 30, 90, True)
		move_straight(velocity_pub, 1.0, 1.0, True)
		rotate(velocity_pub, 30, 90, True)
		move_straight(velocity_pub, 1.0, 9.0, True)
		rotate(velocity_pub, 30, 90, False)
		move_straight(velocity_pub, 1.0, 1.0, True)
		
	go_to_goal(velocity_pub, 1.0, 1.0)
		
if __name__ == "__main__":
	try:
		rospy.init_node('turtlesim_cleaning_bot', anonymous = True)
		pose_sub = rospy.Subscriber('/turtle1/pose', Pose, poseCallback)
		velocity_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)
		time.sleep(2)
		
		#move_straight(velocity_pub, 1.0, 3.0, True)
		#rotate(velocity_pub, 30, 90, True)
		#go_to_goal(velocity_pub, 8.0, 1.0)
		#set_desired_orientation(velocity_pub, 30, 180)
		#spiral_motion(velocity_pub, 20, 0)
		grid_cleaning(velocity_pub)
		
	except rospy.ROSInterruptException:
		rospy.loginfo("node terminated.")
		
