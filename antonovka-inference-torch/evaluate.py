from src.model.inference import AppleClassification
import ttach as tta
import time
import warnings
import os
import numpy as np
import pandas as pd
warnings.filterwarnings("ignore")

# warning! Should ends with '/'
IMAGE_FOLDER = 'data/train_public/'
MODEL_FOLDER = './models/'
OUTPUT_FILE = './Antonovka_out.csv'
NUM_WORKERS = 4

def add_backslash_if_needed(folder):
    if folder[-1] == '/':
        return folder
    return folder + '/'

def process_folder():
    image_folder = add_backslash_if_needed(IMAGE_FOLDER)
    model_folder = add_backslash_if_needed(MODEL_FOLDER)
    image_names = list(os.listdir(image_folder))
    image_names.sort()

    all_thrs = [0.53, 0.4, 0.44, 0.5, 0.65]
    all_transforms = [
        tta.Compose([tta.Rotate90([0, 90])]),
        tta.Compose([tta.Scale([1, 1.25])]),
        tta.Compose([tta.Scale([1, 0.75])]),
        None,
        tta.Compose([tta.Rotate90([0, 90])])
        ]

    all_preds = []
    for ind in range(5):
        system = AppleClassification(model_path=f'{model_folder}fold{ind}.ckpt',
                                     device='cuda:0',
                                     transforms=all_transforms[ind],
                                     th=all_thrs[ind])
        labels, probs = system.process_folder(image_folder, image_names, num_workers=NUM_WORKERS)
        # float, will multiply by weights
        labels = np.array(labels, dtype=float)
        all_preds.append(labels)

    weights = np.array([1, 1, 1, 1, 1], dtype=float)
    weighted_values = weights[0] * all_preds[0]
    for ind in range(1, 5):
        weighted_values += weights[ind] * all_preds[ind]
    weighted_values = weighted_values / np.sum(weights)
    final_preds = (weighted_values > 0.5).astype(int)

    df = pd.DataFrame({'name': image_names,
                       'disease_flag': final_preds})
    df.to_csv(OUTPUT_FILE, index=False)

    return

if __name__ == '__main__':
    start_pred = time.time()

    process_folder()

    end_pred = time.time()
    print('Run time:', end_pred - start_pred, 'seconds')
