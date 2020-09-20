import numpy as np
# distance between the two driving wheels
axis_length = 0.1  #[m]
#radius of the driving wheel
wheel_radius= 0.065 #[m]
# increments of the wheel encoders
encoder_increments= 1000
#encoder pin configuration
#              A----------B---------------------- left motor
#              v          v          A----------B right motor
#              v          v          V          V
encoder_pins=['SPI2_CS1','SPI2_CS0','SPI1_CS0','SPI1_MISO']
#sonar sensor orientation in 2d
sonar_angles=np.pi*np.array([0,0.25,0.5,0.75,1,1.25,1.5,1.75])
#sonar sensor trigger pin configuration
sonar_pins_out=['AUD_MCLK','SPI2_SCK','SPI1_MOSI','SPI1_SCK','GPIO_PZ0','DAP4_FS','DAP4_DOUT','UART2_CTS']
#sonar echo pin configuration
sonar_pins_in=['UART2_RTS','LCD_TE','SPI1_MISO','CAM_AF_EN','GPIO_PZ6','SPI2_MOSI','DAP4_DIN','LCD_BL_PW']
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
