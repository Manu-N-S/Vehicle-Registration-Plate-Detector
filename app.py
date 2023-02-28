from flask import Flask, render_template, Response, request, after_this_request
import os 

from deeplearning import object_detection
from camera import VideoCamera

app = Flask(__name__)
BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')


@app.route('/')
def home():
    return render_template('front.html')

@app.route('/Live')
def index():
    return render_template('index.html')

def generate_frames(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH,filename)
        upload_file.save(path_save)
        text_list = object_detection(path_save,filename)
        
        print(text_list)

        return render_template('upload.html',upload=True,upload_image=filename,text=text_list,no=len(text_list))

    return render_template('upload.html',upload=False)

if __name__ == '__main__':
    app.run(debug=True)
