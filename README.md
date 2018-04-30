<h1>machine_learning_tools</h1>

<h2>Collection of data manipulation tools for Machine Learning</h2>

<h3>train-test-splitter</h3>
    Was created to split image sets but can be used for any file type(s). In order to perform the split, *.py script has to be executed with directory-to-split as the first parameter. Script will automatically create train-currentdatetime, test-currentdatetime folders and use 0.2 ratio. Alternatively you can specify training_data_dir, testing_data_dir and testing_data_ratio. Example: <b>python3 train-test-splitter-win.py "all_data_dir" "training_data_dir" "testing_data_dir" "testing_data_ratio"</b> Alternatively: <b>python3 train-test-splitter-win.py "all_data_dir"</b>

