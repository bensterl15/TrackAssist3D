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

import numpy as np
from time import time

num_epochs = 20
width = 256
batch_size = 1
learning_rate = 1e-6

img_transform = transforms.Compose([
	transforms.ToTensor()
])

#raw_path = './ThreshTrain/raw/'
#gt_path = './ThreshTrain/gt/'

raw_container = np.load('raw_train.npy')
gt_container = np.load('gt_train.npy')

thresholds_vector = np.load('thresholds.npy')

N = np.shape(raw_container)[0]

class autoencoder(nn.Module):
	def __init__(self):
		super(autoencoder, self).__init__()
		self.encoder = nn.Sequential(
			#nn.Conv2d(1, 1, 129),
			#nn.Softplus(),
			#nn.MaxPool2d(2),

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
		#print(f'x shape: {x.shape}, input shape:{input.shape}')
		print(f'threshold : {x}', flush = True)
		#x = input - x
		x = F.leaky_relu(x, negative_slope=0.01)
		#print(f'threshold : {torch.mean(x)}', flush=True)
		return x

if torch.cuda.is_available():
	model = autoencoder().cuda()
else:
	model = autoencoder()

model = nn.DataParallel(model)
model = model.float()

# Comment in and out as applicable: (Loads previous model)
#model.load_state_dict(torch.load('./autoencoder.pth'))

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(
	model.parameters(), lr=learning_rate)

#total_loss = 0
for epoch in range(num_epochs):
	for i in range(N):
		optimizer.zero_grad()
		start = time()
		raw = torch.from_numpy(np.reshape(raw_container[i], (1, 1, 256, 256))).float()
		thresh = torch.from_numpy(np.array( thresholds_vector[i] )).float()
		if torch.cuda.is_available():
			raw = Variable(raw).cuda()
			thresh = Variable(thresh).cuda()
		else:
			raw = Variable(raw)
			thresh = Variable(thresh)

		# ===================forward=====================
		output = model(raw.float())
		# print(f'outputshape:{output.shape}, gtshape:{gt.shape}')
		loss = criterion(output.float(), thresh.float())
		print(f'loss: {loss.data}')
		# ===================backward====================
		loss.backward()

		# To print the weights of the model:
		#for name, param in model.named_parameters():
			#print(name, param.grad)

		optimizer.step()

	# ===================log========================
	print('epoch [{}/{}], loss:{:.4f}'.format(epoch + 1, num_epochs, loss.data), flush = True)

	if epoch % 5 == 0:
		if epoch > 0:
			torch.save(model.state_dict(), './autoencoder.pth')
