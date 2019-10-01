#!/usr/bin/env python
'''
Reads each sonar Sensor, calculates the distance and publishes all sensors via a pintcloud
'''


import Jetson.GPIO as GPIO
import time
import robot_dimensions as robot
import threading
from sensor_msgs.msg import PointCloud



class sonar_thread(threading.Thread):
    def __init__(self,threadID,pin_in,pin_outi,group):
        self.threadID = threadID
        self.pin_in   = pin_in
        self.pin_out  = pin_out
        self.group    = group
    def run(self):
        if self.group == 1:
            while not barrier[0].isSet() or not barrier[2].isSet() or not barrier[4].isSet() or not barrier[6].isSet():
                while not barrier[self.threadID].isSet():
                    distanz(self.pin_in,self.pin_out)
                    barrier[self.threadID].set()
                if self.threadID == 1:
                    if barrier[1].isSet() and barrier[3].isSet() and barrier[5].isSet() and barrier[7].isSet():
                        barrier[0].clear()
                        barrier[2].clear()
                        barrier[4].clear()
                        barrier[6].clear()


        if self.group == 2:
            while not barrier[1].isSet() or not barrier[3].isSet() or not barrier[5].isSet() or not barrier[7].isSet():
                while not barrier[self.threadID].isSet():
                    distanz(self.pin_in,self.pin_out,self.ThreadID)
                    barrier[self.threadID].set()
                if self.threadID == 0:
                    if barrier[0].isSet() and barrier[2].isSet() and barrier[4].isSet() and barrier[6].isSet():
                        pub=rospy.Publisher("Sonar_sensor",PointCloud,queue_size=10)
                        barrier[1].clear()
                        barrier[3].clear()
                        barrier[5].clear()
                        barrier[7].clear()
                        



def distanz(pin_in,pin_out,ID):
    global distances
    # set Trigger on HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger to LOW after 0.01ms
    time.sleep(0.00001)
    GPIO.output(pin_out, False)

    StartZeit = time.time()
    StopZeit = time.time()

    while GPIO.input(pin_in) == 0:
        StartZeit = time.time()

    while GPIO.input(pin_in) == 1:
        StopZeit = time.time()

    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distance = (TimeElapsed * 34300) / 2
    distances[ID]=distance 


def sonar_sensing():
    Pros = []
    while not rospy.is_shutdown():
        # actiave only 4 sensors at a time to avoid crossdetection
        odd_distance=np.zeros(4)
        for i in range(4):
        


if__name__=='__main__':
    try:
        barriers=[threading.Event() for _ in range(8)]
        global distances
        distances=np.zeros(8)
        rospy.init_node("Sonar")
        sonar_sensing()
    except rospy.ROSInterruptException:
        rospy.loginfo("sonar not working")
