#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge, CvBridgeError
import sys

bridge = CvBridge()

rospy.init_node('tennis_ball_publisher', anonymous=True)
pub = rospy.Publisher('tennis_ball_image', Image, queue_size = 10)
rate = rospy.Rate(25)

video_capture = cv2.VideoCapture('tennis-ball-video.mp4')
i = 0  
while not rospy.is_shutdown():
	ret, frame = video_capture.read()
	image_message = bridge.cv2_to_imgmsg(frame, encoding='bgr8')
	pub.publish(image_message)
	rospy.loginfo("frame %d published",i)
	i+=1
	rate.sleep()
  
