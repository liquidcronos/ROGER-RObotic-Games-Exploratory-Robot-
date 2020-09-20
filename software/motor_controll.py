#! /usr/bin/env python
from sys import argv
import numpy as np
import rospy

from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

#can be called two times for each wheel
class motor_control:

    def __init__(self):
        #0 = encoder, 1 = desired speed
        rospy.Subscriber(argv[0],  Float32, self.float_callback,0)
        rospy.Subscriber(argv[1],  Float32, self.float_callback,1)

        subscriped_values=np.zeros(2)

        self.output = Twist()
        self.pub = rospy.Publisher("homing_cmd", Twist, queue_size=10)

        while not rospy.is_shutdown():
            #TODO implement digital controller here
            # How To Handle Time ?
            # Each wheel can and should be controlled seperatly -> 2 Node better?
            # rate needs to be specified so that time can be counted on!


    def float_callback(self,data,pos):
        subscriped_values[pos]=data


if  __name__=="__main__":
    rospy.init_node("homing")
    try:
        node=motor_control()

    except rospy.ROSInterruptException:
        pass
