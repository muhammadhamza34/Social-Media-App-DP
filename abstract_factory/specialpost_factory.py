from abc import ABCMeta, abstractmethod
from models import *
from app import app
import os

class ISpecialPost(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_post():
        '''Special Post Interface'''

class SpecialPost(ISpecialPost):
    def __init__(self, text, owner, pic):
        self.text = text
        self.owner = owner
        self.post = Post(post_content=text, post_owner=owner)
        
        file_name = f'{self.post.id}-photo.{(pic.filename).split(".")[-1]}' 
        path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        pic.save(path)

        self.photo = Photo(photo_name=file_name, of_post=self.post)

    def get_post(self):
        return (self.post, self.photo)

class SpecialPostFactory():
    @staticmethod
    def get_special_post(text, owner, pic):
        return SpecialPost(text, owner, pic)