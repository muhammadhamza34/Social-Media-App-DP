#Singleton Design Pattern
from models import *

class CurrentUser:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, session):
        if cls._instance is None:
            user_id = session['user_id']
            user = User.query.filter_by(id=user_id).first()
            cls._instance = cls.__new__(cls)
            cls._instance.user = user
        return cls._instance

    @classmethod
    def remove(self):
        if self._instance != None:
            self._instance = None

    @classmethod
    def get_timeline_posts(self):
        user = self._instance.user
        user_id = user.id
        ids_included = [friend.friend_id for friend in user.friends]
        ids_included += [user.id]
        posts = Post.query.filter(Post.user_id.in_(ids_included)).order_by(Post.id.desc())
        return posts

    @classmethod
    def get_sent_requests(self):
        user = self._instance.user
        sent_requests_found = user.sent_requests
        sent_requests = []
        for req in sent_requests_found:
            friend_id = req.requested_to
            friend = User.query.filter_by(id=friend_id).first()
            sent_requests.append([req, friend])
        return sent_requests

    @classmethod
    def get_received_requests(self):
        user = self._instance.user
        recd_requests_found = user.recd_requests
        recd_requests = []
        for req in recd_requests_found:
            friend_id = req.requested_by
            friend = User.query.filter_by(id=friend_id).first()
            recd_requests.append([req, friend])
        return recd_requests

    @classmethod
    def get_own_posts(self):
        user = self._instance.user
        user_id = user.id
        posts = user.posts.order_by(Post.id.desc())
        return posts

    @classmethod
    def get_new_friends(self):
        user = self._instance.user
        user_id = user.id
        ids_excluded = [request.requested_to for request in user.sent_requests]
        ids_excluded += [request.requested_by for request in user.recd_requests]
        ids_excluded += [friend.friend_id for friend in user.friends]
        ids_excluded += [user_id]
        users_found = User.query.filter(User.id.notin_(ids_excluded))
        return users_found

    @classmethod
    def get_friends(self):
        user = self._instance.user
        user_id = user.id
        friends = []
        for friend_found in user.friends:
            user_friend = User.query.filter_by(id=friend_found.friend_id).first()
            friends.append(user_friend)
        return friends