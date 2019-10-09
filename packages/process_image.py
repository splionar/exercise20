import rosbag
#import os
import cv2
import numpy as np
from cv_bridge import CvBridge
import sys

processed_bag = rosbag.Bag('mounted_volume/amod19-rh3-ex-process-stefan.bag', 'w')
bag = rosbag.Bag(sys.argv[1])

br = CvBridge()
font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (20,460)
fontScale = 1
fontColor = (255,255,255)
lineType = 2

for topic, msg, t in bag.read_messages(topics=['/duckiemon/camera_node/image/compressed']):
    np_arr = np.fromstring(msg.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    cv2.putText(image_np,str(t), 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    lineType)
    #cv2.imwrite("testpic.png", image_np)

    compressed_img_msg = br.cv2_to_compressed_imgmsg(image_np, dst_format='jpg')
    processed_bag.write('/duckiemon/camera_node/image/compressed', compressed_img_msg, t)

bag.close()
processed_bag.close()