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
  

		
username = getpass.getuser()  
logitems = ["rpm", "speed", "temp", "dtc_status", "engine_mil_time", "Throttle_posi"]

o = OBD_Recorder('/home/pi/Desktop/pyobd-pi/log/Record_Data/', logitems)
o.connect()

if(not o.is_connected()):
    localtime = datetime.now()
    current_time = str(localtime.year)+"-"+str(localtime.month)+"-"+str(localtime.day)+"-"+str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)
    log_string = current_time
    logerror = "Time:" + str(current_time) + "\t"+ "The OBD is not connected"
    logtime_file.write(logerror+"\n")
    logtime_file.close()
    print "Not connected"
    
o.record_data()
#if not c.is_connected():
#    print "Not recorded Flags"
#c.record_data()

