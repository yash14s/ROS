#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
import time

def scan_callback(scan_data):
    avoidance(scan_data)

def avoidance(distance):
	velocity_msg = Twist()
	can_move = False
	rotate_clk = False
	count_clk = 0; count_anticlk = 0
	speed = 0.5
	omega = 1
	loop_rate = rospy.Rate(10)
	
	for i in range(-5,6):
		if(distance.ranges[i] > 0.6):
			can_move = True
			break
			
	if can_move:
		velocity_msg.linear.x = speed
		velocity_msg.angular.z = 0.0
		
	else:
		velocity_msg.linear.x = 0.0
		for i in range(-5,6):
			if(i < 0 and distance.ranges[i] > 3):
				count_anticlk+=1
			if(i > 0 and distance.ranges[i] > 3):
				count_clk+=1
				
		if count_clk > count_anticlk:
			rotate_clk = True
			omega = -1
			
		velocity_msg.angular.z = omega		
				
	pub.publish(velocity_msg)

if __name__ == '__main__':
    rospy.init_node('obstacle_avoider', anonymous=True) 
    rospy.Subscriber('scan', LaserScan, scan_callback)
    pub = rospy.Publisher('/cmd_vel' , Twist , queue_size=10)
    time.sleep(3)
    rospy.spin()
