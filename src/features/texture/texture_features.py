import cv2
import numpy as np
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops

def extract_texture_features(img_bgr):
    """LBP (256D) + GLCM (4D) = 260D"""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    lbp = local_binary_pattern(gray, P=8, R=1, method='uniform')
    hist_lbp, _ = np.histogram(lbp.ravel(), bins=256, range=(0,256))
    hist_lbp = hist_lbp.astype(float) / (hist_lbp.sum() + 1e-7)

    glcm = graycomatrix(gray, distances=[1], angles=[0],
                        levels=256, symmetric=True, normed=True)
    glcm_feat = np.array([
        graycoprops(glcm, 'contrast')[0, 0],
        graycoprops(glcm, 'dissimilarity')[0, 0],
        graycoprops(glcm, 'homogeneity')[0, 0],
        graycoprops(glcm, 'energy')[0, 0]
    ])

    return np.concatenate([hist_lbp, glcm_feat])  # (260,)