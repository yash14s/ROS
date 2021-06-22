import rospy
import time
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

def move():
    speed_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    while not rospy.is_shutdown():
    	twist = Twist()
    	twist.linear.x = 0.1
    	twist.linear.y = -0.1
    	twist.angular.z = math.pi/4.0
    	speed_publisher.publish(twist)

def position_callback(position_message):
    rospy.loginfo('X: %f' %position_message.x)
    rospy.loginfo('Y: %f' %position_message.y)
    rospy.loginfo('theta: %f' %position_message.theta)
    time.sleep(1)
    
def position_report():
    rospy.init_node('position_status', anonymous=True)
    rospy.Subscriber('/turtle1/pose', Pose, position_callback)
    
if __name__ == '__main__':
    try:
    	position_report()
    	move()
    	rospy.spin()
    except rospy.ROSInterruptException:
        pass
