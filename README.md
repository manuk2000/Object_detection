Mini README File

  This program consists of multiple Python scripts that
  work together to achieve a specific functionality.
  Here's a brief overview of each script and their
  purpose:

  1: background_version.py: This script is responsible
  for processing a video by applying a zoom effect to
  specific regions based on user-defined parameters.
  It utilizes the functions and logic from other scripts
  to accomplish the zooming functionality.
  
  2: tracking/ReduceArr.py: This script contains functions
  to track the position of an object in a video and
  generate a reduced array that represents the object's
  movement over time. The reduced array is used in later
  stages of the program to determine the zoom timing.
  
  3: zoom/ZoomBarrier.py: This script enables the user
  to select the positions of barrier dots in the video,
  which are used as reference points for determining
  the left and right zoom positions.

  4: zoom/times_left_right_zoom.py: This script calculates
  the zoom timing by analyzing the reduced array generated
  by the tracking process. It determines when to switch
  between the left and right zoom positions based on the
  barrier dot positions.
  
  5: zoom/result.py: This script combines all the components
  together to achieve the final result. It reads the
  necessary input files, performs the zooming process
  using the determined positions and timing, and generates
  the processed video with the applied zoom effect.

To see the result of the program, you can run the
result.py file. This script will execute the entire
program and generate the processed video with the
applied zoom effect. Running the result.py file will
provide you with the visual outcome of the zooming
process on the input video.

Also, download the source code file from [this link]
(https://pysource.com/wp-content/uploads/2021/10/
Object-tracking-from-scratch-source_code.zip) and
extract it to the program's root directory.

Please make sure to install OpenCV and download the
source code file before running the program.
