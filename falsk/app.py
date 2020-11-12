#!flask/bin/python

# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/
from __future__ import print_function
import os
import PIL
from PIL import Image
import simplejson
import traceback

from flask import Flask, request, render_template, flash, jsonify, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename

from lib.upload_file import uploadfile

from werkzeug.middleware.shared_data import SharedDataMiddleware
import sys
sys.path.insert(0, "/home/dev/Desktop/using_ray/CBIR-master/src")


from evaluate import inferInput
from NGT import search4flask as search

import matplotlib.pyplot as plt
import matplotlib.image as mpimg


depth = 5
d_type = 'L2' # L1 , L2, Angle ,Normalized Angle, Cosine, Normalized Cosine, Hamming,Jaccard
f_class = 'vgg' # 'daisy' , 'edge' ,hog' , 'res' , 'vgg'



app = Flask(__name__)
app.secret_key = "secret key"
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['IMAGES_FOLDER'] = 'data/images'
app.config['THUMBNAIL_FOLDER'] = 'data/thumbnail/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['DEPTH']= 4
# app.config['F_CLASS']= 'res'
app.config['D_TYPE']= 'L2'

ALLOWED_EXTENSIONS = set(['txt', 'gif', 'png', 'jpg',
                          'jpeg', 'bmp'])
IGNORED_FILES = set(['.gitignore'])

bootstrap = Bootstrap(app)
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename


def create_thumbnail(image):
    try:
        base_width = 80
        img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))

        return True

    except:
        # print traceback.format_exc()
        return False



# @app.route("/upload", methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         files = request.files['file']

#         if files:
#             filename = secure_filename(files.filename)
#             filename = gen_file_name(filename)
#             mime_type = files.content_type

#             if not allowed_file(files.filename):
#                 result = uploadfile(
#                     name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")

#             else:
#                 # save file to disk
#                 uploaded_file_path = os.path.join(
#                     app.config['UPLOAD_FOLDER'], filename)
#                 files.save(uploaded_file_path)

#                 # create thumbnail after saving
#                 if mime_type.startswith('image'):
#                     create_thumbnail(filename)

#                 # get file size after saving
#                 size = os.path.getsize(uploaded_file_path)

#                 # return json for js call back
#                 result = uploadfile(name=filename, type=mime_type, size=size)

#             return simplejson.dumps({"files": [result.get_file()]})

#     if request.method == 'GET':
#         # get all file in ./data directory
#         files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(
#             os.path.join(app.config['UPLOAD_FOLDER'], f)) and f not in IGNORED_FILES]

#         file_display = []

#         for f in files:
#             size = os.path.getsize(os.path.join(
#                 app.config['UPLOAD_FOLDER'], f))
#             file_saved = uploadfile(name=f, size=size)
#             file_display.append(file_saved.get_file())

#         return simplejson.dumps({"files": file_display})

#     return redirect(url_for('index'))


@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
@app.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename=filename)


@app.route("/data/images/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['IMAGES_FOLDER']), filename=filename)


# @app.route('/test/', methods=['GET', 'POST'])
# def test():
#     return render_template('estore/product_list.html')


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed')
        return render_template('product_list.html', filename=filename)

    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/postimg', methods=['POST'])
def postimg():
    l = []

    if 'img' not in request.files:
        return '{"id": 0}'
    file = request.files['img']
    filename = '111.JPEG'
    linkInput = os.path.join('/home/dev/Desktop/using_ray/CBIR-master/flask-file-uploader-master/data/', filename)
    file.save(os.path.join('/home/dev/Desktop/using_ray/CBIR-master/flask-file-uploader-master/data/', filename))


    # results_res = search(link=linkInput,f_class='res',d_type=app.config['D_TYPE'],depth=app.config['DEPTH'])
    
    results_vgg = search(link=linkInput,f_class='res',d_type=app.config['D_TYPE'],depth=app.config['DEPTH'])
   
    # results_daisy = search(link=linkInput,f_class='daisy',d_type=app.config['D_TYPE'],depth=app.config['DEPTH'])
    # results_hog = search(link=linkInput,f_class='hog',d_type=app.config['D_TYPE'],depth=app.config['DEPTH'])
    # results_edge = search(link=linkInput,f_class='edge',d_type=app.config['D_TYPE'],depth=app.config['DEPTH'])

    # for item in result:


        
    
    #     links = os.path.join(app.config['IMAGES_FOLDER'], item)
    #     linkweb = item.get('link')
    #     l.append(links)
       
    


    # print(img)
    # return url_for('result'),
    # return render_template('result.html',file = files_Gym)
    info = {
        "vgg": results_vgg,
        # "res": results_res,
        # "daisy":results_daisy,
        # "hog":results_hog,
        # "edge":results_edge

    }
 
    return jsonify(info)


@app.route('/data/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('data', filename='/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
