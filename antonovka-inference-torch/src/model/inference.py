import os
import torch
from tqdm import tqdm
import numpy as np
import pandas as pd
import ttach as tta
from src.model.classification_system import QualityDescriptor
from src.data.transforms import noramilize, resize
from src.data.dataset import Apples
from torch.utils.data import DataLoader


class AppleClassification:
    def __init__(self,
                 model_path,
                 transforms=None,
                 th=0.5,
                 device='cpu'):
        self.device = torch.device(device)
        classifier = QualityDescriptor.load_from_checkpoint(model_path)
        classifier.model = torch.nn.Sequential(classifier.model, torch.nn.Sigmoid())
        classifier.freeze()
        self.mean = classifier.hparams['dataset']['mean']
        self.std = classifier.hparams['dataset']['std']
        self.size = classifier.hparams['dataset']['size']
        if transforms:
            classifier = tta.ClassificationTTAWrapper(classifier, transforms, merge_mode='mean')
        self.classifier = classifier.to(self.device)
        self.th = th

    def process_image(self, img):
        img = noramilize(img=img,
                         mean=self.mean,
                         std=self.std)
        img = resize(img, self.size)
        img = np.moveaxis(np.array(img), 2, 0)
        img = torch.tensor(img, device=self.device).unsqueeze(0)
        pred = self.classifier(img).flatten().detach().cpu().item()
        label = 0 if pred < self.th else 1
        return label, pred

    def process_folder(self, folder, image_names, csv_path=None, num_workers=8, batch_size=4):
        ds = Apples(names=image_names,
                    image_dir=folder,
                    mean=self.mean,
                    std=self.mean,
                    size=self.size)
        loader = DataLoader(dataset=ds,
                            num_workers=num_workers,
                            batch_size=batch_size)
        predictions = []
        with torch.no_grad():
            for batch in tqdm(loader):
                batch = batch.to(self.device).float()
                bpreds = self.classifier(batch)
                bpreds = bpreds.flatten().detach().cpu().tolist()
                predictions.extend(bpreds)
        labels = np.copy(predictions)
        labels[labels < self.th] = 0
        labels[labels > self.th] = 1
        labels = labels.astype(int)

        if csv_path:
            df = pd.DataFrame({'name': ds.names,
                               'disease_flag': labels,
                               'prob': predictions})
            df.to_csv(csv_path, index=0)

        return labels, predictions
