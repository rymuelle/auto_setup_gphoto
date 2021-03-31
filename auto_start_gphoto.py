#/dev/video0 == obs virtual camera
#turn auto power off to disable on all cameras

import os
import numpy as np 
import subprocess
import io

#initilize video loopback dev
n_dev = 10
start = 10
dev_list = np.arange(n_dev) + start
dev_list = str(dev_list)[1:-1].replace(" ",",")
modprobe_command = "sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2 devices={} video_nr={}".format(n_dev,dev_list)
os.system(modprobe_command)

def get_text_command(cmd): 
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_usb_num(gphoto2_str): 
    return gphoto2_str.split("usb:")[1].replace(" ","")

def get_owner_name(usb): 
    output =  get_text_command("gphoto2 --get-config ownername --port=usb:{}".format(usb))
    output = output.split("\n")
    for out in output:
        if "Current: " in out:
            return out.replace("Current: ", "")

def get_camera_list():
    result = get_text_command("gphoto2 --auto-detect")
    camera_list = result.split("\n")
    camera_list = camera_list[2:-1]
    usb_list = list(map(get_usb_num, camera_list))
    ownername_list = []
    
    for port in usb_list:
        print(get_owner_name(port))
get_camera_list()


