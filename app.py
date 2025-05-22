import config
import datetime

from flask import request, jsonify
from flask_restful import Api
from flasgger import Swagger
from config import db
from models import Users, Application, Video

app = config.app
api = Api(app)

app.config['SWAGGER'] = {
    'title': 'EyeDTrack REST API',
    'uiversion': 3
}
swagger = Swagger(app)

@app.route('/create_user', methods=['POST'])
def create_user():
    """
    Create a new user account
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Users
          required:
            - first_name
            - last_name
            - contact_number
            - user_birthday
            - password
            - email_address
          properties:
            first_name:
              type: string
              description: First Name of user
            last_name:
              type: string
              description: Last Name of user
            contact_number:
              type: string
              description: Contact Number of user
            user_birthday:
              type: string
              format: date
              description: Birthday in YYYY-MM-DD format
            password:
              type: string
              description: Password for application login
            email_address:
              type: string
              description: Email Address of user
    responses:
      201:
        description: Post created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact_number = data.get('contact_number')
    user_birthday = data.get('user_birthday')
    password = data.get('password')
    email_address = data.get('email_address')

    if not email_address or not first_name:
        return jsonify({'error': 'Missing first name or email address'}), 400

    # Convert birthday string to date
    birthday_date = None
    if user_birthday:
        try:
            birthday_date = datetime.date.fromisoformat(user_birthday)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    new_user = Users(first_name=first_name,
                     last_name=last_name,
                     contact_number=contact_number,
                     user_birthday=birthday_date,
                     password=password,
                     email_address=email_address)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "User ID": new_user.user_id,
        "First Name": new_user.first_name,
        "Last Name": new_user.last_name,
        "Email Address": new_user.email_address
    }), 201

@app.route('/create_app', methods=['POST'])
def create_app():
    """
    Create a new app
    ---
    tags:
      - Applications
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Applications
          required:
            - behavior_category
            - behavior_output
            - algo_mar
            - algo_pitch
            - algo_yaw
            - algo_roll
            - behavior_confidence
            - timestamp
            - video_id
          properties:
            behavior_category:
              type: string
              description: Type of detected behavior
            behavior_output:
              type: string
              description: Specific behavior recognized
            algo_mar:
              type: string
              description: Mouth Aspect Ratio
            algo_pitch:
              type: string
              description: Pitch angle of the head movement
            algo_yaw:
              type: string
              description: Yaw angle of the head movement
            algo_roll:
              type: string
              description: Roll angle of the head movement
            behavior_confidence:
              type: string
              description: Confidence score of the detected behavior
            timestamp:
              type: string
              description: Time at which the behavior data was recorded
            video_id:
              type: string
              description: Unique identifier of the video session
    responses:
      201:
        description: Post created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    behavior_category = data.get('behavior_category')
    behavior_output = data.get('behavior_output')
    algo_mar = data.get('algo_mar')
    algo_pitch = data.get('algo_pitch')
    algo_yaw = data.get('algo_yaw')
    algo_roll = data.get('algo_roll')
    behavior_confidence = data.get('behavior_confidence')
    timestamp = data.get('timestamp')
    video_id = data.get('video_id')

    if not behavior_category or not behavior_output:
        return jsonify({'error': 'Missing behavior category or output'}), 400

    new_app = Application(behavior_category=behavior_category,
                     behavior_output=behavior_output,
                     algo_mar=algo_mar,
                     algo_pitch=algo_pitch,
                     algo_yaw=algo_yaw,
                     algo_roll=algo_roll,
                     behavior_confidence=behavior_confidence,
                     timestamp=timestamp,
                     video_id=video_id
                     )
    db.session.add(new_app)
    db.session.commit()

    return jsonify({
        "Behavior Category": new_app.behavior_category,
        "Behavior Output": new_app.behavior_output,
    }), 201

@app.route('/create_video', methods=['POST'])
def create_video():
    """
    Create a new video
    ---
    tags:
      - Videos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Videos
          required:
            - file_path
            - file_name
            - timestamp
            - user_id
          properties:
            file_path:
              type: string
              description: File path indicating the location of the video file
            file_name:
              type: string
              description: Name of the video file without the path
            timestamp:
              type: string
              description: Time at which the behavior data was recorded
            user_id:
              type: string
              description: Identifier of the user
    responses:
      201:
        description: Post created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()
    file_path = data.get('file_path')
    file_name = data.get('file_name')
    timestamp = data.get('timestamp')
    user_id = data.get('user_id')

    if not file_name:
        return jsonify({'error': 'Missing File Name'}), 400

    new_vid = Video(file_path=file_path,
                     file_name=file_name,
                     timestamp=timestamp,
                     user_id=user_id
                     )
    db.session.add(new_vid)
    db.session.commit()

    return jsonify({
        "File name": new_vid.file_name,
    }), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Get user by ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID of the user to retrieve
    responses:
      200:
        description: A single user object
      404:
        description: User not found
    """
    user = Users.query.get(user_id)
    if user:
        return jsonify({
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email_address": user.email_address,
            "contact_number": user.contact_number,
            "user_birthday": user.user_birthday.isoformat() if user.user_birthday else None
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/app/<int:app_id>', methods=['GET'])
def get_app_by_id(app_id):
    """
    Get app by ID
    ---
    tags:
      - Applications
    parameters:
      - name: app_id
        in: path
        type: integer
        required: true
        description: ID of the app to retrieve
    responses:
      200:
        description: A single app object
      404:
        description: User not found
    """
    app = Application.query.get(app_id)
    if app:
        return jsonify({
            "app_id": app.app_id,
            "behavior_category": app.behavior_category,
            "behavior_output": app.behavior_output,
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/vid/<int:vid_id>', methods=['GET'])
def get_vid_by_id(vid_id):
    """
    Get vid by ID
    ---
    tags:
      - Videos
    parameters:
      - name: vid_id
        in: path
        type: integer
        required: true
        description: ID of the vid to retrieve
    responses:
      200:
        description: A single vid object
      404:
        description: User not found
    """
    vid = Video.query.get(vid_id)
    if vid:
        return jsonify({
            "vid_id": vid.vid_id,
            "file_name": vid.file_name,
            "timestamp": vid.timestamp,
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)