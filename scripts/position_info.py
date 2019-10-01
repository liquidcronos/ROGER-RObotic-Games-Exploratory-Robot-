#!/usr/bin/env python
import numpy as np
import rospy
import sys
from nav_msgs.msg import Odometry

'''
slows the odometry informaion rate, needs to be called with desired rate
and name of topic to contrict, will publish to robotic_games/Odometry
'''

def position_callback(data):
    global fast_odo
    fast_odo=data

def constrictor():
    global fast_odo
    rospy.init_node("limited_odometry")
    frequency=rospy.Rate(float(sys.argv[1]))
    rospy.Subscriber(sys.argv[2],Odometry,position_callback)
    pub=rospy.Publisher("robotic_games/Odometry",Odometry,queue_size=1)
    while not rospy.is_shutdown():
        pub.publish(fast_odo)
        frequency.sleep()

if __name__=="__main__":
    global fast_odo
    fast_odo=Odometry()
    try:
        constrictor()
    except rospy.ROSInterruptException:
        pass

