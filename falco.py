import json
from flask import Response
import image_proc
import os
from flask import Flask, request, url_for, redirect, send_from_directory
import flask
from werkzeug.utils import secure_filename
import Image

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            base_name, file_extension = os.path.splitext(filename)
            im.save(os.path.join(app.config['UPLOAD_FOLDER'], base_name + '.png'))
            res = image_proc.getMatches()
            arr = []
            for fn in res:
                arr.append('/uploads/' + fn)
            ky = {'key': arr}
            dat = json.dumps(ky)
            resp = Response(response=dat, status=200, mimetype="application/json")
            return(resp)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
