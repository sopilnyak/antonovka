from src.model.inference import AppleClassification
import ttach as tta
import time
import warnings
import os
from shutil import copyfile
import tempfile
import cv2

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
                                 transforms=transforms,
                                 th=0.2)
    return system


def predict(system, filepath):
    folder = tempfile.mkdtemp()
    _, output = tempfile.mkstemp()
    copyfile(filepath, os.path.join(folder, os.path.basename(filepath)))

    labels, _ = system.process_folder(folder + '/', csv_path=None, num_workers=NUM_WORKERS)

    hm_filename = ''
    if labels[0] == 1:
        image = cv2.imread(filepath)
        system.generate_heatmap(image)
        hm_filepath = filepath.split('.')[0] + '_hm' + filepath.split('.')[1]
        print('wrote heatmap to {}'.format(hm_filepath))
        cv2.imwrite(hm_filepath, image)
        hm_filename = os.path.basename(hm_filepath)

    if labels[0] == 0:
        return 'false', hm_filename
    return 'true', hm_filename
