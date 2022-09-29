import os

import scipy
import scipy.ndimage
import nibabel as nib
import numpy as np
import zarr
import Model.constants_and_paths as mcp

from Model.constants_and_paths import ROOT_STR

alpha = 0.1

print('START')

data_dir = mcp.ROOT_STR

# zarr_path = os.path.join(data_dir, "3Dexpandedprocessed.zarr")
zarr_path = os.path.join(data_dir, "3Dexpanded.zarr")
raw_data = zarr.open(zarr_path, mode='r')

n_samples = np.shape(raw_data['raw'])[0]

for index in range(n_samples):
	raw = raw_data['raw'][index]
	predict = np.load(data_dir+f'\\output_{index}.npy')

	raw = np.copy(raw)
	predict = np.squeeze(predict)

	#print(np.shape(raw))
	#print(np.shape(predict))

	predict[predict <= alpha] = 0
	predict[predict > alpha] = 1

	for i in range(np.shape(predict)[0]):
		predict[i] = scipy.ndimage.morphology.binary_fill_holes(predict[i])

	raw[predict == 0] = 0

	img = nib.Nifti1Image(raw, affine = np.eye(4))
	nib.save(img, 'out.nii')

	np.save(data_dir+'\\surface_'+str(index)+'.npy', raw)

	print(f"{index} is done")

print('DONE')
