from flask import render_template
import os
from app import app

DATA_BASE_FOLDER = '/Users/yasser/sci-repo/pitchdataset'

IMAGE_FOLDER = 'images'
GROUND_TRUTH_FOLDER = 'groundTruth'
GT_EXT = '.json'

images_folder = os.path.join(DATA_BASE_FOLDER, IMAGE_FOLDER)
ground_truth_folder = os.path.join(DATA_BASE_FOLDER, GROUND_TRUTH_FOLDER)

def find_sub_dirs(directory):
    subdirs = []
    for x in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, x)):
            subdirs.append(x)
    return subdirs

def find_all_images(directory, subd):
    files = []
    for x in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, x)):
            x_basename = os.path.splitext(x)[0]
            ground_truth_file_name = os.path.join(os.path.join(ground_truth_folder, subd), x_basename + GT_EXT)
            has_ground_truth = os.path.isfile(ground_truth_file_name)
            files.append({'filename': x, 'basename': x_basename, 'truth': has_ground_truth})
    # sort the files so that the files with no ground truth are up in the list
    files.sort(key=lambda x: x['truth'], reverse=False)
    return files

@app.route('/')
@app.route('/index')
def index():
    subdirs = find_sub_dirs(images_folder)

    images = {}
    for subd in subdirs:
        images[subd] = find_all_images(os.path.join(images_folder, subd), subd)

    data = {
        'subdirs': subdirs,
        'images': images
    }
    return render_template("main.html", **data)


@app.route('/a/<subd>/<img_name>')
def annotate(subd, img_name):
    data = {
        'image_src': "/static/dataset/images/%s/%s" % (subd, img_name),
        'subd' : subd,
        'img_name': img_name
    }

    return render_template("annotate.html", **data)
    