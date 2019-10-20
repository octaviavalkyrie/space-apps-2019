from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import argparse
import RPi.GPIO as GPIO
from sonic import distance, is_ice


GPIO_LED = 26
GPIO_SRV = 17



if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_SRV,GPIO.OUT) 
    GPIO.setup(GPIO_LED, GPIO.OUT)

    servo = GPIO.PWM(GPIO_SRV, 50)     # Sets up pin 11 as a PWM pin
    servo.start(0)               # Starts running PWM on the pin and sets it to 0
    port = '/dev/serial0'

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

    try:
        with open('log.txt', 'a+') as outf:
            sample_time = time.time()
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
                        time.sleep(.01)

                    if count > 0:
                        sample = total/count
                    
                        if is_ice(sample):
                            print("Ice.", sample)
                            GPIO.output(GPIO_LED, True)
                            # log location
                            outf.write("Ice found at (" + str(vehicle.location._lat) + ", " + str(vehicle.location ._lon) + ")\n")
                            
                            # move the servo back and forth
                            if time.time() - sample_time > 5:
                                servo.ChangeDutyCycle(7)     # move to 90 degrees
                                time.sleep(2)                # wait 10 secs
                                servo.ChangeDutyCycle(12)    # move back to zero
                                sample_time = time.time()
                        else:
                            print("Not ice.", sample)
                            GPIO.output(GPIO_LED, False)
                    else:
                        print("unable to collect data!")
                else:
                    GPIO.output(GPIO_LED, False)
                    print("Moving", vehicle.groundspeed)
                time.sleep(.5)

    except KeyboardInterrupt:
        # Close vehicle object before exiting script
        vehicle.close()

        # Clean up outputs
        servo.stop()
        GPIO.cleanup()

        print("Completed")
