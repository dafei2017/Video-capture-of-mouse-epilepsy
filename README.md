# Video-capture-of-mouse-epilepsy
1. Procedure description  
The program is a Python script. Python3 environment and python libraries must be installed before running the program. For details, see requirements. TXT.  
The program mainly includes the following files:  
 
The config.yaml file is the configuration file, requirements. TXT file is the list of software that the project depends on, and run.bat file is the executable file.  
   
Use steps:  
1. Modify the configuration file config.yaml, mainly modifying the video_path parameter to the corresponding video input path.  The output_dir parameter is changed to the corresponding output path  
2. Double-click run.bat to start running.  
   
2. Description of program running results  
After the program runs, a folder named output will be generated under the same directory as the video files, and the final results of the program run will be saved here.  Including the following files:  
 
TXT file, PNG file and npy file are the final results.  
   
 
Hist.png saves the histogram of the difference between frames in X axis of video time.  
   
 
Time_points. TXT saves the time points of the mouse's fast movement calculated based on the mean value of the global difference between frames;  Res.npy is a matrix that holds the difference in motion between frames.  
   
3. Running examples and algorithm description  
After the runtime environment is installed and the correct path is configured, double-click run.bat to start running, and the following screen will appear:  
 
Boolean operation is used to binarize each frame of the video, and the binarized difference between each frame and the next frame is calculated, which is saved into the matrix res.npy and output into the visualized histogram hist.png. According to the mean value of the inter-frame difference of the whole video, the threshold value of epilepsy determination is obtained by multiplying the threshold coefficient.  Compare the difference between all frames to find out the time point when the threshold is exceeded and save it in time_points.txt.  Among them,  
 
The SRC dialog displays the raw information of the input video.  
 
Bin_img displays binary video;  
 
Diff_img displays video information that calculates the difference between frames.  
4. Appendix Description  
V1.zip: program source code;  
Output.zip: The result of the sample video.  
