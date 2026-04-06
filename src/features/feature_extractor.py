import os
import cv2
import numpy as np
from PIL import Image
import pandas as pd
from tqdm import tqdm

from color.color_features     import extract_color_features
from texture.texture_features import extract_texture_features
from shape.shape_features     import extract_shape_features
from deep.deep_features       import load_resnet50, extract_deep_features

PROCESSED_DIR = "dataset/processed"
OUTPUT_DIR    = "vectors"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_all(image_path, model, transform):
    img_pil = Image.open(image_path).convert("RGB")
    img_bgr = cv2.imread(image_path)

    vector = np.concatenate([
        extract_deep_features(img_pil, model, transform),
        extract_color_features(img_bgr),
        extract_texture_features(img_bgr),
        extract_shape_features(img_bgr),
    ])
    norm = np.linalg.norm(vector)
    return vector / (norm + 1e-7)

if __name__ == "__main__":
    model, transform = load_resnet50()
    all_features, all_filenames, all_categories = [], [], []

    for category in sorted(os.listdir(PROCESSED_DIR)):
        cat_dir = os.path.join(PROCESSED_DIR, category)
        if not os.path.isdir(cat_dir):
            continue
        files = [f for f in os.listdir(cat_dir)
                 if f.lower().endswith(('.jpg','.jpeg','.png'))]
        print(f"Xu ly: {category} ({len(files)} anh)")
        for file in tqdm(files, desc=f"  {category}"):
            try:
                feat = extract_all(os.path.join(cat_dir, file), model, transform)
                all_features.append(feat)
                all_filenames.append(file)
                all_categories.append(category)
            except Exception as e:
                print(f"  Loi {file}: {e}")

    features_array = np.array(all_features)
    np.save(os.path.join(OUTPUT_DIR, "deep_vectors_resnet50.npy"), features_array)
    pd.DataFrame({"filename": all_filenames, "category": all_categories})\
      .to_csv(os.path.join(OUTPUT_DIR, "vectors_index.csv"), index=False)

    print(f"\n Shape: {features_array.shape}")