#! /usr/bin/env python
import numpy as np
import rospy

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


class SimpleHoming:

    def __init__(self):
        rospy.Subscriber('dead_reckoning', Odometry, self.position_callback)

        self.output = Twist()
        self.pub = rospy.Publisher("homing_cmd", Twist, queue_size=10)

        rospy.spin()

    def tuner(self, alpha, rho):
        k_rho_z = 0.8
        k_alpha_z = 1 # 0.3      #1
        k_phi_z = -1
        sigma = 0.1 #to be tuned according to size of arena

        return np.array([k_rho_z * np.cos(alpha) ** 2, k_alpha_z * (1 + np.sin(alpha) ** 2) * (2 - np.exp(-rho ** 2 / sigma ** 2)),
                         k_phi_z * (1 + np.sin(alpha) ** 2) * np.exp(-rho ** 2 / sigma ** 2)])

    def position_callback(self,data):

        rho                 = data.pose.pose.position.x
        alpha               = data.pose.pose.orientation.z
        K = self.tuner(alpha, rho)
        k_rho = K[0]
        k_alpha = K[1]

        self.output.linear.x     = k_rho*rho
        self.output.angular.z    = k_alpha*alpha
        self.pub.publish(self.output)

if  __name__=="__main__":
    rospy.init_node("homing")
    try:
        node=SimpleHoming()

    except rospy.ROSInterruptException:
        pass
