from flask import render_template
import os
from app import app

DATA_BASE_FOLDER = '/Users/yasser/sci-repo/pitchdataset'

IMAGE_FOLDER = 'images'
GROUND_TRUTH_FOLDER = 'groundTruth'


def find_sub_dirs(directory):
    subdirs = []
    for x in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, x)):
            subdirs.append(x)
    return subdirs

def find_all_images(directory):
    files = []
    for x in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, x)):
            files.append({'filename': x, 'basename': os.path.splitext(x)[0]})
    return files

@app.route('/')
@app.route('/index')
def index():
    images_folder = os.path.join(DATA_BASE_FOLDER, IMAGE_FOLDER)
    subdirs = find_sub_dirs(images_folder)

    images = {}
    for subd in subdirs:
        images[subd] = find_all_images(os.path.join(images_folder, subd))

    data = {
        'subdirs': subdirs,
        'images': images
    }
    return render_template("main.html", **data)
