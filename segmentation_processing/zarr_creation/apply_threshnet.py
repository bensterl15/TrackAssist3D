__author__ = 'Ben Sterling'

import os

import torch
import torchvision
from torch import nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torchvision.utils import save_image

from PIL import Image
import numpy as np

img_transform = transforms.Compose([
	transforms.ToTensor()
])

class autoencoder(nn.Module):
	def __init__(self):
		super(autoencoder, self).__init__()
		self.encoder = nn.Sequential(
			nn.Flatten(start_dim=0),

			nn.Linear(256*256, 64*64),
			nn.LeakyReLU(0.02, True),

			nn.Linear(64*64, 32*32),
			nn.LeakyReLU(0.02, True),

			nn.Linear(32*32, 1),
			nn.LeakyReLU(0.02, True),
		)

	def forward(self, x):
		x = self.encoder(x)
		x = F.leaky_relu(x, negative_slope = 0.01)
		return x

if torch.cuda.is_available():
	model = autoencoder().cuda()
	model = nn.DataParallel(model)
	model = model.float()
	model.load_state_dict(torch.load('./autoencoder.pth'))
	model.eval()
else:
	model = autoencoder()
	model = nn.DataParallel(model)
	model = model.float()
	model.load_state_dict(torch.load('./autoencoder.pth'))
	model.eval()

def process_array(arr, model):
	raw = torch.from_numpy(np.reshape(arr, (1, 1, 256, 256))).float()
	if torch.cuda.is_available():
		raw = Variable(raw).cuda()
	else:
		raw = Variable(raw)

	# ===================forward=====================
	output = model(raw.float())

	out = raw.detach().numpy()
	thresh = output.detach().numpy()
	out = np.reshape(out, (256, 256))
	out[out < thresh] = 0
	return out

# Hard code the dimensions for now:
for i in range(21):
	for j in range(14):
		raw = np.load(f'3Dtraining/raw/{i}/{j}.npy')
		gt = np.load(f'3Dtraining/gt/{i}/{j}.npy')

		raw = process_array(raw, model)
		gt = process_array(gt, model)

		np.save(f'3Dtraining/raw/{i}/{j}.npy', raw)
		np.save(f'3Dtraining/gt/{i}/{j}.npy', gt)

	# Note that layers [0,9]U[51,60] are blanks
	for j in range(10, 51):
		raw = np.load(f'3Dexpanded/raw/{i}/{j}.npy')
		raw = process_array(raw, model)
		np.save(f'3Dexpanded/raw/{i}/{j}.npy', raw)
