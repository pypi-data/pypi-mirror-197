import cv2
import numpy as np
import os

import numpy as np
import pandas as pd
from PIL import Image

from vis.run import run
from vis.user_classes import *

# # define directory path
data_dir = '/Users/amitosi/PycharmProjects/chester/chester/data/videos/mixkit-people-dancing-at-a-night-club-4344-medium.mp4'
# Create a video capture object
cap = cv2.VideoCapture(data_dir)

# Define image size
image_shape = (3, 1024, 1024)

vis_collector = run(video=cap,
                    frame_per_second=5, image_shape=image_shape, plot_sample=16,
                    get_grayscale=True, get_reveresed_video=True,
                    get_zoomed_video=True, zoom_factor=1.2, zoom_center=(700, 700),
                    get_frames_description=False, detect_frame_objects=False, detect_faces=False, plot=True)
