#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################Imports
import argparse
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pdb
from scipy import ndimage
import time
import os
import shutil
import sys
import platform
import datetime
import glob
import imageio
import cv2

###############################Global variables
SEPARATOR = ""
instanceCount = 0
###############################Methods
def __init__(self):
    instanceCount += 1
    print("Instance Nr. " + str(instanceCount) + " of imageRescaler created")

def __del__(self):
    class_name = self.__class__.__name__
    print(class_name, "destroyed" )       
    
def definePlatform():
    global SEPARATOR
    plat = platform.system()
    print("Running on " + plat + " platform.")
    if plat == "Windows":
        SEPARATOR = "\\"
    else:
        SEPARATOR = "/"    

def loadImageToArray(str_path):
    inp_img = Image.open(str_path)
    inp_img = inp_img.convert("RGBA")
    inp_img_arr = np.asarray(inp_img)
    inp_img_arr.setflags(write=1)
    #plt.imshow(inp_img_arr)
    plt.show()        
    return inp_img_arr

def rescaleVertImage(inp_img_arr, x, y):
    out_img = Image.new("RGBA", (y, y), color=0)
    out_img = np.asarray(out_img)
    out_img.setflags(write=1)
    #print("inp_img_arr.shape = " + str(inp_img_arr.shape))
    #print("out_img.shape = " + str(out_img.shape))
    for x_pos, x_val in enumerate(inp_img_arr):
        out_img[x_pos] = x_val
    #plt.imshow(out_img)
    #plt.show() 
    return out_img

def rescaleImage(inp_img_arr):
    
    x, y, z = inp_img_arr.shape

    if (x > y):
        #out_img = Image.new("RGBA", (x, x), color=0)
        inp_img_arr = ndimage.rotate(inp_img_arr, -90)
        temp = x
        x = y
        y = temp
        out_img = rescaleVertImage(inp_img_arr, x, y)
        out_img = Image.fromarray(out_img)
        out_img = ndimage.rotate(out_img, 90)

        #plt.imshow(out_img) 
        return out_img

    if (x < y):
        out_img = rescaleVertImage(inp_img_arr, x, y)
        #out = np.asarray(out)
        #plt.imshow(out_img) 
        return out_img

    if (x == y):    
        out_img = inp_img_arr

    return out_img


def recursive_copy_files(source_path, destination_path, override=False):
    """
    Recursive copies files from source  to destination directory.
    :param source_path: source directory
    :param destination_path: destination directory
    :param override if True all files will be overridden otherwise skip if file exist
    :return: count of copied files
    """
    startTime = time.time()
    totalFiles = sum([len(files) for r, d, files in os.walk(source_path)])
    files_count = 0
    
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    items = glob.glob(source_path + SEPARATOR + '*')
    for item in items:
        try:
            if os.path.isdir(item):
                path = os.path.join(destination_path, item.split(SEPARATOR)[-1])
                files_count += recursive_copy_files(source_path=item, destination_path=path, override=override)
            else:
                file = os.path.join(destination_path, item.split(SEPARATOR)[-1])
                if not os.path.exists(file) or override:
                    print("Input " + item)
                    print("Output " + file)
                    base_file, ext = os.path.splitext(file)
                    if ext == ".gif":
                        gif = imageio.mimread(item)
                        #for number, image in enumerate(gif):
                        img = Image.fromarray(gif[len(gif) - 1])
                        outputFileName = base_file + ".png"
                        img.save(outputFileName)
                        img = loadImageToArray(outputFileName)
                        img = rescaleImage(img)
                        img = Image.fromarray(img)
                        os.remove(outputFileName) 
                        img.save(base_file + ".png")
                    if ext == ".mp4":
                        vid = imageio.get_reader(item, 'ffmpeg')
                        vid_length = vid.get_length()
                        nums = [int(vid_length / 8), int(vid_length / 4), int(vid_length / 2), int(vid_length / 1.5)]
                        for num in nums:
                            image = vid.get_data(num)
                            outputFileName = base_file + str(num) + ".png"
                            imageio.imwrite(outputFileName, image)
                            img = loadImageToArray(outputFileName)
                            img = rescaleImage(img)
                            img = Image.fromarray(img)
                            os.remove(outputFileName) 
                            #print(base_file, ext)
                            img.save(base_file + "_"  + str(num) + ".png")
                    else:
                        img = loadImageToArray(item)
                        img = rescaleImage(img)
                        img = Image.fromarray(img)

                        #print(base_file, ext)
                        img.save(base_file + ".png")
                        #shutil.copyfile(item, file)
        except Exception as e:
            print("Exception in recursive_copy_files(): " + str(e))
        files_count += 1                        
        timeElapsed = time.time() - startTime
        timeLeft = (totalFiles / files_count * timeElapsed) - timeElapsed
        sys.stdout.write("\rTotal time left - " + str(timeLeft).split(".")[0] + " s\n")
        sys.stdout.flush()    
        
    return files_count

def parseArgs():
    parser = argparse.ArgumentParser(description='Image Rescaler is a tool to change the aspect ratio of an image without distorting it\'s contents. Recursively scans specified folder and it\' subfolders. In our case(ML), aspect ratio is 1. It adds transparent(RGBA) padding to an image file to make it square. In case if *.gif animation file is specified last frame of it is extracted. Also, program supports mp4 videos, but requires ffmpeg codecs as a dependency for that to work. Output file format is *.png')
    parser.add_argument('-i', '--input_dir', help='Input directory', required=True)
    parser.add_argument('-o', '--output_dir', help='Output directory', default="./img_rescale" + "_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M"), required=False)
    args = vars(parser.parse_args())

    #Chop off / from the end
    if args['input_dir'].endswith("/"):# or args['input_dir'].endswith("\"):
        args['input_dir'] = args['input_dir'][:-1]     

    if args['output_dir'].endswith("/"):# or args['output_dir'].endswith("\"):
        args['output_dir'] = args['output_dir'][:-1]             


    print("Input dir: " + args['input_dir'])
    print("Output dir: " + args['output_dir'])
    return args    
###############################Main method
def main():
    definePlatform()
    args = parseArgs()
    INPUT_DIR = args['input_dir']
    OUTPUT_DIR = args['output_dir']
    recursive_copy_files(INPUT_DIR, OUTPUT_DIR)

if __name__ == '__main__':
    main()