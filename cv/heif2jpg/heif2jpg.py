# Hint: This program cannot run in Windows because pyheif and whatimage don't support.
import subprocess
import os
import io
import whatimage
import pyheif
import traceback
from PIL import Image
from multiprocessing import Process, Queue 
from io import BytesIO

import numpy as np

result_queue = Queue()

opt_path = ""


class Convert(Process):
    def __init__(self, id, work_q, res_q, opt_path):
        super(Convert, self).__init__()
        self.work_q = work_q
        self.id = id
        self.js = 0
        self.res_q = res_q
        self.opt_path = opt_path

    def decodeImage(self, bytesIo, filename):
        try:
            fmt = whatimage.identify_image(bytesIo)
            # print('fmt = ', fmt)
            if fmt in ['heic']:
                heif_file = pyheif.read(bytesIo)

                name = ""
                for fnm in filename.split("/")[-1].split(".")[:-1]:
                   name += fnm
                
                # print('i = ', i)
                print('%s.size = ' % name, heif_file.size)

                pi = Image.frombytes(heif_file.mode,
                            heif_file.size,
                            heif_file.data,
                            "raw",
                            heif_file.mode,
                            heif_file.stride,
                            )

                pi.save(os.path.join(self.opt_path, name+".jpg"),  format="jpeg", quality=100)
                
                self.js += 1
        except:
            traceback.print_exc()
    

    def read_image_file_rb(self, file_path):
        with open(file_path, 'rb') as f:
            file_data = f.read()
        return file_data
    
    def run(self):
        for f in self.work_q:
            print("Thread %d - Converting:\t" % os.getpid(), f)
            data = self.read_image_file_rb(f)
            self.decodeImage(data, str(f))
        self.res_q.put(self.js)
        exit(0)
 
 
if __name__ == "__main__":
    dir_path = input("Please input the path of source folder: ")
    
    opt_path = "./convert_output/"
    if not os.path.exists(opt_path):
        os.mkdir(opt_path)
    
    file_list = []
    for path, dirs, filenames in os.walk(dir_path):
                    
        for filename in filenames:
            file_path = os.path.join(path, filename)
            file_list.append(file_path)
    
    proc_num = os.cpu_count()
    print("Cpu count:", proc_num)
    processes = []
    step = len(file_list) / proc_num
    for i in range(1, proc_num+1):
        ff = file_list[int((i-1)*step):int(i*step)]
        processes.append(Convert(i, ff, result_queue, opt_path))
    
    for i in range(proc_num):
        processes[i].start()
    
    for i in range(proc_num):
        processes[i].join()
    
    jjs = 0
    while not result_queue.empty():
        jjs += result_queue.get()
            
            
    print("Done! Converted %d files." % jjs)