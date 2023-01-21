import cv2
import glob

images = [cv2.imread(file) for file in glob.glob('images/*.jpg')]

# import ipdb
# ipdb.set_trace()
