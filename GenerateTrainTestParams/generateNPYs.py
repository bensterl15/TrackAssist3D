import pickle

num_fmaps = 256
batch_size = 2
train_until = 2000
snapshot_every = 50
in_channels = 1,
fmap_inc_factor = 2,
conv_in_channels = 1
learning_rate = 5e-5

input_shape = (12, 128, 128)
output_shape = (2, 88, 88)
voxel_size = (1, 1, 1)
downsample_factors = [[1, 2, 2], [1, 2, 2],]
kernel_size_down = [[[2, 3, 3], [2, 3, 3]]] * 3
kernel_size_up = [[[2, 3, 3], [2, 3, 3]]] * 2
conv_kernel = [[1, 1, 1]]

D = {
    'num_fmaps':num_fmaps,
    'batch_size':batch_size,
    'train_until': train_until,
    'snapshot_every': snapshot_every,
    'in_channels': in_channels,
    'fmap_inc_factor': fmap_inc_factor,
    'conv_in_channels': conv_in_channels,
    'learning_rate': learning_rate,
    'input_shape':input_shape,
    'output_shape':output_shape,
    'voxel_size':voxel_size,
    'downsample_factors':downsample_factors,
    'kernel_size_down':kernel_size_down,
    'kernel_size_up':kernel_size_up,
    'conv_kernel':conv_kernel,
}

with open('network_params.pickle', 'wb') as handle:
    pickle.dump(D, handle, protocol=pickle.HIGHEST_PROTOCOL)

#convpass = ConvPass(num_fmaps, 1, [[1, 1, 1]], activation='Sigmoid')