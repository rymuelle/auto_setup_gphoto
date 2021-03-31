#/dev/video0 == obs virtual camera
#turn auto power off to disable on all cameras

import os
import numpy as np 
import subprocess
import io
import subprocess

#initilize video loopback dev
n_dev = 5
start = 10
dev_list = np.arange(n_dev) + start
dev_list = str(dev_list)[1:-1].replace(" ",",")
modprobe_command = "sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2 devices={} video_nr={}".format(n_dev,dev_list)
print(modprobe_command)
#os.system(modprobe_command)

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

def get_camera_dict():
    result = get_text_command("gphoto2 --auto-detect")
    camera_list = result.split("\n")
    camera_list = camera_list[2:-1]
    usb_list = list(map(get_usb_num, camera_list))
    ownername_dict = {}    
    for port in usb_list:
        ownername_dict[get_owner_name(port)] = port
    return ownername_dict

start_video = "gphoto2 --stdout --capture-movie --port=usb:{} | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 {}"

def run_camera(port,dev):
    os.system(start_video.format(port,dev))

if __name__=="__main__":
    device_map = {'demo1':'/dev/video10', 'demo2':'/dev/video11', 'studio1':'/dev/video12', 'studio2':'/dev/video13'}

    camera_dict = get_camera_dict()
    subprocess.call(['ls','-l','-a'],shell=True)
    for camera in device_map:
        port = camera_dict[camera]
        dev = device_map[camera]
        print(camera,port,dev)
        start_video_command = start_video.format(port,dev)
        print(start_video_command)
        print(start_video_command.split(" "))
        subprocess.Popen([start_video_command],shell=True)
        #run_camera(port,dev)

    #gphoto_command = start_video.format()
    #os.system()
