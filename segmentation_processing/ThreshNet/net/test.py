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

num_epochs = 100
width = 256
batch_size = 1
learning_rate = 1e-3

img_transform = transforms.Compose([
	transforms.ToTensor()
])

raw_container = np.load('raw_test.npy')
gt_container = np.load('gt_test.npy')

thresholds_vector = np.load('thresholds.npy')

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
	model = model.float()
	model.load_state_dict(torch.load('./autoencoder.pth'))
	model.eval()
else:
	model = autoencoder()
	model = nn.DataParallel(model)
	model = model.float()
	model.load_state_dict(torch.load('./autoencoder.pth'))
	model.eval()

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)

N = np.shape(raw_container)[0]
for i in range(30):
	raw = torch.from_numpy(np.reshape(raw_container[i], (1, 1, 256, 256))).float()
	thresh = torch.from_numpy(np.array(thresholds_vector[i] )).float()
	if torch.cuda.is_available():
		raw = Variable(raw).cuda()
		thresh = Variable(thresh).cuda()
	else:    
		raw = Variable(raw)
		thresh = Variable(thresh)

	# ===================forward=====================
	output = model(raw.float())
	loss = criterion(output.float(), thresh.float())
	print(f'loss : {loss.data}')


	out = raw.detach().numpy()
	thresh = output.detach().numpy()
	out = np.reshape(out, (256, 256))
	out[out < thresh] = 0
	print(out.shape)

	out = 255 * out / np.max(out)
	out = out.astype(np.uint8)

	outimg = Image.fromarray(out)
	outimg.save(f'im{i}.png')

#torch.save(model.state_dict(), './autoencoder.pth')
