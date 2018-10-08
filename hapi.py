import os
import sys

sys.path.append(os.path.join(os.path.realpath(__file__), 'ivport-v2'))

import ivport


# raspistill capture
def capture(camera):
    "This system command for raspistill capture"
    cmd = "raspistill -t 10 -o still_CAM%d.jpg" % camera
    os.system(cmd)


with ivport.IVPort(ivport.TYPE_DUAL2) as multiplexor:
    multiplexor.camera_change(1)

    capture(1)
    multiplexor.camera_change(2)
    
    capture(2)
    multiplexor.close()
