import os
from flask import Flask

from dotenv import load_dotenv
# loading the envrionment variables from the root folder.
load_dotenv()

# Import your blueprint object from routes.py
from routes.route import main_bp



app = Flask(__name__)

# global  configuration for the secret key
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')


# Global Configuration for storage

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


# Register your blueprint here
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
