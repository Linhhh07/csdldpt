import cv2
import numpy as np

def extract_shape_features(img_bgr):
    """Hu Moments (7D)"""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    moments = cv2.moments(gray)
    hu = cv2.HuMoments(moments).flatten()
    hu = -np.sign(hu) * np.log10(np.abs(hu) + 1e-10)
    return hu  # (7,)