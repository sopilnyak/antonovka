from src.model.inference import AppleClassification
import ttach as tta
import time
import warnings
import os
from shutil import copyfile
import tempfile
import cv2
import matplotlib.pyplot as plt
import uuid
import numpy as np

warnings.filterwarnings("ignore")

NUM_WORKERS = 0


def init_model(model_path):
    transforms = tta.Compose(
                [
                    tta.HorizontalFlip(),
                ]
            )
    system = AppleClassification(model_path=model_path,
                                 device='cuda:0',
                                 transforms=None,
                                 th=0.2, gradcam=True)
    return system


def predict(system, filepath):
    folder = tempfile.mkdtemp()
    _, output = tempfile.mkstemp()
    copyfile(filepath, os.path.join(folder, os.path.basename(filepath)))
    image_names = os.listdir(folder)

    labels, _ = system.process_folder(folder + '/', image_names, csv_path=None, num_workers=NUM_WORKERS)

    hm_filename = ''
    if labels[0] == 1:
        image = cv2.imread(filepath)
        hm = system.generate_heatmap(image)
        hm_filename = '{uuid}{extension}'.format(
                uuid=str(uuid.uuid4()),
                extension='.jpg')
        hm_filepath = os.path.join('storage', hm_filename)
        print('wrote heatmap to {}'.format(hm_filepath))
        cv2.imwrite(hm_filepath, np.uint8(255 * hm))
        hm_filename = os.path.basename(hm_filepath)

    if labels[0] == 0:
        return 'false', hm_filename
    return 'true', hm_filename
