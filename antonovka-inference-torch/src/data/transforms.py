from albumentations import (
    CLAHE, RandomRotate90,
    Transpose, ShiftScaleRotate, Blur,
    IAAAdditiveGaussianNoise, GaussNoise, MotionBlur, MedianBlur, RandomBrightnessContrast,
    IAASharpen, IAAEmboss, Flip, OneOf, Compose, Resize, Normalize, BboxParams,
)


def strong_aug(p=1):
    return Compose([
        Flip(p=p),
        OneOf([
            IAASharpen(alpha=(0.1, 0.3), lightness=(0.1, 0.3), p=1),
            IAAEmboss(p=1),
            CLAHE(clip_limit=2, p=1)], p=p),
        OneOf([
            Blur(blur_limit=(1, 3), p=1),
            GaussNoise(var_limit=(10, 30), p=1)], p=p),
        ShiftScaleRotate(shift_limit=0.01, scale_limit=(-0.1, 0.5), rotate_limit=90, p=p),
        RandomBrightnessContrast(brightness_limit=(-0.01, 0.05), contrast_limit=(-0.01, 0.01), p=p),
    ], p=1)


def light_aug(p=1.0):
    return Compose([
        Flip(p=1),
        ShiftScaleRotate(shift_limit=0.01, scale_limit=(-0.1, 0.5), rotate_limit=90, p=1),
        RandomBrightnessContrast(brightness_limit=(-0.01, 0.05), contrast_limit=(-0.01, 0.01), p=p),
    ], p=p)


def light_aug_detection(p=1.0):
    return Compose([
        Flip(p=1),
        Transpose(p=0.8),
        ShiftScaleRotate(shift_limit=0.01, scale_limit=0.01, rotate_limit=30, p=1),
        RandomBrightnessContrast(brightness_limit=(-0.01, 0.01), contrast_limit=(-0.01, 0.01), p=p),
    ],
        bbox_params=BboxParams(format='pascal_voc', label_fields=['category_ids']),
        p=p)


def resize(img, size):
    res = Resize(size[0], size[1])
    scope = res(image=img)
    img = scope['image']
    return img


def augment(img, aug_type, p=1):
    if aug_type == 'light':
        aug = light_aug(p=p)
    elif aug_type == 'strong':
        aug = strong_aug(p=p)
    scope = aug(image=img)
    img = scope['image']
    return img


def noramilize(img, mean=0, std=0):
    norm = Normalize(mean=mean, std=std, p=1)
    scope = norm(image=img)
    img = scope['image']
    return img


def augment_detection(img, boxes, p=1):
    category_ids = [1] * len(boxes)
    aug = light_aug_detection(p=p)
    scope = aug(image=img,
                bboxes=boxes,
                category_ids=category_ids)
    return scope['image'], scope['bboxes']
