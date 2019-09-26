'''
Code performs dead reckoning using wheel encoders which values  are read in in Form of a Float32.
it is asumed that the encoder counts upward when driving forward and downward when drving backwards.

vector3.x =left wheel,
vector3.y=right wheel
'''

import rospy 
import numpy as np
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Vector3
class deadreckoning:
    def __init__(self):

        radius =0.065/2   #heel radius [m]
        axis_len=0.1   #axis length [m]
        increments= 1000 #encoder increments per revolution
        rospy.subscriber("wheel",Vector3,self.encoder_callback)
        pub=rospy.Publisher("dead_reckoning",Odometry,queue_size=10)
        encoder_counter=np.array([0,0])
        
        #                  x y phi
        current_position= [0,0, 0 ]

    def encoder_callback(self,data):
        new_encoder_counter=np.array([data.x,data.y])
        dist    = (new_encoder_counter-self.encoder_counter)/self.increments*2*np.pi*self.radius
        del_s   = 0.5*(dist[0]+dist[1])
        del_phi = 0.5*(dist[0]-dist[1])/axis_len

        movement=np.array([-1*del_s*np.sin(self.current_position[2]+del_phi/2),
                              del_s*np.cos(self.current_position[2]+del_phi/2),
                              del_phi])
        self.current_position=self.current_position+movement

        output=Odometry()
        output.position.x   = self.current_position[0]
        output.position.y   = self.current_position[1]
        output.orientation.z= self.current_position[2]
        self.pub.publish(output)
        encoder_counter=new_encoder_counter
        

if __name__ == "__main__":
    try:
        rospy.init_node("dead_reckoning")
        reck=deadreckoning()
    except rospy.ROSInterrupt:
        rospy.loginfo(" dead reckoning error")

 
