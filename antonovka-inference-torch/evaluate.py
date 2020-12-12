from src.model.inference import AppleClassification
import ttach as tta
import warnings

warnings.filterwarnings("ignore")


IMAGE_FOLDER = 'data/train_public/'
MODEL_PATH = 'models/fold_0.ckpt'

def process_folder():
    transforms = tta.Compose(
                [
                    tta.HorizontalFlip(),
                ]
            )
    system = AppleClassification(model_path=MODEL_PATH,
                                 device='cuda:0',
                                 transforms=transforms)
    _ = system.process_folder(IMAGE_FOLDER, csv_path='Antonovka_out.csv')
    return


if __name__ == '__main__':
    process_folder()
