
import os
import cv2
import numpy as np
from PIL import Image, ImageOps
from tqdm import tqdm
import pandas as pd
import imagehash

RAW_DIR = "dataset/raw"
PROCESSED_DIR = "dataset/processed"
METADATA_DIR = "dataset/metadata"

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

# Cau hinh nguong
LAPLACIAN_MIN  = 42
BRIGHTNESS_MIN = 28
BLANK_MEAN_MIN = 245
BLANK_STD_MAX  = 8

SOURCE_MAP = {
    "tu_lanh":    "Kaggle",
    "tu_quan_ao": "Kaggle",
    "giay": "Kaggle",
    # "dien_thoai": "ImageNet",
}

def is_blank_image(gray):
    return np.mean(gray) > BLANK_MEAN_MIN and np.std(gray) < BLANK_STD_MAX

metadata          = []
total_saved       = 0
duplicate_count   = 0
bad_quality_count = 0
hash_set          = set()
reject_log        = []

print("=== CHUAN HOA  ===\n")

for folder in sorted(os.listdir(RAW_DIR)):
    folder_path = os.path.join(RAW_DIR, folder)
    if not os.path.isdir(folder_path):
        continue

    save_dir = os.path.join(PROCESSED_DIR, folder)
    os.makedirs(save_dir, exist_ok=True)

    count = 0
    files = [f for f in os.listdir(folder_path)
             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

    print(f"Dang xu ly: {folder} ({len(files)} anh)")

    for file in tqdm(files, desc=f"   {folder}"):
        src_path = os.path.join(folder_path, file)

        try:
            img = Image.open(src_path).convert("RGB")
            img_cv = cv2.imread(src_path)
            if img_cv is None:
                continue

            # 1. Loai trung het
            current_hash = imagehash.phash(img)
            if current_hash in hash_set:
                duplicate_count += 1
                continue
            hash_set.add(current_hash)

            # 2. Kiem tra chat luong
            gray            = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            lap_var         = cv2.Laplacian(gray, cv2.CV_64F).var()
            mean_brightness = np.mean(gray)

            bad_reason = None
            if lap_var < LAPLACIAN_MIN:
                bad_reason = "blur"
            elif mean_brightness < BRIGHTNESS_MIN:
                bad_reason = "dark"
            elif is_blank_image(gray):
                bad_reason = "blank"

            if bad_reason:
                bad_quality_count += 1
                reject_log.append({
                    "folder":     folder,
                    "file":       file,
                    "reason":     bad_reason,
                    "lap_var":    round(lap_var, 2),
                    "brightness": round(mean_brightness, 2)
                })
                continue

            # 3. Crop vat chinh
            orig_h, orig_w = img_cv.shape[:2]
            _, thresh = cv2.threshold(gray, 22, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)

            if not contours:
                pass  # fallback: khong crop, giu nguyen anh goc
            else:
                largest    = max(contours, key=cv2.contourArea)
                area_ratio = cv2.contourArea(largest) / (orig_h * orig_w)

                if 0.045 < area_ratio < 0.90:
                    x, y, w, h = cv2.boundingRect(largest)
                    if w >= 50 and h >= 50:
                        padding = int(0.07 * min(w, h))
                        x = max(0, x - padding)
                        y = max(0, y - padding)
                        w = min(orig_w - x, w + padding * 2)
                        h = min(orig_h - y, h + padding * 2)
                        img = img.crop((x, y, x + w, y + h))

            # 4. Chuan hoa 224x224
            final_img = ImageOps.pad(img, (224, 224),
                                     color="white", method=Image.LANCZOS)

            new_filename = f"{folder}_{count:04d}.jpg"
            final_path   = os.path.join(save_dir, new_filename)
            final_img.save(final_path, "JPEG", quality=95, optimize=True)

            source = SOURCE_MAP.get(folder, "ImageNet")
            metadata.append({
                "filename": new_filename,
                "category": folder,
                "source":   source
            })

            count       += 1
            total_saved += 1

        except Exception as e:
            print(f"\n   Loi file {file}: {e}")
            continue

    print(f"   -> Da luu {count} anh\n")

# Luu metadata
df = pd.DataFrame(metadata)
df.to_csv(os.path.join(METADATA_DIR, "categories.csv"), index=False)

# Luu reject log
if reject_log:
    df_reject = pd.DataFrame(reject_log)
    df_reject.to_csv(os.path.join(METADATA_DIR, "reject_log.csv"), index=False)

    print("\n=== THONG KE LY DO LOAI ANH ===")
    for reason, grp in df_reject.groupby("reason"):
        print(f"  {reason:8s}: {len(grp)} anh")

print("\n=== HOAN THANH ===")
print(f"Tong anh da luu     : {total_saved}")
print(f"Anh trung lap       : {duplicate_count}")
print(f"Anh kem chat luong  : {bad_quality_count}")

print("\n=== THONG KE TUNG CATEGORY ===")
for cat, grp in df.groupby("category"):
    status = "[DU]" if len(grp) >= 10 else "[IT ANH]"
    print(f"  {status}  {cat}: {len(grp)} anh")