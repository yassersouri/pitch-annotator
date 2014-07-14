from flask import render_template
from flask import json
from flask import request
import os
from app import app

DATA_BASE_FOLDER = 'E:/Code Vault/Github/pitch-annotator/dataset'

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

def get_ground_truth_file_name(img_file_name, subd):
    x_basename = os.path.splitext(img_file_name)[0]
    ground_truth_file_name = os.path.join(os.path.join(ground_truth_folder, subd), x_basename + GT_EXT)
    return x_basename, ground_truth_file_name

def get_ground_truth_subfolder(subd):
    ground_truth_subfolder = os.path.join(ground_truth_folder, subd)
    return ground_truth_subfolder

def find_all_images(directory, subd):
    files = []
    for x in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, x)):
            x_basename, ground_truth_file_name = get_ground_truth_file_name(x, subd)
            has_ground_truth = has_actual_lines_in_ground_truth(ground_truth_file_name)
            files.append({'filename': x, 'basename': x_basename, 'truth': has_ground_truth})
    # sort the files so that the files with no ground truth are up in the list
    files.sort(key=lambda x: x['truth'], reverse=False)
    return files

def has_actual_lines_in_ground_truth(ground_truth_file_name):
    try:
        with open(ground_truth_file_name, 'r') as infile:
            lines = json.loads(infile.read())
            if len(lines) > 0:
                return True
    except Exception, e:
        return False
    return False

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


@app.route('/s/<subd>/<img_name>', methods=['POST'])
def persist(subd, img_name):
    lines = request.json
    x_basename, ground_truth_file_name = get_ground_truth_file_name(img_name, subd)
    ground_truth_subfolder = get_ground_truth_subfolder(subd)
    if not os.path.exists(ground_truth_subfolder):
        os.makedirs(ground_truth_subfolder)
    with open(ground_truth_file_name, 'w') as outfile:
        outfile.write(json.dumps(lines))
    return json.jsonify(m='OK')

@app.route('/g/<subd>/<img_name>', methods=['GET'])
def retrieve(subd, img_name):
    x_basename, ground_truth_file_name = get_ground_truth_file_name(img_name, subd)
    data = {'has': False}
    if os.path.isfile(ground_truth_file_name):
        with open(ground_truth_file_name, 'r') as infile:
            lines = json.loads(infile.read())
            if len(lines) > 0:
                data['has'] = True
            data['lines'] = lines
        return json.jsonify(**data)
    else:
        return json.jsonify(**data)
