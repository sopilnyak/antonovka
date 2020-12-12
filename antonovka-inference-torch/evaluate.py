from src.model.inference import AppleClassification
import ttach as tta
import warnings

warnings.filterwarnings("ignore")


FOLDER = '/mnt/QUANTGEN/SRCDATA/DL/apples/agrohack/train_public/'


def process_folder():
    transforms = tta.Compose(
                [
                    tta.HorizontalFlip(),
                ]
            )
    system = AppleClassification(model_path='/mnt/QUANTGEN/SRCDATA/DL/apples/checkpoints/apples/fold_0.ckpt',
                                 device='cuda:0',
                                 transforms=transforms)
    _ = system.process_folder(FOLDER, csv_path='Antonovka_out.csv')
    return


if __name__ == '__main__':
    process_folder()
