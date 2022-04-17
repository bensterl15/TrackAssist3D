# UNZIP THE ZARR FILES SO WE CAN RUN THE REFLECTION / 2D THRESHOLDING NETWORK ON IT

import zarr
import os
import numpy as np

# SNR = 5 dB
SNR = 10**(5/20)

# Reflection (Auto-Regressive) coefficients
AR_Coefs = np.array([0.6, 0.5, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2])/6

train = zarr.open('MRI_train.zarr', 'r')
test = zarr.open('MRI_test.zarr', 'r')

n_samples = np.shape(train['raw'])[0]

Nz = np.shape(train['raw'][0])[0]
Nx = np.shape(train['raw'][0][0])[0]
Ny = np.shape(train['raw'][0][0][0])[0]
raw_train = np.zeros((n_samples, Nz, 256, 256))
gt_train  = np.zeros((n_samples, Nz, 256, 256))
raw_test  = np.zeros((n_samples, Nz, 256, 256))
gt_test   = np.zeros((n_samples, Nz, 256, 256))

### APPLY REFLECTION HERE
x_start = int((256 - Nx)/2)
y_start = int((256 - Ny)/2)
#z_start = 0

x_end = x_start + Nx
y_end = y_start + Ny
#z_end = z_start + Nz

for i in range(n_samples):
	for j in range(Nz):
		raw_train[i, j, x_start:x_end, y_start:y_end] = train['raw'][i][j]
		raw_test [i, j, x_start:x_end, y_start:y_end] = test['raw'][i][j]
		gt_train [i, j, x_start:x_end, y_start:y_end] = train['gt'][i][j]
		gt_test  [i, j, x_start:x_end, y_start:y_end] = test['gt'][i][j]

raw_train_copy = raw_train.copy()
raw_test_copy = raw_test.copy()

for i in range(n_samples):
	for z in range(Nz):
		reflection_train = np.zeros((256, 256))
		reflection_test = np.zeros((256, 256))
		for j in range(AR_Coefs.shape[0]):
			if z - j >= 0:
				reflection_train = reflection_train + AR_Coefs[j] * raw_train_copy[i, z - j]
				reflection_test = reflection_test + AR_Coefs[j] * raw_test_copy[i, z - j]
	# Where the object is present, there is no reflection from underneath:
	reflection_train[gt_train[i, z] == 1] = 0
	reflection_test[gt_test[i, z] == 1] = 0
	
	raw_train[i,z] = raw_train[i,z] + reflection_train
	raw_test[i,z] = raw_test[i,z] + reflection_test
###

os.mkdir('train_r')
os.mkdir('test_r')

os.mkdir('train_r/raw')
os.mkdir('train_r/gt')

os.mkdir('test_r/raw')
os.mkdir('test_r/gt')

n_train_samples = np.shape(raw_train)[0]
n_test_samples  = np.shape(raw_test)[0]

for i in range(n_train_samples):
	os.mkdir(f'train_r/raw/{i}')
	os.mkdir(f'train_r/gt/{i}')
	for j in range(Nz):
		r_img = raw_train[i][j]
		g_img = gt_train[i][j]
		np.save(f'train_r/raw/{i}/{j}.npy', r_img)
		np.save(f'train_r/gt/{i}/{j}.npy', g_img)

for i in range(n_test_samples):
	os.mkdir(f'test_r/raw/{i}')
	os.mkdir(f'test_r/gt/{i}')
	for j in range(Nz):
		r_img = raw_test[i][j]
		g_img = gt_test[i][j]
		np.save(f'test_r/raw/{i}/{j}.npy', r_img)
		np.save(f'test_r/gt/{i}/{j}.npy', g_img)
