import cv2
import os
import line_filter
import chroma

INPUT_DIR = '/Users/yasser/Desktop/result-2/img/'
OUT_DIR = '/Users/yasser/Desktop/result-2/out-thomas/'

IMAGE_FORMATS = ['.jpg', '.jpeg', '.png']
IMAGE_EXT = '.jpg'

def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def main():
    ensure_folder(OUT_DIR)

    for IMG in os.listdir(INPUT_DIR):
        IMG_EXT = os.path.splitext(IMG)[-1]
        IMG_BASE = os.path.splitext(IMG)[0]

        image_address = os.path.join(INPUT_DIR, IMG)
        out_address = os.path.join(OUT_DIR, IMG_BASE + IMAGE_EXT)

        if os.path.isfile(image_address):
            if IMG_EXT in IMAGE_FORMATS:
                img = cv2.imread(image_address)
                keyer = chroma.hue_keyer(img, theta=110.0*255/360, acceptance_angle=20)
                edge = line_filter.line_detection_filter(img[:,:,0], keyer)
                edge = 255 - edge

                cv2.imwrite(out_address, edge)
                print image_address

if __name__ == '__main__':
    main()