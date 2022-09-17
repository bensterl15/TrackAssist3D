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

from Model.constants_and_paths import ROOT_STR

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

logging.basicConfig(level=logging.ERROR)

# n_samples = 21
n_samples = 1

data_dir = "../zarr_creation/"

zarr_name = '3Dtraining.zarr'
zarr_path = os.path.join(data_dir, zarr_name)
print(zarr_path)
log_dir = 'logs'

num_fmaps = 256
input_shape = gp.Coordinate((12, 128, 128))
output_shape = gp.Coordinate((2, 88, 88))

batch_size = 2

voxel_size = gp.Coordinate((1, 1, 1))
input_size = input_shape * voxel_size
output_size = output_shape * voxel_size

checkpoint_every = 200
train_until = 2000
snapshot_every = 200
zarr_snapshot = False

num_workers = 16
cache_size = 100


class CustomLoss(torch.nn.Module):
	def __init__(self, weight=None, size_average=True):
		super(CustomLoss, self).__init__()

	def forward(self, inputs, targets, smooth = 1):
		
		inputs = inputs.view(-1)
		targets = targets.view(-1)

		#intersection = (inputs * targets).sum()
		#dice_loss = 1 - (2.*intersection + smooth)/(inputs.sum() + targets.sum() + smooth)

		BCE = F.binary_cross_entropy(inputs, targets, reduction = 'mean')

		# Compute number of pixels wrongly selected as 0 (accepting null hypothesis)
		#targets_inv = -1*(targets - 1)
		#type2_error = (inputs * targets_inv).sum()

		Total_Loss = BCE# + type2_error/(327680)

		return Total_Loss


def mknet():
	unet = UNet(
		in_channels = 1,
		num_fmaps = num_fmaps,
		fmap_inc_factor = 2,
		downsample_factors = [
			[1, 2, 2],
			[1, 2, 2],
			#[1, 3, 3],
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

def train(iterations):
	with open(ROOT_STR + "DataDirPath.txt", "r") as f:
		data_dir = f.readline()
	f.close()

	zarr_path = os.path.join(data_dir, zarr_name)
	
	model = mknet()
#	loss = CustomLoss() #torch.nn.BCELoss()
	loss = torch.nn.BCELoss()
	optimizer = torch.optim.Adam(lr=5e-5, params=model.parameters())

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
		gp.Normalize(raw, factor = 1.0) +
		gp.Normalize(gt, factor = 1.0)
		for i in range(n_samples)
	)

	pipeline = sources
	pipeline += gp.RandomProvider()

	# add "channel" dimensions
	pipeline += gp.Unsqueeze([raw, gt])
	
	pipeline += gp.Stack(batch_size)

	# pipeline += gp.PreCache(num_workers = num_workers, cache_size = cache_size)

	pipeline += gp.Normalize(gt, factor=1)

	pipeline += Train(
		model,
		loss,
		optimizer,
		inputs={
			'input' : raw
		},
		outputs={
			0: predict,
		},
		loss_inputs={
			0: predict,
			1: gt,
		},
		log_dir = log_dir,
		save_every=20)

	pipeline += gp.Squeeze([raw, gt, predict], axis=1)

	pipeline += gp.Snapshot({gt: 'gt', predict: 'predict', raw: 'raw'}, every = snapshot_every, output_filename = 'batch_{iteration}.hdf', additional_request = snapshot_request)

	with gp.build(pipeline):
		for i in tqdm(range(iterations)):
			pipeline.request_batch(request)

if __name__ == '__main__':
	if 'test' in sys.argv:
		train_until = 10
		snapshot_every = 1
		num_workers = 1

	train_until = 10
	snapshot_every = 1
	num_workers = 1
	
	train(train_until)
