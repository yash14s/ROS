#!/usr/bin/env python
import rospy
from ros_practice.msg import ultrasonic

def ultrasonic_sensor_callback(ultrasonic_sensor_message):
    rospy.loginfo("new ultrasonic data received: (%.2f, %.2f, %.2f, %.2f, %s)", 
        ultrasonic_sensor_message.front,ultrasonic_sensor_message.back,
        ultrasonic_sensor_message.left,ultrasonic_sensor_message.right, ultrasonic_sensor_message.command)
    
rospy.init_node('ultrasonic_sensor_subscriber_node', anonymous=True)

rospy.Subscriber("ultrasonic_sensor_topic", ultrasonic, ultrasonic_sensor_callback)

rospy.spin()
