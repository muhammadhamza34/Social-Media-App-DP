'''
Facade Pattern
'''

from models import *
from app import db

class RecRequest:
    @staticmethod
    def add_entry(user_id, to_id):
        to_user = User.query.filter_by(id=to_id).first()
        recdRequest = ReceivedRequest(requested_to=to_user, requested_by=user_id)
        db.session.add(recdRequest)
        db.session.commit()

    @staticmethod
    def remove_entry(request_id, to_id, user_id=None):
        if user_id:
            recd_req = ReceivedRequest.query.filter_by(requested_by=user_id, user_id=to_id).first()
            db.session.delete(recd_req)
            db.session.commit()
        else:
            recd_req = ReceivedRequest.query.filter_by(id=request_id).first()
            db.session.delete(recd_req)
            db.session.commit()

class RequestSent:
    @staticmethod
    def add_entry(user_id, to_id):
        current_user = User.query.filter_by(id=user_id).first()
        sentRequest = SentRequest(requested_by=current_user, requested_to=to_id)
        db.session.add(sentRequest)
        db.session.commit()

    @staticmethod
    def remove_entry(request_id, by_id, user_id=None):
        if user_id:
            sent_req = SentRequest.query.filter_by(requested_to=user_id, user_id=by_id).first()
            db.session.delete(sent_req)
            db.session.commit()
        else:
            sent_req = SentRequest.query.filter_by(id=request_id).first()
            db.session.delete(sent_req)
            db.session.commit()

class AddFriend:
    @staticmethod
    def add_friend(user_id, by_id):
        current_user = User.query.filter_by(id=user_id).first()
        new_friend = Friend(friend_of=current_user, friend_id=by_id)
        db.session.add(new_friend)
        db.session.commit()
        other_user = User.query.filter_by(id=by_id).first()
        again_friend = Friend(friend_of=other_user, friend_id=user_id)
        db.session.add(again_friend)
        db.session.commit()

#Facade Class
class Facade():
    def __init__(self):
        self.rec_req = RecRequest()
        self.send_req = RequestSent()
        self.add_friend = AddFriend()

    def send_request(self, user_id, friend_id):
        self.send_req.add_entry(user_id, friend_id)
        self.rec_req.add_entry(user_id, friend_id)

    def cancel_request(self, user_id, request_id):
        sent_req = SentRequest.query.filter_by(id=request_id).first()
        to_id = sent_req.requested_to
        db.session.commit()
        self.send_req.remove_entry(request_id, to_id)
        self.rec_req.remove_entry(request_id, to_id, user_id)

    def accept_request(self, user_id, request_id):
        recd_req = ReceivedRequest.query.filter_by(id=request_id).first()
        by_id = recd_req.requested_by
        db.session.commit()
        self.add_friend.add_friend(user_id, by_id)
        self.rec_req.remove_entry(request_id, by_id)
        self.send_req.remove_entry(request_id, by_id, user_id)

    def remove_request(self, user_id, request_id):
        recd_req = ReceivedRequest.query.filter_by(id=request_id).first()
        by_id = recd_req.requested_by
        self.rec_req.remove_entry(request_id, by_id)
        self.send_req.remove_entry(request_id, by_id, user_id)

    
