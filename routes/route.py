import os
import uuid
import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from werkzeug.utils import secure_filename
from PIL import Image

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Helper function to validate file extensions."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main_bp.route("/")
def home():
    return render_template('landing.html')


@main_bp.route("/avatar_selection", methods=['GET', 'POST'])
def avatar_selection():
    # --- POST METHOD (Handling Submission) ---
    global method
    method = None # The  variable to check the  type of  upload

    if request.method == 'POST':
        if 'avatar_file' not in request.files and 'avatar_file' not in request.form:
            flash('No file data received.', 'error')
            return redirect(request.url) 

        avatar_data = request.form.get('avatar_file')
        success = False  # Track if asset processing succeeded

        # Case 1: User selected an existing avatar URL from the UI list
        if avatar_data and not request.files.get('avatar_file'):
            try:
                response = requests.get(avatar_data)
                if response.status_code == 200:
                    filename = f"avatar_image.jpg"
                    save_to = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
                    with open(save_to, 'wb') as f:
                        f.write(response.content)
                
                    flash('Avatar downloaded and saved successfully!', 'success')
                    success = True
                    method= 'avatar_upload'
                else:
                    flash('Failed to fetch avatar from api.', 'error')
            except Exception as e:
                flash(f'Error saving avatar: {str(e)}', 'error')

        # Case 2: User uploaded a file from their local computer
        else:
            file = request.files['avatar_file']

            if file.filename == '':
                flash('No file selected.', 'error')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                # Reset file pointer to beginning before reading
                file.seek(0)
                img = Image.open(file)
                
                if img.size[0] >= 300 and img.size[1] >= 300:
                    filename = secure_filename(file.filename)

                    extension = filename.rsplit('.', 1)[1].lower() # getting th extension of the  file to append  later
                    filename = f"upload_avatar.{extension}"
                    save_to = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    
                    # Reset pointer again before saving file to disk
                    file.seek(0)
                    file.save(save_to)
                
                    flash('Uploaded successfully!', 'success')
                    success = True
                    method= 'file_upload'

                else:
                    flash('Dimensions too small (expected: at least 300x300 px).', 'error')
            else:
                flash('Invalid file type.', 'error')

        
        if success:
            return redirect(url_for('main.final', method= method))
        
        # If validation or download failed, reload current page safely
        return redirect(request.url)

    # --- GET METHOD (Runs when user opens or fails form validation) ---
    # Store seeds in session so they persist across page reloads/failed posts
    if 'suggested_seeds' not in session:
        session['suggested_seeds'] = [str(uuid.uuid4()) for _ in range(9)]
        
    chosen_style = "shapes" 
    return render_template(
        "avatar_selection.html", 
        style=chosen_style, 
        seed=session['suggested_seeds'], 
        current_step=1
    )


@main_bp.route("/final")
def final():
    method = request.args.get('method')

    return render_template(
        'username_avatar.html',
        method=method)

@main_bp.route("/krishna") 
def krishna():
    return "Hare krishna!!"
