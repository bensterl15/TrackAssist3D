# ZIP THE ZARR FILES SO WE CAN RUN THE 3D NETWORK ON IT

import zarr
import os
import numpy as np

#training = zarr.open('3Dtrainingprocessed.zarr', 'w')
expanded = zarr.open('3Dexpandedprocessed.zarr', 'w')

def save_to_container(arr, container, name):
	for i in range(arr.shape[0]):
		dataset = container.create_dataset(name + '/' + str(i), shape=arr[i].shape)
		dataset[:] = arr[i]

#raw = np.zeros((21, 14, 256, 256))
#gt  = np.zeros((21, 14, 256, 256))
ex = np.zeros((21, 60, 256, 256))

'''
for i in range(21):
	for j in range(14):
		raw[i, j] = np.load(f'3Dtraining/raw/{i}/{j}.npy')
		gt[i, j] = np.load(f'3Dtraining/gt/{i}/{j}.npy')
'''

for i in range(21):
	for j in range(60):
		ex[i, j] = np.load(f'3Dexpanded/raw/{i}/{j}.npy')

#save_to_container(raw, training, 'raw')
#save_to_container(gt,  training, 'gt')
save_to_container(ex,  expanded, 'raw')
