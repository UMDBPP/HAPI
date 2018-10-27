import os
import sys

# sys.path.append(os.path.join(os.path.realpath(__file__), 'ivport'))

import ivport
import ivport.picamera
import time

# def capture(camera):
#     cmd = f'raspistill -t 10 -o still_CAM{camera}.jpg'
#     os.system(cmd)
#
#
# with ivport.IVPort(ivport.TYPE_QUAD2) as multiplexor:
#     multiplexor.camera_change(1)
#     capture(1)
#
#     multiplexor.camera_change(2)
#     capture(2)

with ivport.picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 90
    camera.start_preview()

    time.sleep(2)    # Camera Initialize
    start = time.time()
    camera.capture_sequence([], use_video_port=True)
    finish = time.time()
