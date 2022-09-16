from funlib.learn.torch.models import UNet, ConvPass
from gunpowder.torch import Train
import gunpowder as gp
import math
import numpy as np
import logging
import os
import sys
from tqdm import tqdm
from PIL import Image
from skimage import filters
# import matplotlib.pyplot as plt
import zarr
import torch
import torch.nn as nn
import torch.nn.functional as F

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

logging.basicConfig(level=logging.ERROR)

# n_samples = 21
n_samples = 1

data_dir = "./output/"

zarr_name = '3Dtraining.zarr'
zarr_path = os.path.join(data_dir, zarr_name)
print(zarr_path)
log_dir = 'logs'



class CustomLoss(torch.nn.Module):
    def __init__(self, weight=None, size_average=True):
        super(CustomLoss, self).__init__()

    def forward(self, inputs, targets, smooth=1):
        inputs = inputs.view(-1)
        targets = targets.view(-1)
        BCE = F.binary_cross_entropy(inputs, targets, reduction='mean')
        return BCE


def mknet(pdict):
    num_fmaps = pdict['num_fmaps']
    fmap_inc_factor = pdict['fmap_inc_factor']
    downsample_factors = pdict['downsample_factors']
    kernel_size_down = pdict['kernel_size_down']
    kernel_size_up = pdict['kernel_size_up']
    in_channels = pdict['in_channels']
    unet = UNet(
        in_channels=in_channels,
        num_fmaps=num_fmaps,
        fmap_inc_factor=fmap_inc_factor,
        downsample_factors=downsample_factors,
        kernel_size_down=kernel_size_down,
        kernel_size_up=kernel_size_up,
    )

    conv_in_channels = pdict['conv_in_channels']
    conv_kernel = pdict['conv_kernel']
    unet = nn.DataParallel(unet)
    convpass = ConvPass(num_fmaps, in_channels, conv_kernel, activation='Sigmoid')
    convpass = nn.DataParallel(convpass)

    model = torch.nn.Sequential(
        unet,
        convpass,
    )
    return (model)


def train(pdict):
    batch_size = pdict['batch_size']
    snapshot_every = pdict['snapshot_every']
    voxel_size = gp.Coordinate(pdict['voxel_size'])
    input_shape = gp.Coordinate(pdict['input_shape'])
    output_shape = gp.Coordinate(pdict['output_shape'])

    input_size = input_shape * voxel_size
    output_size = output_shape * voxel_size

    iterations = pdict['train_until']
    learning_rate = pdict['learning_rate']
    model = mknet(pdict)
    loss = torch.nn.BCELoss()
    optimizer = torch.optim.Adam(lr=learning_rate, params=model.parameters())

    raw = gp.ArrayKey('raw')
    gt = gp.ArrayKey('gt')
    predict = gp.ArrayKey('predict')

    request = gp.BatchRequest()
    request.add(raw, input_size)
    request.add(gt, output_size)

    snapshot_request = gp.BatchRequest()
    snapshot_request[predict] = request[gt].copy()

    sources = tuple(
        gp.ZarrSource(
            zarr_path,
            {
                raw: f'raw/{i}',
                gt: f'gt/{i}',
            },
            {
                raw: gp.ArraySpec(interpolatable=True, voxel_size=voxel_size),
                gt: gp.ArraySpec(interpolatable=False, voxel_size=voxel_size),
            }) +
        gp.RandomLocation() +
        gp.Normalize(raw, factor=1.0) +
        gp.Normalize(gt, factor=1.0)
        for i in range(n_samples)
    )

    pipeline = sources
    pipeline += gp.RandomProvider()

    # add "channel" dimensions
    pipeline += gp.Unsqueeze([raw, gt])

    pipeline += gp.Stack(batch_size)

    pipeline += gp.Normalize(gt, factor=1)

    pipeline += Train(
        model,
        loss,
        optimizer,
        inputs={
            'input': raw
        },
        outputs={
            0: predict,
        },
        loss_inputs={
            0: predict,
            1: gt,
        },
        log_dir=log_dir,
        save_every=20)

    pipeline += gp.Squeeze([raw, gt, predict], axis=1)

    pipeline += gp.Snapshot({gt: 'gt', predict: 'predict', raw: 'raw'}, every=snapshot_every,
                            output_filename='batch_{iteration}.hdf', additional_request=snapshot_request)

    with gp.build(pipeline):
        for i in tqdm(range(iterations)):
            pipeline.request_batch(request)

'''
if __name__ == '__main__':
    if 'test' in sys.argv:
        train_until = 10
        snapshot_every = 1

    train_until = 5
    snapshot_every = 1
    train(train_until)
'''