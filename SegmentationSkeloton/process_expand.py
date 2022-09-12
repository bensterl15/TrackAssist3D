import numpy as np
import tifffile
import os 
import scipy
import scipy.signal
import zarr
import nibabel as nib

def save_to_container(arr, container, name):
    for i in range(arr.shape[0]):
        dataset = container.create_dataset(name + '/' + str(i), shape=arr[i].shape)
        dataset[:] = arr[i]

names = []

zarr_container = zarr.open('3Dexpanded.zarr', 'w')

for i in range(21):
    names.append('T' + str(i+1))
    
raw = np.zeros((21, 60, 256, 256))
num_name = 0
for name in names:

    if num_name != 0:
        continue

    raw_ = 0
    try:
        raw_ = tifffile.imread(os.path.join('raw', name, name + '.tiff'))
    except:
        raw_ = tifffile.imread(os.path.join('raw', name, name + '.tif'))

    raw_ = scipy.signal.resample(raw_, 40, axis = 0)
    raw_ = raw_ / np.max(raw_)
    
    mean_x = 0
    mean_y = 0
    for z_ind in range(14):
        for x_ind in range(512):
            for y_ind in range(512):
                mean_x += x_ind * raw_[z_ind, x_ind, y_ind]
                mean_y += y_ind * raw_[z_ind, x_ind, y_ind]
    
    mean_x = int(mean_x)
    mean_y = int(mean_y)
        
    # Override for now.. UGH
    mean_x = 130
    mean_y = 315
    width = 128
    
    print(num_name)
    
    raw[num_name, 10:50] = raw_[:,(mean_x-width):(mean_x+width),(mean_y-width):(mean_y+width)]

    img = nib.Nifti1Image(raw[num_name, 10:50], affine=np.eye(4))
    nib.save(img, f'ugh{name}.nii')

    #raw[raw < 0.2] = 0
        
    num_name = num_name + 1
    
    
save_to_container(raw, zarr_container, 'raw')