#!/usr/bin/env python

import obd_io
import serial
import string
import platform
import obd_sensors
from datetime import datetime
import time
import getpass
import glob
import os.path


from obd_utils import scanSerial

class OBD_Recorder():
    def __init__(self, path, log_items):
        self.port = None
        self.sensorlist = []
        localtime = time.localtime(time.time())
        filename = path+"car-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"
        filenameflag = '/home/pi/Desktop/pyobd-pi/Flags/'+"car-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"
	self.log_file = open(filename, "w", 128)
	self.log_file_flag = open(filenameflag,"w", 128)
        self.log_file.write("Time,\t RPM,\t KPH,\t C,\t int,\t tstring,\t min,\t Km,\t char\n");

        for item in log_items:
            self.add_log_item(item)
		
        #self.gear_ratios = [34/13, 39/21, 36/23, 27/20, 26/21, 25/22]
        #log_formatter = logging.Formatter('%(asctime)s.%(msecs).03d,%(message)s', "%H:%M:%S")

    def connect(self):
        portnames = scanSerial()
        #portnames = ['COM10']
        print portnames
        for port in portnames:
            self.port = obd_io.OBDPort(port, None, 2, 2)
            if(self.port.State == 0):
				self.port.close()
				self.port = None
            else:
                localtime = datetime.now()
		current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+"."+str(localtime.microsecond)
	        log_string = current_time
                logtime = "Time:" + str(current_time) + "\t"+ "The OBD Not connected"
		logtimenotcon = '/home/pi/Desktop/pyobd-pi/Score/'+"car-"+str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+".log"
                logtime_file = open(logtimenotcon, "w", 128)
                logtime_file.write(logtime+"\n")
                break

        if(self.port):
            print "Connected to "+self.port.port.name
            
    def is_connected(self):
        return self.port
        
    def add_log_item(self, item):
        for index, e in enumerate(obd_sensors.SENSORS):
            if(item == e.shortname):
                self.sensorlist.append(index)
                print "Logging item: "+e.name
                break
            
            
    def record_data(self):
        if(self.port is None):
            return None
        
        print "Logging started"
        
        while 1:
            localtime = datetime.now()
            current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+"."+str(localtime.microsecond)
            log_string = current_time
            results = {}
            for index in self.sensorlist:
                (name, value, unit) = self.port.sensor(index)
                log_string = log_string + ","+str(value)
                results[obd_sensors.SENSORS[index].shortname] = value;
			
		#VIN = "NAAN11FC3FK834458"
            #gear = self.calculate_gear(results["rpm"], results["speed"])
	    Set_Flag_Score = self.Set_Flag(results["rpm"], results["temp"])
            #log_string = log_string
	    log_Flags = str(Set_Flag_Score)
            self.log_file.write(log_string+"\n")
	    self.log_file_flag.write(log_Flags+"\n")

    
    def Set_Flag(self, rpm, temp):
	if (rpm < 4000 and temp < 60):
	    Flag_Blue = 1
	    Set_Flag_record = 'Flag_Blue'
	    Flag_Score = 0.1
	    return Flag_Score
########RPM Normal and Coolant Normal
	elif (rpm < 4000 and (temp >= 60 and temp < 120)):
	    Flag_Green = 1
	    Set_Flag_record = 'Flag_Green'
	    Flag_Score = 0
	    return Flag_Score
########RPM Normal and Coolant high
	elif (rpm < 4000 and temp >= 120):
	    Flag_Yellow = 1
	    Set_Flag_record = 'Flag_Yellow'
	    Flag_Score = 0.3
	    return Flag_Score
########RPM high and Coolant Low
	elif ((rpm >= 4000 and rpm < 6000) and temp < 60):
	    Flag_Orange = 1
	    Set_Flag_record = 'Flag_Orange'
	    Flag_Score = 0.6
	    return Flag_Score
########RPM high and Coolant Normal
	elif ((rpm >= 4000 and rpm < 6000) & (temp >= 60 and temp < 120)):
	    Flag_Blue = 1
	    Set_Flag_record = 'Flag_Blue'
	    Flag_Score = 0.1
	    return Flag_Score
########RPM high and Coolant high
	elif ((rpm >= 4000 and rpm < 6000) and temp >= 120):
	    Flag_Orange = 1
	    Set_Flag_record ='Flag_Orange'
	    Flag_Score = 0.6
	    return Flag_Score
########RPM too high and Coolant Low
	elif (rpm >= 6000 and temp < 60):
	    Flag_Red = 1
	    Set_Flag_record = 'Flag_Red'
	    Flag_Score = 1
	    return Flag_Score
########RPM too high and Coolant Normal
	elif (rpm >= 6000 and (temp >= 60 and temp < 120)):
	    Flag_Orange = 1
	    Set_Flag_record = 'Flag_Orange'
	    Flag_Score = 0.6
	    return Flag_Score
########RPM too high and Coolant high
	elif (rpm >= 6000 and temp >= 120):
	    Flag_Red = 1
	    Set_Flag_record = 'Flag_Red'
	    Flag_Score = 1
	    return Flag_Score


    
def Average_Score():
    import glob
    import os.path
    import os
    current_directory = os.path.abspath('/home/pi/Desktop/pyobd-pi/Flags')
    current_directory1 = os.path.abspath('/home/pi/Desktop/pyobd-pi/Last-score')
    current_directory2 = os.path.abspath('/home/pi/Desktop/pyobd-pi/Last-len')
    #print(current_directory)
    filename_list = glob.glob1(current_directory,'car-*.txt')
    log_lenght = open(current_directory2 + '/' +'Len', "r")
    last_lenght = log_lenght.readline()
    log_lenght.close()
    #print filename_list
    mean = 0
    current_len = 0
    last_score_file = open(current_directory1 +'/'+'Score','r')
    last_score = last_score_file.readline()
    last_score_file.close()
    for files in filename_list:
	infile = open(current_directory+'/'+files, 'r')
	#print infile

	numbers = [float(line) for line in infile.readlines()]
	infile.close()
	current_len = len(numbers)
	mean = sum(numbers)/len(numbers)
	#print(mean)
	#infile.deleted()
	myfile = "current_directory/filename_list"
	os.remove(myfile)

    localtime = time.localtime(time.time())
    #log_lenght.write(str(float(last_lenght)))
    filename = "/home/pi/Desktop/pyobd-pi/Score/Score_Trip_" + str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"
    final_score = ((mean + float(last_score)) / 2)     
    Flag_Trip = open(filename, "w", 128)
    localtime = datetime.now()
    current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)
    log_string = "Time:" + str(current_time) + "\t" + "Score OBD: " + str(final_score)
    Flag_Trip.write(log_string + "\n")
   

		
username = getpass.getuser()  
logitems = ["rpm", "speed", "temp", "dtc_status", "engine_mil_time", "Throttle_posi"]
logFlagScore = ["Set_Flag_Score"]

o = OBD_Recorder('/home/pi/Desktop/pyobd-pi/log/Record_Data/', logitems)
c = OBD_Recorder('/home/pi/Desktop/pyobd-pi/Flags/', logFlagScore)
o.connect()
c.connect()

if(not o.is_connected()):
    localtime = datetime.now()
    current_time = str(localtime.year)+"-"+str(localtime.month)+"-"+str(localtime.day)+"-"+str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)
    log_string = current_time
    logerror = "Time:" + str(current_time) + "\t"+ "The OBD is not connected"
    logtimenotcon = '/home/pi/Desktop/pyobd-pi/Score/'+'Score_Trip_Error-'+current_time
    logtime_file = open(logtimenotcon, "w", 128)
    logtime_file.write(logerror+"\n")
    logtime_file.close()
    print "Not connected"
    
Average_Score()
o.record_data()
c.record_data()
Average_Score()
#if not c.is_connected():
#    print "Not recorded Flags"
#c.record_data()

