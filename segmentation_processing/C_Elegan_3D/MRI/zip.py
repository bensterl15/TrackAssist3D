# ZIP THE ZARR FILES SO WE CAN RUN THE 3D NETWORK ON IT

import zarr
import os
import numpy as np

train = zarr.open('trainprocessed.zarr', 'w')
test = zarr.open('testprocessed.zarr', 'w')

def save_to_container(arr, container, name):
	for i in range(arr.shape[0]):
		dataset = container.create_dataset(name + '/' + str(i), shape=arr[i].shape)
		dataset[:] = arr[i]

n_samples = 10
Nz = 192
Nx = 256
Ny = 256
train_raw = np.zeros((n_samples, Nz, Nx, Ny))
train_gt  = np.zeros((n_samples, Nz, Nx, Ny))
test_raw  = np.zeros((n_samples, Nz, Nx, Ny))
test_gt   = np.zeros((n_samples, Nz, Nx, Ny))

for i in range(n_samples):
	for j in range(14):
		train_raw[i, j] = np.load(f'train_r/raw/{i}/{j}.npy')
		train_gt[i, j]  = np.load(f'train_r/gt/{i}/{j}.npy')
		test_raw[i, j]  = np.load(f'test_r/raw/{i}/{j}.npy')
		test_gt[i, j]   = np.load(f'test_r/gt/{i}/{j}.npy')

save_to_container(train_raw, train, 'raw')
save_to_container(train_gt,  train, 'gt')
save_to_container(test_raw,  test, 'raw')
save_to_container(test_gt, test, 'gt')
