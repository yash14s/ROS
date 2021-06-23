#!/usr/bin/env python
# license removed for brevity
import rospy
from ros_practice.msg import ultrasonic
import random

#create a new publisher. we specify the topic name, then type of message then the queue size
pub = rospy.Publisher('ultrasonic_sensor_topic', ultrasonic, queue_size=10)

#we need to initialize the node
rospy.init_node('ultrasonic_sensor_publisher_node', anonymous=True)

#set the loop rate
rate = rospy.Rate(0.25) # 1hz
#keep publishing until a Ctrl-C is pressed
i = 0
command_list = ['F','B','L','R','S']
while not rospy.is_shutdown():
    ultrasonic_sensor = ultrasonic()
    ultrasonic_sensor.front = 45.25 + (random.random()*100)
    ultrasonic_sensor.back = 45.25 + (random.random()*100)
    ultrasonic_sensor.left = 45.25 + (random.random()*100)
    ultrasonic_sensor.right = 45.25 + (random.random()*100)
    ultrasonic_sensor.command = command_list[random.randint(0,4)]
    rospy.loginfo("I publish reading %d: " %i)
    rospy.loginfo(ultrasonic_sensor)
    pub.publish(ultrasonic_sensor)
    rate.sleep()
    i=i+1

