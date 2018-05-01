# -*- coding: utf-8 -*-

#Imports
import time
import os
import shutil
import numpy as np
import sys
import datetime
from PIL import Image
import platform
#Variables
ALL_DATA_DIR = ""#/media/intern/Acer/Users/Intern/Desktop/Work/Data/crops"
COLOUR_IMG_DIR = ""#/media/intern/Acer/Users/Intern/Desktop/Work/Data/train"
GRAYSCALE_IMG_DIR = ""#/media/intern/Acer/Users/Intern/Desktop/Work/Data/test"
SEPARATOR = ""
#Functions
def definePlatform():
    global SEPARATOR
    plat = platform.system()
    print("Running on " + plat + " platform.")
    if plat == "Windows":
        SEPARATOR = "\\"
    else:
        SEPARATOR = "/"
########################################################################
def is_grey_scale(img_path):
    try:
        im = Image.open(img_path).convert('RGB')
        w,h = im.size
        for i in range(w):
            for j in range(h):
                r,g,b = im.getpixel((i,j))
                if r != g != b: return False
        return True
    except Exception as e:
        print("Exception in is_grey_scale()" + str(e))
########################################################################
def split_dataset_into_test_and_train_sets(ALL_DATA_DIR, COLOUR_IMG_DIR, GRAYSCALE_IMG_DIR):
    #Stats
    totalFiles = sum([len(files) for r, d, files in os.walk(ALL_DATA_DIR)])
    proceFiles = 1
    startTime = time.time()
    # Recreate testing and training directories
    if GRAYSCALE_IMG_DIR.count(SEPARATOR) > 1:
        shutil.rmtree(GRAYSCALE_IMG_DIR, ignore_errors=True)
        os.makedirs(GRAYSCALE_IMG_DIR)
        print("Successfully cleaned/created directory " + GRAYSCALE_IMG_DIR)
    else:
        print("Refusing to delete testing data directory " + GRAYSCALE_IMG_DIR + " as we prevent you from doing stupid things!")

    if COLOUR_IMG_DIR.count(SEPARATOR) > 1:
        shutil.rmtree(COLOUR_IMG_DIR, ignore_errors=True)
        os.makedirs(COLOUR_IMG_DIR)
        print("Successfully cleaned/created directory " + COLOUR_IMG_DIR)
    else:
        print("Refusing to delete testing data directory " + COLOUR_IMG_DIR + " as we prevent you from doing stupid things!")

    num_color_imgs = 0
    num_grayscale_imgs = 0

    for subdir, dirs, files in os.walk(ALL_DATA_DIR):
        category_name = os.path.basename(subdir)

        # Don't create a subdirectory for the root directory
        print("\nProcessing " + category_name + " in " + os.path.basename(ALL_DATA_DIR))
        if category_name == os.path.basename(ALL_DATA_DIR):
            continue

        training_data_category_dir = COLOUR_IMG_DIR + SEPARATOR + category_name
        testing_data_category_dir = GRAYSCALE_IMG_DIR + SEPARATOR + category_name

        if not os.path.exists(training_data_category_dir):
            os.mkdir(training_data_category_dir)

        if not os.path.exists(testing_data_category_dir):
            os.mkdir(testing_data_category_dir)

        for file in files:
            input_file = os.path.join(subdir, file)
            if is_grey_scale(input_file):
                try:
                    shutil.copy(input_file, GRAYSCALE_IMG_DIR + SEPARATOR + category_name + SEPARATOR + file)
                except Exception as e:
                    print("Exception in split_dataset_into_test_and_train_sets()" + str(e))
                num_grayscale_imgs += 1
            else:
                try:
                    shutil.copy(input_file, COLOUR_IMG_DIR + SEPARATOR + category_name + SEPARATOR + file)
                except Exception as e:
                    print("Exception in split_dataset_into_test_and_train_sets()" + str(e))
                num_color_imgs += 1
                
            timeElapsed = time.time() - startTime
            timeLeft = (totalFiles / proceFiles * timeElapsed) - timeElapsed
            proceFiles += 1      
            sys.stdout.write("\rTotal time left - " + str(timeLeft).split(".")[0] + " s")
            sys.stdout.flush()

    print("\nProcessed " + str(num_color_imgs) + " training files.")
    print("Processed " + str(num_grayscale_imgs) + " testing files.")
    print("Time elapsed - " + str(timeElapsed) + " s")
########################################################################
def getAllArgs():
    global ALL_DATA_DIR, COLOUR_IMG_DIR, GRAYSCALE_IMG_DIR
    
    try:
        ALL_DATA_DIR = sys.argv[1]
        if ALL_DATA_DIR.endswith(SEPARATOR):
            ALL_DATA_DIR = ALL_DATA_DIR[:-1]
    except Exception:
        print("Please, specify at least one argument with directory to process!")
        print("If you want to manually specify input, color output, grayscale output directories:")
        print("python3 train-test-splitter.py \"/input_path\" \"/color_output_path\" \"/grayscale_output_path\" ")
        sys.exit()
        
    try:
        COLOUR_IMG_DIR = sys.argv[2]
    except Exception:
        now = datetime.datetime.now()
        COLOUR_IMG_DIR = ALL_DATA_DIR + "_color_" + now.strftime("%Y-%m-%d-%H-%M")
        print("Output color data directory is not specified. Using default: " + COLOUR_IMG_DIR) 
        
    try:
        GRAYSCALE_IMG_DIR = sys.argv[3]
    except Exception:
        now = datetime.datetime.now()
        GRAYSCALE_IMG_DIR = ALL_DATA_DIR + "_grayscale_" + now.strftime("%Y-%m-%d-%H-%M")
        print("Output grayscale data directory is not specified. Using default: " + GRAYSCALE_IMG_DIR)      
########################################################################
#Code
definePlatform()
getAllArgs()
split_dataset_into_test_and_train_sets(ALL_DATA_DIR, COLOUR_IMG_DIR, GRAYSCALE_IMG_DIR)
