#!/usr/bin/env python

from ros_practice.srv import RectangleAreaService
from ros_practice.srv import RectangleAreaServiceRequest
from ros_practice.srv import RectangleAreaServiceResponse

import rospy

def handle_calc_area(req):
    print ("Returning area of rectangle with the dimensions [%f,%f]"%(req.w, req.h))
    return RectangleAreaServiceResponse(req.w * req.h)

def rectangle_area_calc_server():
    rospy.init_node('rectangle_area_server_node')
    a = rospy.Service('rect_area_service', RectangleAreaService, handle_calc_area)
    print ("Ready to find rectangle area.")
    rospy.spin()
    
if __name__ == "__main__":
    rectangle_area_calc_server()
