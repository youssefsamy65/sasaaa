import roslibpy
from gpiozero import Servo
from time import sleep
import os
import signal
import sys
lap_host = os.getenv('lap_HOST', 'localhost') 
# Initialize the servos
servo2 = Servo(9)
servo3 = Servo(5)
servo4 = Servo(3)

# Global variable to store the received message
received_message = ""

def message_callback(msg):
    global received_message
    received_message = msg['data']
    
    hi = "hello"
    bye = "bye"

    if hi in received_message or bye in received_message:
        for _ in range(4):
            servo3.max()  # Move servo 3 to max position (180 degrees)
            servo4.value = 0.67  # Move servo 4 to ~150 degrees
            sleep(2)
            servo4.mid()  # Move servo 4 to mid position (90 degrees)
            sleep(0.3)
    elif "shake hands" in received_message:
        for _ in range(4):
            for pos in range(100, 181):  # Move servo 4 from 100 to 180 degrees
                servo4.value = (pos - 90) / 90.0  # Convert to servo range
                sleep(0.015)
            for pos in range(180, 99, -1):  # Move servo 4 from 180 to 100 degrees
                servo4.value = (pos - 90) / 90.0  # Convert to servo range
                sleep(0.015)
    received_message = ""

def main():
    client = roslibpy.Ros(host=lap_host, port=9090)
    client.run()

    listener = roslibpy.Topic(client, '/chatter', 'std_msgs/String')
    listener.subscribe(message_callback)

    try:
        while client.is_connected:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        listener.unsubscribe()
        client.terminate()

if __name__ == '__main__':
    main()

