# import cv
import cv2
# import math
import numpy

def hue_keyer(img, theta=120, acceptance_angle=90):
	LB = (theta - acceptance_angle)
	UB = (theta + acceptance_angle)

	# result = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
	result = numpy.zeros((img.shape[0], img.shape[1]))

	# img_HSV = cv.CreateMat(img.rows, img.cols, cv.CV_8UC3)
	img_HSV = numpy.zeros(img.shape)
	# cv2.CvtColor(img, img_HSV, cv.CV_RGB2HSV)
	img_HSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

	# img_HSV_array = numpy.asarray(img_HSV)
	# result_array = numpy.asarray(result)
	result[(img_HSV[:,:,0] > LB) & (img_HSV[:,:,0] < UB)] = 255

	return result