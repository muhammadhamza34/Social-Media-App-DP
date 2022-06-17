from app import db
from datetime import datetime

# Models
#Users Table
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    gender = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    profile_picture = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='post_owner', cascade="all,delete", lazy='dynamic')
    likes = db.relationship('Like', backref='liked_by', cascade="all,delete", lazy='dynamic')
    friends = db.relationship('Friend', backref='friend_of', cascade="all,delete", lazy='dynamic')
    sent_requests = db.relationship('SentRequest', backref='requested_by', cascade="all,delete", lazy='dynamic')
    recd_requests = db.relationship('ReceivedRequest', backref='requested_to', cascade="all,delete", lazy='dynamic')

#Posts Table
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.Text)
    post_timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_photos = db.relationship('Photo', backref='of_post', cascade="all,delete", lazy='dynamic')
    post_likes = db.relationship('Like', backref='for_post', cascade="all,delete", lazy='dynamic')

#Likes Table
class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

#Photos Table
class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    photo_name = db.Column(db.String(), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

#Friends Table
class Friend(db.Model):
    __tablename__ = 'friend'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, nullable=False)

#Sent Requests Table
class SentRequest(db.Model):
    __tablename__ = 'sentrequest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requested_to = db.Column(db.Integer, nullable=False)

#Received Requests Table
class ReceivedRequest(db.Model):
    __tablename__ = 'receivedrequest'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requested_by = db.Column(db.Integer, nullable=False)