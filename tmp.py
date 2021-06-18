# # import the necessary packages
# import numpy as np
# import cv2
# from skimage.measure import compare_ssim

# def compare_images(imageA, imageB):
# 	# compute the mean squared error and structural similarity
# 	# index for the images
# 	m = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
# 	m /= float(imageA.shape[0] * imageA.shape[1])
# 	s = compare_ssim(imageA, imageB)
# 	print ("ssim= ",s,"mse= ",m)
	

# # load the images -- the original, the original + contrast,
# # and the original + photoshop
# original = cv2.imread("images/download.png")
# contrast = cv2.imread("images/download1.png")
# # convert the images to grayscale
# original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
# contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
# compare_images(original, original)
# compare_images(original, contrast)

from PIL import Image
import imagehash
hash0 = imagehash.average_hash(Image.open('images/download.png')) 
hash1 = imagehash.average_hash(Image.open('images/download1.png')) 
cutoff = 5  # maximum bits that could be different between the hashes. 

print("img1: ",hash0,"img2: ",hash1)