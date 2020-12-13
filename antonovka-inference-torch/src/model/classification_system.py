from argparse import Namespace
from pytorch_lightning import LightningModule
from src.model.models import se_resnext50_32x4d


class QualityDescriptor(LightningModule):
    def __init__(self, hparams):
        super(QualityDescriptor, self).__init__()
        if type(hparams) == dict:
            hparams = Namespace(**hparams)
        self.hparams = hparams
        model = se_resnext50_32x4d()
        self.model = model

    def on_load_checkpoint(self, checkpoint):
        self._transofrms = None
        if 'transforms' in checkpoint.keys():
            self._transofrms = checkpoint['transforms']

    def forward(self, x):
        return self.model(x)