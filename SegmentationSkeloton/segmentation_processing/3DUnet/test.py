from funlib.learn.torch.models import UNet, ConvPass
from gunpowder.torch import Predict
import gunpowder as gp
import math
import numpy as np
from tifffile import imsave
import nibabel as nib
import torch
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


logging.basicConfig(level=logging.ERROR)

# n_samples = 21
n_samples = 1

data_dir = "../zarr_creation/"

zarr_name = '3Dexpanded.zarr'
zarr_path = os.path.join(data_dir, zarr_name)
print(zarr_path)
log_dir = 'logs'

full_shape = gp.Coordinate((60, 256, 256))

num_fmaps = 256
input_shape = gp.Coordinate((12, 128, 128))
output_shape = gp.Coordinate((2, 88, 88))

batch_size = 8

voxel_size = gp.Coordinate((1, 1, 1))
input_size = input_shape * voxel_size
output_size = output_shape * voxel_size

checkpoint_every = 1
train_until = 5
snapshot_every = 1
zarr_snapshot = False
num_workers = 16

strs = os.listdir('.')
strs = [int(x[17:]) for x in strs if "model_checkpoint_" in x]
strs.sort()
highest_model = strs[-1]
# Does not work unless it is multiple of 100 for some reason..
highest_model = highest_model - (highest_model % 100)
highest_model = str(highest_model)
print(f'highest model: {highest_model}')

CURRENT_IMAGE = 0

'''
class WeightedMSELoss(torch.nn.MSELoss):
	def __init__(self):
		super(WeightedMSELoss, self).__init__()

	def forward(self, prediction, gt, weights):
		loss = super(WeightedMSELoss, self).forward(prediction*weights, gt*weights)
		return loss

'''

def mknet():
    unet = UNet(
    in_channels = 1,
    num_fmaps = num_fmaps,
    fmap_inc_factor = 2,
    downsample_factors = [
        [1, 2, 2],
        [1, 2, 2],
        #[1, 3, 3]
    ],
        kernel_size_down = [[[2, 3, 3], [2, 3, 3]]]*3,
        kernel_size_up   = [[[2, 3, 3], [2, 3, 3]]]*2,
    )

    unet = nn.DataParallel(unet)
    convpass = ConvPass(num_fmaps, 1, [[1, 1, 1]], activation='Sigmoid')
    convpass = nn.DataParallel(convpass)

    model = torch.nn.Sequential(
        unet,
        convpass,
    )
    return(model)

def test():
    with open("..\\..\\..\\DataDirPath.txt", "r") as f:
        data_dir = f.readline()
    f.close()

    zarr_path = os.path.join(data_dir, zarr_name)

    #for im_index in range(n_samples):
    im_index = CURRENT_IMAGE
    model = mknet()
    model.load_state_dict(torch.load('model_checkpoint_' + highest_model)['model_state_dict'])
    model.eval()

    raw = gp.ArrayKey('raw')
    predict = gp.ArrayKey('predict')
        
    request = gp.BatchRequest()
    request.add(raw, full_shape)
    request.add(predict, full_shape)

    source = gp.ZarrSource(
        zarr_path,
        {
            raw: f'raw/{im_index}',
        },
        {
            raw: gp.ArraySpec(interpolatable=True, voxel_size=voxel_size),
        })

    pipeline = source
    pipeline += gp.Normalize(raw, factor = 1.0)

    # add "channel" dimensions
    pipeline += gp.Unsqueeze([raw])
        
    # Add "batch" dimensions, which is just 1 in this case:
    pipeline += gp.Unsqueeze([raw])

    pipeline += Predict(
        model,
        inputs={
            'input' : raw
        },
        outputs={
            0: predict,
        })

    scan_request = gp.BatchRequest()
    scan_request.add(raw, input_size)
    scan_request.add(predict, output_size)
    pipeline += gp.Scan(scan_request)
	
    pipeline += gp.Squeeze([raw, predict], axis=1)

    with gp.build(pipeline):
        batch = pipeline.request_batch(request)
		
    output = batch[predict].data
    print(type(output))
    print(output.shape)
    np.save('output_' + str(im_index) + '.npy', output)

if __name__ == '__main__':

    '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, required=True)
    args = parser.parse_args()
    CURRENT_IMAGE = args.image
    print(f'CURRENT_IMAGE: {CURRENT_IMAGE}')
    '''
	
    for i in range(n_samples):
        i = CURRENT_IMAGE
        test()
        f_name = 'output_' + str(i)
	
        output = np.load(f_name + '.npy')
        output = np.squeeze(output)
        #output[output >= 0.5] = 1
        #output[output < 0.5] = 0
        
        imsave(f_name + '.tif', output)
        img = nib.Nifti1Image(output, affine=np.eye(4))
        nib.save(img, f_name + '.nii')