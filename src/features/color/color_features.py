import cv2
import numpy as np

def extract_color_features(img_bgr):
    """HSV Histogram (128D) + Color Moments (9D) = 137D"""
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    h = cv2.calcHist([hsv], [0], None, [64], [0,180]).flatten()
    s = cv2.calcHist([hsv], [1], None, [32], [0,256]).flatten()
    v = cv2.calcHist([hsv], [2], None, [32], [0,256]).flatten()
    hist = np.concatenate([h, s, v])
    hist = hist / (hist.sum() + 1e-7)

    moments = []
    for c in range(3):
        ch = hsv[:, :, c].astype(np.float32)
        mean = np.mean(ch)
        std  = np.std(ch)
        skew = np.mean(((ch - mean) / (std + 1e-7)) ** 3)
        moments.extend([mean, std, skew])

    return np.concatenate([hist, np.array(moments)])  # (137,)