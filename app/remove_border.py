import cv2
import glob

FOLDER = '/Users/yasser/Desktop/azadi/frames/'
EXT = 'jpg'

def main():
    """
    This script removes the ugly border which is present in PTZ cameras of Azadi dataset.
    """
    files = glob.glob("%s*.%s" % (FOLDER, EXT))

    for file in files:
        img = cv2.imread(file)
        img2 = img[:-2, 10:-15]
        cv2.imwrite(file, img2)
        print file

if __name__ == '__main__':
    main()