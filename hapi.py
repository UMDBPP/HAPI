import os
import sys

sys.path.append(os.path.join(os.path.realpath(__file__), 'ivport-v2'))

import ivport


def capture(camera):
    cmd = f'raspistill -t 10 -o still_CAM{camera}.jpg'
    os.system(cmd)


with ivport.IVPort(ivport.TYPE_DUAL2) as multiplexor:
    multiplexor.camera_change(1)
    capture(1)

    multiplexor.camera_change(2)
    capture(2)
