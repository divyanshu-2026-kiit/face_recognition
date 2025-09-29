import os
import cv2
import numpy as np
from pathlib import Path

# Paths for dataset and model
ROOT = Path(__file__).resolve().parents[1]  # go back to "face-recognition-app"
DATASET_DIR = ROOT / 'backend' / 'storage' / 'dataset'
MODEL_DIR = ROOT / 'backend' / 'storage' / 'models'
MODEL_PATH = MODEL_DIR / 'trainer.yml'

def scan_dataset(dataset_dir):
    """
    Reads images from dataset_dir, assigns labels and returns:
    - list of images
    - numpy array of labels
    - mapping name->label
    """
    if not dataset_dir.exists():
        raise SystemExit(f"Dataset directory not found: {dataset_dir}")

    names = sorted([d.name for d in dataset_dir.iterdir() if d.is_dir()])
    name_to_label = {name: idx for idx, name in enumerate(names)}

    images = []
    labels = []

    for name in names:
        person_dir = dataset_dir / name
        for img_file in person_dir.glob("*.jpg"):
            img = cv2.imread(str(img_file), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
                labels.append(name_to_label[name])

    return images, np.array(labels), name_to_label

if __name__ == "__main__":
    images, labels, mapping = scan_dataset(DATASET_DIR)
    if len(images) == 0:
        raise SystemExit("No images found. Make sure samples are captured.")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=2,
        neighbors=8,
        grid_x=8,
        grid_y=8
    )
    recognizer.train(images, labels)
    recognizer.save(str(MODEL_PATH))

    # Also save label mapping
    labels_file = MODEL_PATH.with_suffix('.labels')
    with open(labels_file, 'w', encoding='utf-8') as f:
        for name, idx in mapping.items():
            f.write(f"{idx},{name}\n")

    print("TRAIN_OK")
