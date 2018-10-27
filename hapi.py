import os
import sys
import time

sys.path.append(os.path.join(os.path.realpath(__file__), 'ivport'))

import ivport.ivport

timeout_seconds = 30
picamera_capture_interval = 5

def capture(camera):
    cmd = 'raspistill -t 10 -o /home/pi/Desktop/hapi_images/still_CAM' + camera + '.jpg'
    os.system(cmd)

image_index = 0

logging_start_time = time.time()

with ivport.IVPort(ivport.TYPE_QUAD2) as multiplexer:
    while time.time() < logging_start_time + timeout_seconds:
        multiplexer.camera_change(1)
        capture(1)

        multiplexer.camera_change(2)
        capture(2)

        multiplexer.camera_change(3)
        capture(3)

        multiplexer.camera_change(4)
        capture(4)

        time.sleep(picamera_capture_interval)