import scipy.io
import glob
import json
import cv2
import numpy

json_file_name = '/Users/yasser/sci-repo/pitchdataset/groundTruth/train/2.json'
img_file_name = '/Users/yasser/sci-repo/pitchdataset/images/train/2.jpg'

def do_stuff(json_file_name, img_file_name):
    img = cv2.imread(img_file_name)
    shape = img.shape[0:2]
    lines = 0
    with open(json_file_name, 'r') as f:
        lines = json.loads(f.read())
    
    edge = numpy.zeros(shape, dtype=numpy.uint8)
    segs_pre = numpy.ones(shape, dtype=numpy.uint8) * 255
    segs = numpy.zeros(shape, dtype=numpy.uint8)

    for line in lines:
        cv2.line(segs_pre, (int(line['x1']), int(line['y1'])), (int(line['x2']), int(line['y2'])), (0, 0, 0), thickness=1)
        cv2.line(edge, (int(line['x1']), int(line['y1'])), (int(line['x2']), int(line['y2'])), (255, 255, 255), thickness=1)

    cv2.imshow('test', segs_pre)
    cv2.waitKey(0)

def main():

    do_stuff(json_file_name, img_file_name)

if __name__ == '__main__':
    main()