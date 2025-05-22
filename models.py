from config import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Users(db.Model):
    __tablename__ = "user_profile"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(500))
    last_name = db.Column(db.String(500))
    contact_number = db.Column(db.String(11))
    user_birthday = db.Column(db.Date)
    password = db.Column(db.String(20))
    email_address = db.Column(db.String(500))

class UsersSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        sqla_session = db.session

users_schema = UsersSchema()
user_schema = UsersSchema(many=True)

class Application(db.Model):
    __tablename__ = "app_tbl"
    app_id = db.Column(db.Integer, primary_key=True)
    behavior_category = db.Column(db.String(100))
    behavior_output = db.Column(db.String(20))
    algo_mar = db.Column(db.String(100))
    algo_pitch = db.Column(db.String(100))
    algo_yaw = db.Column(db.String(100))
    algo_roll = db.Column(db.String(100))
    behavior_confidence = db.Column(db.String(50))
    timestamp = db.Column(db.Date)
    video_id = db.Column(db.Integer)

class ApplicationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Application
        load_instance = True
        sqla_session = db.session

Application_schema = ApplicationSchema()
app_schema = ApplicationSchema(many=True)

class Video(db.Model):
    __tablename__ = "video_table"
    video_id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(500))
    file_name = db.Column(db.String(500))
    timestamp = db.Column(db.Date)
    user_id = db.Column(db.Integer)

class VideoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Video
        load_instance = True
        sqla_session = db.session

Video_schema = VideoSchema()
vid_schema = VideoSchema(many=True)
