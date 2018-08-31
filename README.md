<h1>machine_learning_tools</h1>

<h2>Collection of data manipulation tools for Machine Learning</h2>

<h3>train-test-splitter</h3>
    Was created to split image sets but can be used for any file type(s). In order to perform the split, *.py script has to be executed with directory-to-split as the first parameter. Script will automatically create train-currentdatetime, test-currentdatetime folders and use 0.2 ratio. Alternatively you can specify training_data_dir, testing_data_dir and testing_data_ratio. Example: <b>python3 train-test-splitter-win.py "all_data_dir" "training_data_dir" "testing_data_dir" "testing_data_ratio"</b> Alternatively: <b>python3 train-test-splitter-win.py "all_data_dir"</b>

<h3>grayscale-img-separator</h3>
    In order to perform the split, *.py script has to be executed with directory-to-split as the first parameter. Script will automatically create color-currentdatetime, grayscale-currentdatetime folders. Alternatively you can specify color_data_dir, grayscale_data_dir. Example: <b>python3 train-test-splitter-win.py "all_data_dir" "color_data_dir" "grayscale_data_dir"</b> Alternatively: <b>python3 train-test-splitter-win.py "all_data_dir"</b>

<h3>img-rescaler</h3>
    Image Rescaler is a tool to change the aspect ratio of an image without distorting it\'s contents. Recursively scans specified folder and it\' subfolders. In our case(ML), aspect ratio is 1. It adds transparent(RGBA) padding to an image file to make it square. In case if *.gif animation file is specified last frame of it is extracted. Also, program supports mp4 videos, but requires ffmpeg codecs as a dependency for that to work. Output file format is *.png Example: <b>python3 image_rescaler.py -i "input_directory" -o "output_directory"</b>

<h3>img-video-text-recognition</h3>
    Text-recognition tool based on Pytesseract libraries.
    
<h3>random-sentence-generator-alexify</h3>
    Tool that generates random sentences from given list of words.
    
<h3>klearn.pipeline2.Pipeline2</h3>
    Code that wraps around default scikit-learn Pipeline labrary. It extends the functionality of standard Pipeline by analysing data with predict-probabilty method of default Pipeline and renames the predicted class to "not_sure" if the probability of prediction is less than specified treshold. By default treshold is set to 75%. 
    
<h3>hardware-tests</h3>
    Collection of tests to determine if the GPU set-up and tensorflow / keras is working
