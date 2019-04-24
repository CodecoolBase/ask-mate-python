from flask import Flask
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='../templates', static_folder='../static')
photos = UploadSet('photos', IMAGES)
base_url = 'http://127.0.0.1:5004'

app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
app.config['SECRET_KEY'] = '0b95219177b86d8db3fbde38daf944f0'
# prevent catching files in browser:
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
configure_uploads(app, photos)

bcrypt = Bcrypt(app)
