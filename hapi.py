import os
import sys
import time

sys.path.append(os.path.join(os.path.realpath(__file__), 'ivport'))

# import picamera multiplexer
import ivport

# import IMU library
from ctypes import *

imu_lib = cdll.LoadLibrary('../lib/liblsm9ds1cwrapper.so')

# define path to log directory
log_dir = os.path.join('/home/pi/Desktop', 'hapi_log', time.strftime('%Y%m%d_%H%M%S_%Z'))

# define log filenames
cam_logfile_path = os.path.join(log_dir, 'cam.csv')
imu_logfile_path = os.path.join(log_dir, 'imu.csv')
rtc_logfile_path = os.path.join(log_dir, 'rtc.csv')

# write headers to log files
with open(cam_logfile_path, 'w') as cam_logfile:
    cam_logfile.write('sys_time,camera,file_path')

with open(imu_logfile_path, 'w') as imu_logfile:
    imu_logfile.write('sys_time,gyro_x,gyro_y,gyro_z,accel_x,accel_y,accel_z,mag_x,mag_y,mag_z')

with open(rtc_logfile_path, 'w') as rtc_logfile:
    rtc_logfile.write('sys_time,rtc_time')

# define seconds for which script will run before exiting
timeout_seconds = 6000

# define seconds between camera captures
picamera_capture_interval = 15


# function that calls shell command to take still from current picamera
def capture_image(camera_index):
    os.system('raspistill -t 10 -o /home/pi/Desktop/hapi_images/still_CAM' + str(camera_index) + '.jpg')


# function that reads IMU data and returns a dictionary
def get_imu_data(imu):
    while imu_lib.lsm9ds1_gyroAvailable(imu) == 0:
        pass
    imu_lib.lsm9ds1_readGyro(imu)
    while imu_lib.lsm9ds1_accelAvailable(imu) == 0:
        pass
    imu_lib.lsm9ds1_readAccel(imu)
    while imu_lib.lsm9ds1_magAvailable(imu) == 0:
        pass
    imu_lib.lsm9ds1_readMag(imu)

    gyro = {'x': imu_lib.lsm9ds1_calcGyro(imu, imu_lib.lsm9ds1_getGyroX(imu)),
            'y': imu_lib.lsm9ds1_calcGyro(imu, imu_lib.lsm9ds1_getGyroY(imu)),
            'z': imu_lib.lsm9ds1_calcGyro(imu, imu_lib.lsm9ds1_getGyroZ(imu))}
    accel = {'x': imu_lib.lsm9ds1_calcAccel(imu, imu_lib.lsm9ds1_getAccelX(imu)),
             'y': imu_lib.lsm9ds1_calcAccel(imu, imu_lib.lsm9ds1_getAccelY(imu)),
             'z': imu_lib.lsm9ds1_calcAccel(imu, imu_lib.lsm9ds1_getAccelZ(imu))}
    mag = {'x': imu_lib.lsm9ds1_calcMag(imu, imu_lib.lsm9ds1_getMagX(imu)),
           'y': imu_lib.lsm9ds1_calcMag(imu, imu_lib.lsm9ds1_getMagY(imu)),
           'z': imu_lib.lsm9ds1_calcMag(imu, imu_lib.lsm9ds1_getMagZ(imu))}

    return {'gyro': gyro, 'accel': accel, 'mag': mag}


logging_start_time = time.time()

multiplexer = ivport.IVPort(ivport.TYPE_QUAD2)

imu = imu_lib.lsm9ds1_create()
imu_lib.lsm9ds1_begin(imu)

if imu_lib.lsm9ds1_begin(imu) == 0:
    print('Failed to communicate with LSM9DS1.')
quit()

imu_lib.lsm9ds1_calibrate(imu)

while time.time() < logging_start_time + timeout_seconds:
    imu_data = get_imu_data()

    with open(imu_logfile_path, 'a') as imu_logfile:
        imu_logfile.write(
            '%s,%f,%f,%f,%f,%f,%f,%f,%f,%f' % (
                time.strftime('%Y%m%d_%H%M%S_%Z'), imu_data['gyro']['x'], imu_data['gyro']['y'],
                imu_data['gyro']['z'], imu_data['accel']['x'], imu_data['accel']['y'], imu_data['accel']['z'],
                imu_data['mag']['x'], imu_data['mag']['y'], imu_data['mag']['z']))

    multiplexer.camera_change(1)
    capture_image(1)

    multiplexer.camera_change(2)
    capture_image(2)

    multiplexer.camera_change(3)
    capture_image(3)

    multiplexer.camera_change(4)
    capture_image(4)

    time.sleep(picamera_capture_interval)

multiplexer.close()
