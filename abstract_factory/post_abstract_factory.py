from abc import ABCMeta, abstractmethod
from .normalpost_factory import NormalPostFactory
from .specialpost_factory import SpecialPostFactory

class IPostFactory(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_post(post_type):
        '''The static post factory interface method'''

class PostFactory(IPostFactory):
    @staticmethod
    def get_post(post_type, text, owner, pic):
        try:
            if post_type == 'normal':
                return NormalPostFactory.get_normal_post(text, owner)
            elif post_type == 'special':
                return SpecialPostFactory.get_special_post(text, owner, pic)
            raise AssertionError('Could not find the post type')
        except AssertionError as _e:
            print(e)
        return None

