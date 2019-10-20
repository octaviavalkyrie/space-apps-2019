from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import argparse
import RPi.GPIO as GPIO
from sonic import distance, is_ice


GPIO_LED = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_LED, GPIO.OUT)

# parser = argparse.ArgumentParser()
# parser.add_argument('--connect')
# args = parser.parse_args()

port = '/dev/serial0'  # args.connect

# Connect to the Vehicle.
vehicle = connect(port, wait_ready=True, baud=921600)

# print vehicle state
print("Get some vehicle attribute values:")
print(" GPS: %s" % vehicle.gps_0)
print(" Battery: %s" % vehicle.battery)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Mode: %s" % vehicle.mode.name)    # settable

while True:
    if vehicle.groundspeed < 0.5:
        
        print("stopped ", vehicle.groundspeed)

        total = 0
        count = 0
        for i in range(0, 10):
            dist = distance()
            if dist:
                total += dist
                count += 1
            #print("Measured Distance = %.1f cm" % dist)
            time.sleep(.01)

        sample = total/count
	    
        if is_ice(sample):
            print("Ice.", sample)
            GPIO.output(GPIO_LED, True)
        else:
            print("Not ice.", sample)
            GPIO.output(GPIO_LED, False)
    else:
        GPIO.output(GPIO_LED, False)
        print("Moving", vehicle.groundspeed)
    time.sleep(.5)

# Close vehicle object before exiting script
vehicle.close()

print("Completed")
