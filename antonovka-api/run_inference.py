from src.model.inference import AppleClassification
import ttach as tta
import time
import warnings
import os
from shutil import copyfile
import tempfile

warnings.filterwarnings("ignore")

NUM_WORKERS = 4


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

    labels, _ = system.process_folder(folder, csv_path=output, num_workers=NUM_WORKERS)
    if labels[0] == 0:
        return 'false'
    return 'true'
