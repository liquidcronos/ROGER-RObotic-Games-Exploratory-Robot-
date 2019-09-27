from numpy import pi
# distance between the two driving wheels
axis_length = 0.1  #[m]
#radius of the driving wheel
wheel_radius= 0.065 #[m]
# increments of the wheel encoders
encoder_increments= 1000
#sonar sensor orientation in 2d
sonar_angles=pi*[0,0.25,0.5,0.75,1,1.25,1.5,1.75]
#sonar sensor trigger pin configuration
sonar_pins_in=[0,1,2,3,4,5,6,7]
#sonar echo pin configuration
sonar_pins_out=[8,9,10,11,12,13,14,15]

'''
Sonar sensor indexing, top is front
         0
     7  ___  1
      /     \
   6  |     | 2
      |     |
   5  \____/  3      
        4
'''


#maximum robot velocity
max_vel= 2 #[m/s]
