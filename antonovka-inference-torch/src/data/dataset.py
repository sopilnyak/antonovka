import torch.utils.data as data
import numpy as np
import torch
import cv2
import os
from .transforms import resize, noramilize


class Apples(data.Dataset):
    def __init__(self,
                 names,
                 image_dir,
                 mean=None,
                 std=None,
                 size=(512, 512)):
        super(Apples, self).__init__()

        if mean is None:
            mean = [0.485, 0.456, 0.406]
        if std is None:
            std = [0.229, 0.224, 0.225]
        self.names = names
        self.image_dir = image_dir
        self.size = size
        self.mean = mean
        self.std = std

    def __getitem__(self, index):
        name = self.names[index]
        img = cv2.imread(self.image_dir + name)
        img = noramilize(img, self.mean, self.std)
        img = resize(img, self.size)
        img = np.moveaxis(np.array(img), 2, 0)
        return torch.tensor(img, dtype=torch.float)

    def __len__(self):
        return int(len(self.names))


def predict_from_folder(folder):
    images = os.listdir(folder)
    ds = Apples(images, folder)