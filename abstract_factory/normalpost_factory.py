from abc import ABCMeta, abstractmethod
from models import *

class INormalPost(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_post():
        '''Normal Post Interface'''

class NormalPost(INormalPost):
    def __init__(self, text, owner):
        self.text = text
        self.owner = owner
        self.post = Post(post_content=text, post_owner=owner)

    def get_post(self):
        return self.post

class NormalPostFactory():
    @staticmethod
    def get_normal_post(text, owner):
        return NormalPost(text, owner)


