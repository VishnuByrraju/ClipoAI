from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone
from datetime import timedelta
from moviepy.editor import VideoFileClip
import shutil
import re
import os

# Initialize Flask app
app = Flask(__name__)

# Set up MongoDB
client = MongoClient('Your_Connection_String')
db = client['video_projects_db']

# Set up JWT
app.config['JWT_SECRET_KEY'] = 'clipoai_secret_key'
jwt = JWTManager(app)

# Define collection
video_projects = db['video_projects']
user_logins = db['user_logins']



# Function to generate thumbnail
def generate_thumbnail(video_path, thumbnail_path):
    clip = VideoFileClip(video_path)
    thumbnail = clip.save_frame(thumbnail_path, t=0.5)  # Extract thumbnail at 0.5 seconds
    clip.close()
    return thumbnail

# Allowed file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to secure filename
def secure_filename(filename):
    # Remove any special characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename

# API endpoints

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']
    if not user_logins.find_one({'username': username, 'password': password}):
        return jsonify({'message': 'Invalid credentials'}), 401
    # Create access token
    access_token = create_access_token(identity=username, expires_delta=timedelta(hours=1))
    return jsonify({'access_token': access_token}), 200

# Signup endpoint
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.form
    username = data['username']
    email = data['email']
    password = data['password']
    if user_logins.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 400
    if user_logins.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 400
    # Insert the user
    user_logins.insert_one({'username': username, 'email': email, 'password': password})
    return jsonify({'message': 'User created successfully'}), 201

# Get Video projects endpoints
@app.route('/api/video_projects/<string:id>', methods=['GET'])
@jwt_required()
def get_video_projects(id):
    current_user = get_jwt_identity()
    if id == 'all':
        # Get all video projects
        result = list(video_projects.find({'user_id': current_user}, {'_id': 0}))
        if not result:
            return jsonify({'message': 'No video projects found'}), 404
    else:
        # Get a specific video project
        result = video_projects.find_one({'user_id': current_user,'project_id': id}, {'_id': 0})
    return jsonify(result), 200

# Create Video project endpoint
@app.route('/api/video_projects', methods=['POST'])
@jwt_required()
def create_video_project():
    data = request.form
    project_id = data['project_id']
    current_user = get_jwt_identity()
    if video_projects.find_one({'user_id': current_user,'project_id': data['project_id']}):
        return jsonify({'message': 'Video project already exists'}), 400
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    # If user does not select file, browser also submits an empty part without filename
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        # Create directory if not available
        directory = os.path.dirname(f'uploads/{current_user}/{project_id}/')
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = secure_filename(file.filename)
        # Define upload folder
        UPLOAD_FOLDER = f'uploads/{current_user}/{project_id}/'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Generate thumbnail
        thumbnail_path = os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnail_' + filename+'.jpeg')
        generate_thumbnail(file_path, thumbnail_path)
        project_data = {
        'user_id': str(current_user),
        'project_id': data['project_id'],
        'title': data['title'],
        'description': data.get('description', ''),
        'creation_date': datetime.now(timezone.utc),
        'status': data['status'],
        'video_path': file_path,
        'thumbnail_path': thumbnail_path
    }
        # Insert the project
        inserted_project = video_projects.insert_one(project_data)
        return jsonify({'message': 'Video project created successfully', 'project_id': str(data['project_id'])}), 201

    return jsonify({'message': 'Invalid file type'}), 400

# Update Video project endpoint
@app.route('/api/video_projects/<string:id>', methods=['PUT'])
@jwt_required()
def update_video_project(id):
    current_user = get_jwt_identity()
    project = video_projects.find_one({'user_id': current_user,'project_id': id})
    if not project:
        return jsonify({'message': 'Video project not found'}), 404
    data = request.form
    update_data = {
        'user_id': str(current_user),
        'project_id': project["project_id"],
        'title': data.get('title', project['title']),
        'description': data.get('description', project['description']),
        'creation_date': data.get('creation_date', project['creation_date']),
        'status': data.get('status', project['status']),
    }
    # Update the project
    video_projects.update_one({'user_id': current_user,'project_id': id}, {'$set': update_data})
    return jsonify({'message': 'Video project updated successfully'}), 200

# Delete Video project endpoint
@app.route('/api/video_projects/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_video_project(id):
    current_user = get_jwt_identity()
    result = video_projects.delete_one({'user_id': current_user,'project_id': id})
    directory = os.path.dirname(f'uploads/{current_user}/{id}/')
    # Delete the directory
    if os.path.exists(directory):
            shutil.rmtree(directory)
    if result.deleted_count == 0:
        return jsonify({'message': 'Video project not found'}), 404
    return jsonify({'message': 'Video project deleted successfully'}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
