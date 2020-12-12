from src.model.inference import AppleClassification
import ttach as tta
import time
import warnings

warnings.filterwarnings("ignore")

IMAGE_FOLDER = 'data/train_public/'
MODEL_PATH = './models/fold0.ckpt'
OUTPUT_FILE = './Antonovka_out.csv'
NUM_WORKERS = 4

def process_folder():
    transforms = tta.Compose(
                [
                    tta.HorizontalFlip(),
                ]
            )
    system = AppleClassification(model_path=MODEL_PATH,
                                 device='cuda:0',
                                 transforms=transforms,
                                 th=0.2)
    _ = system.process_folder(IMAGE_FOLDER, csv_path=OUTPUT_FILE, num_workers=NUM_WORKERS)
    return

if __name__ == '__main__':
    start_pred = time.time()

    process_folder()

    end_pred = time.time()
    print('Run time:', end_pred - start_pred, 'seconds')
