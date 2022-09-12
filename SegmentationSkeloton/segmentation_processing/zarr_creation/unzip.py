# UNZIP THE ZARR FILES SO WE CAN RUN THE 2D THRESHOLDING NETWORK ON IT

import zarr
import os
import numpy as np

#training = zarr.open('3Dtraining.zarr', 'r')
expanded = zarr.open('3Dexpanded.zarr', 'r')

#n_samples = np.shape(training['raw'])[0]

#Nz_training = np.shape(training['raw'][0])[0]
Nz_expanded = np.shape(expanded['raw'][0])[0]

#os.mkdir('3Dtraining')
os.mkdir('3Dexpanded')

#os.mkdir('3Dtraining/raw')
#os.mkdir('3Dtraining/gt')

os.mkdir('3Dexpanded/raw')

#n_training_samples = np.shape(training['raw'])[0]
n_expanded_samples = np.shape(expanded['raw'])[0]

'''
for i in range(n_training_samples):
	os.mkdir(f'3Dtraining/raw/{i}')
	os.mkdir(f'3Dtraining/gt/{i}')
	for j in range(Nz_training):
		r_img = training['raw'][i][j]
		g_img = training['gt'][i][j]
		np.save(f'3Dtraining/raw/{i}/{j}.npy', r_img)
		np.save(f'3Dtraining/gt/{i}/{j}.npy', g_img)
'''

for i in range(n_expanded_samples):
	os.mkdir(f'3Dexpanded/raw/{i}')
	for j in range(Nz_expanded):
		r_img = expanded['raw'][i][j]
		np.save(f'3Dexpanded/raw/{i}/{j}.npy', r_img)
