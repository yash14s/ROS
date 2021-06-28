#!/usr/bin/env python

import sys
import rospy
from ros_practice.srv import RectangleAreaService
from ros_practice.srv import RectangleAreaServiceRequest
from ros_practice.srv import RectangleAreaServiceResponse

def rectangle_area_calc_client(x, y):
    rospy.wait_for_service('rect_area_service')
    try:
        rect_area_service = rospy.ServiceProxy('rect_area_service', RectangleAreaService)
        resp = rect_area_service(x, y)
        return resp.area
    except rospy.ServiceException(e):
        print ("Service call failed: %s"%e)

def usage():
    return 

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
    else:
        print ("%s [x y]"%sys.argv[0])
        sys.exit(1)
    print ("Requesting area of rectangle with the dimensions [%f,%f]" %(x, y))
    a = rectangle_area_calc_client(x, y)
    print ("Area of rectangle = %f" %(a))
