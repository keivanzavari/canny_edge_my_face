#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
KEIVAN . ZAVARI @ GMAIL.COM
"""

import rospy
from sensor_msgs.msg import Image 
import cv2
import cv_bridge

# ----------------
show_edge_image = False
image_edges_ros = Image()
pub = rospy.Publisher('edge_detector', Image, queue_size=10)
# ----------------


def callback(data):
    global show_edge_image
    global image_edges_ros

    # image comes in as sensor_msgs/Image and should be convected to
    # numpy array of openCV
    try:
        image_raw_cv = cv_bridge.CvBridge().imgmsg_to_cv2(data, desired_encoding="passthrough")
    except cv_bridge.CvBridgeError:
        print 'fail'

    # apply Canny edge detecto writh two pre-determined min and max values 
    # from openCV doc:
    # Any edges with intensity gradient more than max value are sure to be 
    # edges and those below minVal are sure to be non-edges, so discarded. 
    edges_cv = cv2.Canny(image_raw_cv,190,300)

    # if you don't like to check the image, turn this off
    if show_edge_image:
        cv2.imshow('face', edges_cv)
        cv2.waitKey(1000)

    # to publish the openCV image has to be 
    # converted back to sensor_msgs/Image 
    try:
        image_edges_ros = cv_bridge.CvBridge().cv2_to_imgmsg(edges_cv, encoding="passthrough")
    except cv_bridge.CvBridgeError:
        print 'fail'

    publish_edge()



def listen_for_images():
    # topic name, checked with cv_camera
    topic_listen = '/cv_camera/image_raw'
    rospy.loginfo('listening to topic ' + topic_listen)


    # start the subscriber
    lis = rospy.Subscriber(topic_listen, Image, callback)

    # keep python from exiting until this node is stopped 
    rospy.spin()


def publish_edge():
    global image_edges_ros
    global pub
    #rate = rospy.Rate(comm_freq) # Hz

    # public 
    pub.publish(image_edges_ros)

if __name__ == '__main__':
    try:
        
        # initialise the node
        node_name ='edge_detector'
        rospy.init_node(node_name, anonymous=True)
        rospy.loginfo('initialising ' + node_name + ' node')


        listen_for_images()

    except rospy.ROSInterruptException:
        pass