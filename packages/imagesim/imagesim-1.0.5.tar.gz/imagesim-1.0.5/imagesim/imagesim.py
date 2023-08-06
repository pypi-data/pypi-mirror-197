"""
:authors: PavukEdya, Sou1Guard
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2023 PavukEdya, Sou1Guard
"""

import os
from skimage.metrics import structural_similarity
import numpy as np
import cv2


class ImagesDifferences:

    def __init__(self):
        self.median_frame = None
        self.test = None

    def get_median_frame(self, video_name):
        cap = cv2.VideoCapture(video_name)
        frame_ids = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=40)
        frames = []
        for fid in frame_ids:
            cap.set(cv2.CAP_PROP_POS_FRAMES, fid)
            ret, frame = cap.read()
            frames.append(frame)
        self.median_frame = np.median(frames, axis=0).astype(dtype=np.uint8)

    def check_differences(self, image1, image2, accuracy=0.85):
        gray_image1 = cv2.imread(image1, cv2.IMREAD_GRAYSCALE)
        gray_image2 = cv2.imread(image2, cv2.IMREAD_GRAYSCALE)
        (score, diff) = structural_similarity(gray_image1, gray_image2, full=True)
        return True if score < accuracy else False
