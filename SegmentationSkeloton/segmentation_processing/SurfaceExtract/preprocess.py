import scipy
import scipy.ndimage
import nibabel as nib
import numpy as np
import zarr

alpha = 0.1

index = 0

print('START')
raw = zarr.open('../zarr_creation/3Dexpandedprocessed.zarr', mode='r')
raw = raw['raw'][index]
predict = np.load(f'../3DUnet/output_{index}.npy')

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

np.save('surface.npy', raw)

print('DONE')
