import scipy.io
import glob
import json
import cv2
import numpy
import skimage.morphology
from matplotlib import pylab as plt

json_file_name = '/Users/yasser/sci-repo/pitchdataset/groundTruth/train/3.json'
img_file_name = '/Users/yasser/sci-repo/pitchdataset/images/train/3.jpg'

def gen_one_ground_truth(json_file_name, img_file_name):
    img = cv2.imread(img_file_name)
    shape = img.shape[0:2]
    lines = 0
    with open(json_file_name, 'r') as f:
        lines = json.loads(f.read())
    
    # allocate memory
    edge = numpy.zeros(shape, dtype=numpy.uint8)
    segs_pre = numpy.ones(shape, dtype=numpy.uint8) * 255
    segs = numpy.zeros(shape, dtype=numpy.uint8)

    # drawlines
    for line in lines:
        cv2.line(segs_pre, (int(line['x1']), int(line['y1'])), (int(line['x2']), int(line['y2'])), (0, 0, 0), thickness=1)
        cv2.line(edge, (int(line['x1']), int(line['y1'])), (int(line['x2']), int(line['y2'])), (255, 255, 255), thickness=1)

    # find segments
    segs = skimage.morphology.label(segs_pre, 4, 0)

    # label pixels with value of -1 (edge pixels)
    for i in range(segs.shape[0]):
        for j in range(segs.shape[1]):
            if segs[i, j] == -1:
                if i-1 > 0:
                    if segs[i-1, j] != -1:
                        segs[i, j] = segs[i-1, j]
                elif j-1 > 0:
                    if segs[i, j-1] != -1:
                        segs[i, j] = segs[i, j-1]


    result = {'edge': edge, 'segs': segs}
    return result

def main():
    gen_one_ground_truth(json_file_name, img_file_name)

if __name__ == '__main__':
    main()