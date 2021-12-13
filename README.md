HOW TO SET UP CONDA ENV: 

Steps : 


Install Anaconda using following command: 


1. https://docs.anaconda.com/anaconda/install/windows/


Go to above link and follow the instruction

RUN:

1. conda create --name dronetracking    #this step is one time only
2. conda activate dronetracking
3. conda install -c anaconda opencv
4. conda install -c conda-forge tensorflow
5. GO To https://github.com/Mogball/goturn-files and clone the repo. unzip all the caffe model files and put them along with python code file. make sure to have .prototxt also.
6. PULL the our code from github by cloning our repo. ( make sure to put motion-detction.py file in the folder where you unzipped files from above step) 
7. run python motion-detection.py


To deactivate conda enviornment run:
1. conda deactivate
