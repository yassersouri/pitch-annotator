pitch-annotator
===============

Annotate sports pitch lines in images


Running the code
================

requirements
------------

### 1

`pip install -r requirements.txt`

### 2

Download [this](https://github.com/yassersouri/pitch-annotator/releases/download/init/dataset.zip). Then Extract it to a place where you want to store the image files and the produced annotations.

### 3

In [this line of code](https://github.com/yassersouri/pitch-annotator/blob/new-ui/app/views.py#L7), change the value of `DATA_BASE_FOLDER` to the **absolute** path of the dataset you just created.

running the code
----------------

`python run.py`

Then go to <http://127.0.0.1:5000/>