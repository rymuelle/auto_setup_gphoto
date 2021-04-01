import os
import numpy as np
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-r", "--run",
                  action="store_true", dest="run", default=False,
                  help="run the gphoto commands")
parser.add_option("-n", type="int", dest="n_dev", help="number of loopbacks to start", default=5)
parser.add_option("-s", type="int", dest="start", help="starting /dev/video number", default=10)

(options, args) = parser.parse_args()

#initilize video loopback dev
n_dev = options.n_dev
start = options.start
dev_list = np.arange(n_dev) + start
dev_list = str(dev_list)[1:-1].replace(" ",",")
modprobe_command = "sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2 devices={} video_nr={}".format(n_dev,dev_list)
print(modprobe_command)
if options.run:
    os.system(modprobe_command)

