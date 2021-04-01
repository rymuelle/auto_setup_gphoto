#!/usr/bin/env python3
#/dev/video0 == obs virtual camera
#turn auto power off to disable on all cameras

import os
import numpy as np 
import subprocess
import signal
from optparse import OptionParser

def get_text_command(cmd): 
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_usb_num(gphoto2_str): 
    return gphoto2_str.split("usb:")[1].replace(" ","")

def get_owner_name(usb): 
    output =  get_text_command("gphoto2 --get-config ownername --port=usb:{}".format(usb))
    print(output)
    output = output.split("\n")
    for out in output:
        if "Current: " in out:
            return out.replace("Current: ", "")

def get_camera_dict():
    result = get_text_command("gphoto2 --auto-detect")
    print(result)
    camera_list = result.split("\n")
    camera_list = camera_list[2:-1]
    usb_list = list(map(get_usb_num, camera_list))
    ownername_dict = {}    
    for port in usb_list:
        try:
            ownername_dict[get_owner_name(port)] = port
        except:
            print("port {} in use".format(port))
    return ownername_dict

start_video = "/usr/bin/gphoto2 --stdout --capture-movie --port=usb:{}"

send_to_dev = "/usr/bin/ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 {}"

device_map = {'demo1':'/dev/video10', 'demo2':'/dev/video11', 'studio1':'/dev/video12', 'studio2':'/dev/video13'}

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-r", "--run",
                  action="store_true", dest="run", default=False,
                  help="run the gphoto commands")
    (options, args) = parser.parse_args()

    camera_dict = get_camera_dict()
    dev_process = []
    video_process = []

    for camera in camera_dict:
        port, dev = camera_dict[camera], device_map[camera]
        start_video_command = start_video.format(port,dev)
        send_to_dev_command = send_to_dev.format(dev)
        print("===============")
        print(start_video_command)
        print(send_to_dev_command)
        if options.run:
            video_popen = subprocess.Popen(
                start_video_command.split(" "),
                stdout=subprocess.PIPE)
            dev_popen = subprocess.Popen(
                send_to_dev_command.split(" "),
                stdin=video_popen.stdout,
                stdout=subprocess.PIPE)
            dev_process.append(dev_popen)
            video_process.append(video_popen)
                
input("Press Enter to reset cameras...")

for v,d in zip(video_process,dev_process):
    print("killed")
    v.stdout.close()
    d.terminate()
    v.terminate()
    
input("Press Enter to reset cameras...")

