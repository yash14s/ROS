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
	rotate_clk = False
	Kp_speed = 100; max_speed = 0.3
	dist_values = []
	dist_anticlk = 0
	dist_clk = 0
	
	loop_rate = rospy.Rate(50)
	
	for i in range(-5,6):
		if not math.isnan(distance.ranges[i]):
			dist_values.append(distance.ranges[i])
			if(i < 0 and distance.ranges[i]>3):
				dist_anticlk+=1
			if(i > 0 and distance.ranges[i]>3):
				dist_clk+=1
						
	speed = min(Kp_speed*(min(dist_values)-0.3, max_speed))
	if (dist_clk - dist_anticlk) > 0:
		rotate_clk = True
	
	omega = 1
	if rotate_clk:
		omega = -omega

	velocity_msg.linear.x = speed
	velocity_msg.angular.z = omega		
	pub.publish(velocity_msg)
	loop_rate.sleep()

if __name__ == '__main__':
    rospy.init_node('obstacle_avoider', anonymous=True) 
    rospy.Subscriber('scan', LaserScan, scan_callback)
    pub = rospy.Publisher('/cmd_vel' , Twist , queue_size=100)
    time.sleep(3)
    rospy.spin()
