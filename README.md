# RSA-Major-Project-2016

Instructions

1. Make sure you are running Linux (preferably Ubuntu) and not MacOS or Windows (there are some nasty support issues with OpenCV).
2. Install Python, Pip, Jupyter, and OpenCV if you haven’t already. Required Python packages include matplotlib, pickle, pillow, and tkinter.
3. Set the camera up at a point above the opposite side of the field. Make sure you can see all four corners of the half-field in the frame.
4. Once camera is streaming to an IP address, save a frame using save_frame.py. First argument is the IP address the camera is streaming to.
5. Calibrate the transform by using the field corners. Run calibrate_corners.py and click on each of the four corners of the half-field.
6. Run field_observer.py with the IP address as the first argument to start observing the robot and ball on the field. The program will automatically log to a pickled log file named log_file.txt.
7. If you wish to unpickle the log file in order to read it, run convert_pickle.py with the pickled file as the first argument.
8. Retrieve the Nao robot’s log file from its root directory using scp or other means.
9. In order to match the Nao’s log file with the observed log file correctly, we must determine the time difference between the Nao’s system time and the user’s machine. You are able to do this by editing the IP address within time_difference.sh to ssh into the correct Nao robot. Running time_difference.sh will give you the number of milliseconds (positive or negative) the Nao’s time is ahead of your machine’s.
10. Run match_logs.py with the Nao log file, the observed log file, and the time difference in milliseconds as the arguments.
11. The logs will be matched and written into matched_log_file.txt, which is also pickled. You can playback this log using play_log_file.py with the log file as the first argument.
12. A number of statistics tools exist within the Jupyter Python notebook, Statistics.ipynb.
