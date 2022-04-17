import numpy as np
import matplotlib.pyplot as plt

view_slice = 145
# Linear SNR scale:
SNR = 10

AR_Coefs = np.array([0.6, 0.5, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2])/6

im = np.load('../BRAIN.npy')
im = im / np.max(im)

im2 = np.zeros((256, 256, im.shape[2]+20))
x_start = int((256 - im.shape[0])/2)
y_start = int((256 - im.shape[1])/2)
z_start = 10

x_end = x_start + im.shape[0]
y_end = y_start + im.shape[1]
z_end = z_start + im.shape[2]

im2[x_start:x_end, y_start:y_end, z_start:z_end] = im[:,:,:]

im = im2
print(im.shape)

# Generate the ground truth:
gt = im.copy()
gt[gt > 0] = 1
gt[gt < 0] = 0

# Store a copy without noise:
im_orig = im.copy()

# Insert additive noise:
n = np.random.normal(loc=0, scale=1, size=im.shape)/SNR
im = im + n

for z in range(im.shape[2]):
	# At the very bottom layer, there is nothing to reflect:
	reflection = np.zeros((im.shape[0], im.shape[1]))
	for i in range(AR_Coefs.shape[0]):
		# We use the original because otherwise we would experience double the measurement noise:
		if z - i >= 0:
			reflection = reflection + AR_Coefs[i] * im_orig[:, :, z - i]
	# Where the object is present, there is no reflection from underneath:
	reflection[gt[:, :, z] == 1] = 0
	im[:, :, z] = im[:, :, z] + reflection

np.save('brain_processed.npy', im)

'''
plt.subplot(121)
plt.imshow(im[:,:,view_slice])
plt.title('Image+Noise+Reflection')

im[gt==1] = 1

plt.subplot(122)
plt.imshow(im[:,:,view_slice])
plt.title('Image with gt selected')
plt.show()
'''
