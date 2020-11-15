import requests
import json
import glob
import os.path
import os
import io
import time
import errno
url = 'https://api.backendless.com/92F3C2B3-F512-6540-FFC7-65912EB9F000/D32DE689-ED90-8479-FF3E-C94386701C00/data/CAR'
#####----Score----######
current_directory_Score = os.path.abspath('/home/pi/Desktop/pyobd-pi/Score')
filename_list = glob.glob1(current_directory_Score,'Score_Trip_*')
score_data = ""
for files in filename_list:
	infile = open(current_directory_Score+'/'+files, 'r')
	score_data = infile.read()
if(os.path.exists('/home/pi/Desktop/pyobd-pi/Score/Score_Trip_*')):
	os.remove(current_directory_Score+'/'+files)
else:
	pass
########------Data----#########
current_directory_Data = os.path.abspath('/home/pi/Desktop/pyobd-pi/log/Record_Data')
filename_list_data = glob.glob1(current_directory_Data,'car-*')
log_data = ""
for files in filename_list_data:
	infile = open(current_directory_Data+'/'+files, 'r')
	log_data = infile.read()
if(os.path.exists('/home/pi/Desktop/pyobd-pi/log/Record_Data/car-*')):
	os.remove(current_directory_Data+'/'+files)
else:
	pass
######-----Gyro----#########	
current_directory_Gyro = os.path.abspath('/home/pi/Desktop/Gyro_log/Score')
filename_Gyro = glob.glob1(current_directory_Gyro,'car-*')
log_count_point = ""
for files in filename_Gyro:
	infile = open(current_directory_Gyro+'/'+files, 'r')
	log_count_point = infile.read()
if(os.path.exists('/home/pi/Desktop/Gyro_log/Counter/car_*')):
	os.remove(current_directory_Gyro+'/'+files)
else:
	pass


score_content = json.dumps({'OBD': score_data, 'IMU': log_count_point}).encode('utf-8')
#payload = '{"Data_Recorder":"car-24-5-23-4.txt","Score":"'+score_data.encode('utf8').replace("\n","")+'","Time":"2018/2/3 11:2:5"}'
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=score_content, headers=headers)
print(r)
