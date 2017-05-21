# canny_edge_my_face
Simple ROS node to apply canny edge detection to your camera image



## Usage
Simply run the pyhton file in src directory, or 
``rosrun canny_edge_my_face edge_detector.py``

### Required packages
- cv_camera
- cv_bridge

### Topics
- images coming from cv_camera are read in topic : `/cv_camera/image_raw`
- the image with detected edge is published to : ``/edge_detector``
