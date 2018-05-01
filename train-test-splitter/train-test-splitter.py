# -*- coding: utf-8 -*-

#Imports
import time
import os
import shutil
import numpy as np
import sys
import datetime

#Variables
all_data_dir = ""#/media/intern/Acer/Users/Intern/Desktop/Work/Data/crops"
training_data_dir = ""#/media/intern/Acer/Users/Intern/Desktop/Work/Data/train"
testing_data_dir = ""#/media/intern/Acer/Users/Intern/Desktop/Work/Data/test"
testing_data_pct = 0#0.2
#Functions
def split_dataset_into_test_and_train_sets(all_data_dir, training_data_dir, testing_data_dir, testing_data_pct):
    #Stats
    totalFiles = sum([len(files) for r, d, files in os.walk(all_data_dir)])
    proceFiles = 1
    startTime = time.time()
    # Recreate testing and training directories
    if testing_data_dir.count('/') > 1:
        shutil.rmtree(testing_data_dir, ignore_errors=True)
        os.makedirs(testing_data_dir)
        print("Successfully cleaned/created directory " + testing_data_dir)
    else:
        print("Refusing to delete testing data directory " + testing_data_dir + " as we prevent you from doing stupid things!")

    if training_data_dir.count('/') > 1:
        shutil.rmtree(training_data_dir, ignore_errors=True)
        os.makedirs(training_data_dir)
        print("Successfully cleaned/created directory " + training_data_dir)
    else:
        print("Refusing to delete testing data directory " + training_data_dir + " as we prevent you from doing stupid things!")

    num_training_files = 0
    num_testing_files = 0

    for subdir, dirs, files in os.walk(all_data_dir):
        category_name = os.path.basename(subdir)

        # Don't create a subdirectory for the root directory
        print("\nProcessing " + category_name + " in " + os.path.basename(all_data_dir))
        if category_name == os.path.basename(all_data_dir):
            continue

        training_data_category_dir = training_data_dir + '/' + category_name
        testing_data_category_dir = testing_data_dir + '/' + category_name

        if not os.path.exists(training_data_category_dir):
            os.mkdir(training_data_category_dir)

        if not os.path.exists(testing_data_category_dir):
            os.mkdir(testing_data_category_dir)

        for file in files:
            input_file = os.path.join(subdir, file)
            if np.random.rand(1) < testing_data_pct:
                shutil.copy(input_file, testing_data_dir + '/' + category_name + '/' + file)
                num_testing_files += 1
            else:
                shutil.copy(input_file, training_data_dir + '/' + category_name + '/' + file)
                num_training_files += 1
                
            timeElapsed = time.time() - startTime
            timeLeft = (totalFiles / proceFiles * timeElapsed) - timeElapsed
            proceFiles += 1      
            sys.stdout.write("\rTotal time left - " + str(timeLeft).split(".")[0] + " s")
            sys.stdout.flush()
    print("\nProcessed " + str(num_training_files) + " training files.")
    print("Processed " + str(num_testing_files) + " testing files.")
    print("Time elapsed - " + str(timeElapsed) + " s")

def getAllArgs():
    global all_data_dir, training_data_dir, testing_data_dir, testing_data_pct
    
    try:
        all_data_dir = sys.argv[1]
        if all_data_dir.endswith("/"):
            all_data_dir = all_data_dir[:-1]
    except Exception:
        print("Please, specify at least one argument with directory to process!")
        print("If you want to manually specify input, train output, test output directories and split fraction ratio (0 - 1):")
        print("python3 train-test-splitter.py \"/input_path\" \"0.3\" \"/train_output_path\" \"/test_output_path\" ")
        sys.exit()
        
    try:
        testing_data_pct = sys.argv[2]
    except Exception:
        testing_data_pct = 0.2
        print("Split fraction ratio is not specified. Using default value: " + str(testing_data_pct))         
        
    try:
        training_data_dir = sys.argv[3]
    except Exception:
        now = datetime.datetime.now()
        training_data_dir = all_data_dir + "_train_" + now.strftime("%Y-%m-%d-%H-%M")
        print("Output training data directory is not specified. Using default: " + training_data_dir) 
        
    try:
        testing_data_dir = sys.argv[4]
    except Exception:
        now = datetime.datetime.now()
        testing_data_dir = all_data_dir + "_test_" + now.strftime("%Y-%m-%d-%H-%M")
        print("Output training data directory is not specified. Using default: " + testing_data_dir)      
        
             
#Code
getAllArgs()
split_dataset_into_test_and_train_sets(all_data_dir, training_data_dir, testing_data_dir, testing_data_pct)
