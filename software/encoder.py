#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from sys import argv
import time
import Jetson.GPIO as GPIO
import robot_dimensions as robo

'''
pinsRightEncoder = [24, 22]
pinsLeftEncoder = [16, 18]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)	
GPIO.setup(pinsRightEncoder, GPIO.IN)
GPIO.setup(pinsLeftEncoder, GPIO.IN)
'''

def init(pins, counter):
    print("Init")
    if GPIO.input(pins[0]) == GPIO.HIGH and GPIO.input(pins[1]) == GPIO.HIGH:
        case = 2
    else:
        case = 1
    return case, counter
    
def wait(pins, counter):
    print("wait")
    while True:
        if GPIO.input(pins[0]) == GPIO.HIGH and GPIO.input(pins[1]) == GPIO.HIGH:
            case = 2
            break       
    return case, counter

def high_high(pins, counter):
    print(counter)
    while True:
        if GPIO.input(pins[0]) == GPIO.LOW and GPIO.input(pins[1]) == GPIO.HIGH:
            counter = counter+1
            break
        elif GPIO.input(pins[0]) == GPIO.HIGH and GPIO.input(pins[1]) == GPIO.LOW:
            counter = counter-1
            break
    case = 1
    return case, counter
    




def talker():
    pub = rospy.Publisher(sys.argv[1], Float32, queue_size=10)
    rospy.init_node(sys,argv[1]+"_node", anonymous=True)
    counter = 0
    pins=[robo.encoder_pins[int(sys.argv[2])],robo.encoder_pins[int(sys.argv[3])]]
    case = 0
    options = {0: init,
               1: wait,
               2: high_high}
    #rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        case, counter = options[case](pins, counter)
        pub.publish(counter) 
        #rate.sleep()

if __name__ == '__main__':
 try:
     talker()
 except rospy.ROSInterruptException:
     pass
