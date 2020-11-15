# Car_abuse_rate

Calculate the Mechanical and the Body treatments scores

Hardware Required:

-OBD2 Scanner device

-Microprocessor Raspberry Pi

-Module GSM

-Module MPU6050

Data Collection:

-Data collection: collected Mechanical treatments through OBD2 scanner devices that connected to ECU (pyobd-pi).

-Data collection: Collected Body treatments through module MPU6050, the Gyroscope and Accelerometer (Gyro_Record.py).

-Data transmission: The GSM A6 module wirelessly transmits the data collected to the CAR Portal Server (client.py).

Before proceeding, run:

Note: For the following command line instructions, do not type the '#', that is only to indicate that it is a command to enter. 

#sudo apt-get update

#sudo apt-get upgrade

#sudo apt-get autoremove

#sudo reboot

#sudo apt-get install python-serial
