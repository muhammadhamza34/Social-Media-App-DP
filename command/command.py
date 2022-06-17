from abc import ABCMeta, abstractmethod
from models import *
from app import db

#Receiver
class PostClass:
    def like_post(self, user_id, post_id):
        post = Post.query.filter_by(id=post_id).first()
        user = User.query.filter_by(id=user_id).first()
        like = Like(liked_by=user, for_post=post)
        db.session.add(like)
        db.session.commit()
        
    def unlike_post(self, user_id, post_id):
        like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        db.session.delete(like)
        db.session.commit()

#ICommand Interface
class ICommand(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def execute():
        '''A static interface method'''

#Command Like Post
class LikePostCommand(ICommand):
    def __init__(self, post):
        self.post = post

    def execute(self, user_id, post_id):
        self.post.like_post(user_id, post_id)

#Command Unlike Post
class UnlikePostCommand(ICommand):
    def __init__(self, post):
        self.post = post

    def execute(self, user_id, post_id):
        self.post.unlike_post(user_id, post_id)

#Invoker
class Action:
    '''Invoker Class'''

    def __init__(self):
        self._commands = {}

    def register(self, command_name, command):
        self._commands[command_name] = command

    def execute(self, command_name, post_id, user_id):
        self._commands[command_name].execute(post_id, user_id)


