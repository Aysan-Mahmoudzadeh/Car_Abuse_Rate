import smbus			#import SMBus module of I2C
from time import sleep          #import
import time
from datetime import datetime
import os.path
import math
import glob
import os.path
import os
import io
import time
from Kalman import KalmanAngle

kalmanX = KalmanAngle()
kalmanY = KalmanAngle()

RestrictPitch = True	
radToDeg = 57.2957786
kalAngleX = 0
kalAngleY = 0
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
			value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

acc_x = read_raw_data(ACCEL_XOUT_H)
acc_y = read_raw_data(ACCEL_YOUT_H)
acc_z = read_raw_data(ACCEL_ZOUT_H)
gyro_x = read_raw_data(GYRO_XOUT_H)
gyro_y = read_raw_data(GYRO_YOUT_H)
gyro_z = read_raw_data(GYRO_ZOUT_H)

Ax = acc_x/16384.0
Ay = acc_y/16384.0
Az = acc_z/16384.0	
Gx = gyro_x/131.0
Gy = gyro_y/131.0
Gz = gyro_z/131.0
	
if (RestrictPitch):
    roll = math.atan2(acc_y,acc_z) * radToDeg
    pitch = math.atan(-acc_x/math.sqrt((acc_y**2)+(acc_z**2))) * radToDeg
else:
    roll = math.atan(acc_y/math.sqrt((acc_x**2)+(acc_z**2))) * radToDeg
    pitch = math.atan2(-acc_x,acc_z) * radToDeg
#print(roll)
kalmanX.setAngle(roll)
kalmanY.setAngle(pitch)
gyroXAngle = roll;
gyroYAngle = pitch;
compAngleX = roll;
compAngleY = pitch;


#print (" Reading Data of Gyroscope and Accelerometer")

localtime = time.localtime(time.time())

current_directory1 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/Ax')
current_directory2 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/Ay')
current_directory3 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/Az')
current_directory4 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/Gx')
current_directory5 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/Gy')
current_directory6 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/Gz')
current_directory7 = os.path.abspath('/home/pi/Desktop/Gyro_log/Filter/kalman/x')
current_directory8 = os.path.abspath('/home/pi/Desktop/Gyro_log/Filter/kalman/y')
current_directory9 = os.path.abspath('/home/pi/Desktop/Gyro_log/Filter/comp/x')
current_directory10 = os.path.abspath('/home/pi/Desktop/Gyro_log/Filter/comp/y')
current_directory11 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/roll')
current_directory12 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/pitch')
current_directory13 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/gyroXangle')
current_directory14 = os.path.abspath('/home/pi/Desktop/Gyro_log/Gyro-acc/gyroYangle')
# 
angle_x = 0
angle_y = 0
angle_z = 0
filename ="car-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"

log_file_Ax = open(current_directory1 + '/' +filename, "a", 128)
log_file_Ay = open(current_directory2 + '/' +filename, "a", 128)
log_file_Az = open(current_directory3 + '/' +filename, "a", 128)
log_file_Gx = open(current_directory4 + '/' +filename, "a", 128)
log_file_Gy = open(current_directory5 + '/' +filename, "a", 128)
log_file_Gz = open(current_directory6 + '/' +filename, "a", 128)
log_file_kalmanx = open(current_directory7 + '/' +filename, "a", 128)
log_file_kamlany = open(current_directory8 + '/' +filename, "a", 128)
log_file_compx = open(current_directory9 + '/' +filename, "a", 128)
log_file_compy = open(current_directory10 + '/' +filename, "a", 128)
log_file_roll = open(current_directory11 + '/' +filename, "a", 128)
log_file_pitch = open(current_directory12 + '/' +filename, "a", 128)
log_file_gyroXangle = open(current_directory13 + '/' +filename, "a", 128)
log_file_gyroYangle = open(current_directory14 + '/' +filename, "a", 128)
    
flag = 0
timer = time.time()
score = 0
counter = 0
score_IMU = 0
while True:
	if(flag >10000): #Problem with the connection
	    localtime = time.localtime(time.time())
	    current_time = str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])
	    log_file_score.write("Time:" + str(current_time) + "\t" + "There is a problem with the connection")
	    #print("There is a problem with the connection")
	    flag=0
	    continue
	try:
	#Read Accelerometer raw value
            acc_x = read_raw_data(ACCEL_XOUT_H)
	    acc_y = read_raw_data(ACCEL_YOUT_H)
	    acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Read Gyroscope raw value
	    gyro_x = read_raw_data(GYRO_XOUT_H)
	    gyro_y = read_raw_data(GYRO_YOUT_H)
	    gyro_z = read_raw_data(GYRO_ZOUT_H)
	    
	    Ax = acc_x/16384.0
	    Ay = acc_y/16384.0
	    Az = acc_z/16384.0	
	    Gx = gyro_x/131.0
	    Gy = gyro_y/131.0
	    Gz = gyro_z/131.0
	    
	    dt = time.time() - timer
            timer = time.time()
		
	    if (RestrictPitch):
                roll = math.atan2(acc_x,acc_z) * radToDeg
                pitch = math.atan(-acc_x/math.sqrt((acc_y**2)+(acc_z**2))) * radToDeg
	    else:
	        roll = math.atan(acc_y/math.sqrt((acc_x**2)+(acc_z**2))) * radToDeg
	        pitch = math.atan2(-acc_x,acc_z) * radToDeg

	    gyroXRate = gyro_x/131
	    gyroYRate = gyro_y/131
	    gyroZRate = gyro_z/131

	    if (RestrictPitch):
	        if((roll < -90 and kalAngleX >90) or (roll > 90 and kalAngleX < -90)):
	            kalmanX.setAngle(roll)
	            complAngleX = roll
	            kalAngleX   = roll
	            gyroXAngle  = roll
	        else:
	            kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

	        if(abs(kalAngleX)>90):
	            gyroYRate  = -gyroYRate
                    kalAngleY  = kalmanY.getAngle(pitch,gyroYRate,dt)
	    else:

	        if((pitch < -90 and kalAngleY >90) or (pitch > 90 and kalAngleY < -90)):
	            kalmanY.setAngle(pitch)
	            complAngleY = pitch
                    kalAngleY = pitch
                    gyroYAngle = pitch
	        else:
                    kalAngleY = kalmanY.getAngle(pitch,gyroYRate,dt)

	        if(abs(kalAngleY)>90):
	      	    gyroXRate  = -gyroXRate
	      	    kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)

		#angle = (rate of change of angle) * change in time
	    	gyroXAngle = gyroXRate * dt
	    	gyroYAngle = gyroYAngle * dt

		#compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
	    compAngleX = 0.93 * (compAngleX + gyroXRate * dt) + 0.07 * roll
	    compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch

	    if ((gyroXAngle < -180) or (gyroXAngle > 180)):
	       	gyroXAngle = kalAngleX
	    if ((gyroYAngle < -180) or (gyroYAngle > 180)):
	       	gyroYAngle = kalAngleY
	 

	#final_score = scores(self,Az,Gx,Gy,Gz,roll,pitch)
	log_file_Ax.write(str(Ax/16384.0) + "\n")
	log_file_Ay.write(str(Ay/16384.0) + "\n")
	log_file_Az.write(str(Az/16384.0) + "\n")
	log_file_Gx.write(str(Gx/131.0) + "\n")
	log_file_Gy.write(str(Gy/131.0) + "\n")
	log_file_Gz.write(str(Gz/131.0) + "\n")
	log_file_roll.write(str(roll) + "\n")
	log_file_pitch.write(str(pitch) + "\n")
	log_file_kalmanx.write(str(kalAngleX) + "\n")
	log_file_kamlany.write(str(kalAngleY) + "\n")
	log_file_compx.write(str(compAngleX) + "\n")
	log_file_compy.write(str(compAngleY) + "\n")
	log_file_gyroXangle.write(str(gyroXAngle) + "\n")
	log_file_gyroYangle.write(str(gyroYAngle) + "\n")
	localtime = time.localtime(time.time())
	current_time = str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])
log_angle_x.close()
log_angle_y.close()
log_angle_z.close()
log_file_Ax.close()
log_file_Ay.close()
log_file_Az.close()
log_file_Gx.close()
log_file_Gy.close()
log_file_Gz.close()
log_file_roll.close()
log_file_pitch.close()
log_file_kalmanx.close()
log_file_kamlany.close()	
log_file_compx.close()
log_file_compy.close()
log_file_gyroXangle.close()
log_file_gyroYangle.close()
