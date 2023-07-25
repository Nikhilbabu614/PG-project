from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from mainP import DigitalImageTampering
from enhanced import Enhanced_DigitalImageTampering
import cv2
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
RESULTS_FOLDER = 'static/results/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enhanced')
def enhanced():
    return render_template('enhanced.html')


@app.route('/', methods=['POST'])
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
        resultImage = DigitalImageTampering(7,UPLOAD_FOLDER+filename)
        resultImageName = '/'+filename
        cv2.imwrite(f'{RESULTS_FOLDER}{resultImageName}',resultImage)
        return render_template('result.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_original_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/display_res/<filename>')
def display_result_image(filename):
    return redirect(url_for('static', filename='results/' + filename), code=301)


@app.route('/enhanced', methods=['POST'])
def upload_image_for_enhanced():
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
        resultImage = Enhanced_DigitalImageTampering(UPLOAD_FOLDER+filename)
        resultImageName = '/'+filename
        cv2.imwrite(f'{RESULTS_FOLDER}{resultImageName}',resultImage)
        return render_template('enhanced_result.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
if __name__ == "__main__":
    app.run()