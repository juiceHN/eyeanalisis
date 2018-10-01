# Eye behavior analisis with python
no videos nor images included
### Python version
python 3.5.2

-----
### Installation
The use of a virtualenv is recommended.

to install all libraries required run:
```
pip install -r requirements.txt
```

-----
### Usage

Use Blinks.py to get data from a video. It will detect when someone is  blinking. Aditional you can use your number pad to manually track the eye position. Being 5 center, 8 up, 2 down, 4 left, 6 right, 7 upper left, 9 upper right, 1 left down and 3 right down.
```
python3 blinks.py
```
Once it starts running you need to write down the subject's sex. While running you can press down `q` to quit or `ctrl+c` to cancel.

#### Aditional information

You may need to change
* `EYE_AR_THRESH` to adjust necesities for the size of the eye. It's recommended to use any value from 0.27 to 0.3.
* `EYE_AR_CONSEC_FRAMES` to adjust how many frames does the eye needs to be closed to be count as a blink. It's recommended to use 3 as the value.

-----
### Results

After the analisis of the video is done it will create 2 csv files: 'eye_behavior.csv' and 'eye_behavior_summary.csv'. 

'eye_behavior.csv' contains the following data:
1. Name of the video 
2. The second in which a blink was detected
3. A conbination of a direction and the second for eye movement

'eye_behavior_summary.csv' contains the following data:
1. Name of the video
2. Number of frames in the video
3. Number of blinks detected
4. Number of eye movements made
5. Sex
