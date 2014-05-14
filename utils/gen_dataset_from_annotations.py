import os
import random
import shutil
from gen_groundTruth import gen_one_ground_truth
import scipy.io

ANNOTATION_CLASSES  = ['cam1_S2','cam3_S2','cam6_S2','cam8_S2','cam2_S2','cam4_S2','cam7_S2','cam9_S2']
TRAIN_PERCENT = 0.66

IMAGE_FORMATS = ['.jpg', '.jpeg', '.png']

ROOT_ANNOTATIONS = '/Users/yasser/sci-repo/pitchdataset/'
ROOT_DATASET = '/Users/yasser/Desktop/Azadi_S_A/'

IMAGES = 'images'
GROUNDTRUTH = 'groundTruth'

GROUNDTRUTH_EXT = '.mat'
IMAGE_EXT = '.jpg'
JSON_EXT = '.json'

dataset_images_folder_train = os.path.join(os.path.join(ROOT_DATASET, IMAGES), 'train')
dataset_images_folder_val = os.path.join(os.path.join(ROOT_DATASET, IMAGES), 'val')
dataset_groundtruth_folder_train = os.path.join(os.path.join(ROOT_DATASET, GROUNDTRUTH), 'train')
dataset_groundtruth_folder_val = os.path.join(os.path.join(ROOT_DATASET, GROUNDTRUTH), 'val')

def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def main():
    ensure_folder(dataset_groundtruth_folder_val)
    ensure_folder(dataset_groundtruth_folder_train)
    ensure_folder(dataset_images_folder_val)
    ensure_folder(dataset_images_folder_train)
    num = 1


    for CLASS in ANNOTATION_CLASSES:
        images_folder = os.path.join(os.path.join(ROOT_ANNOTATIONS, IMAGES), CLASS)
        jsons_folder = os.path.join(os.path.join(ROOT_ANNOTATIONS, GROUNDTRUTH), CLASS)
        for IMG in os.listdir(images_folder):
            IMG_EXT = os.path.splitext(IMG)[-1]
            IMG_BASE = os.path.splitext(IMG)[0]

            image_address = os.path.join(images_folder, IMG)
            json_address = os.path.join(jsons_folder, IMG_BASE + JSON_EXT)
            if os.path.isfile(image_address):
                if IMG_EXT in IMAGE_FORMATS:
                    if random.random() < TRAIN_PERCENT:
                        dest_image_address = os.path.join(dataset_images_folder_train, '%d%s' % (num, IMAGE_EXT))
                        dest_groundtruth_address = os.path.join(dataset_groundtruth_folder_train, '%d%s' % (num, GROUNDTRUTH_EXT))
                    else:
                        dest_image_address = os.path.join(dataset_images_folder_val, '%d%s' % (num, IMAGE_EXT))
                        dest_groundtruth_address = os.path.join(dataset_groundtruth_folder_val, '%d%s' % (num, GROUNDTRUTH_EXT))
                    shutil.copyfile(image_address, dest_image_address)
                    gt = gen_one_ground_truth(json_address, image_address)
                    scipy.io.savemat(dest_groundtruth_address, gt, do_compression=True)
            print num
            num += 1

if __name__ == '__main__':
    main()