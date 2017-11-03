from abc import ABCMeta, abstractmethod
import os
from sklearn.externals import joblib
from jobrun.util import md5
import pickle


class UpdateTrigger(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def check(self):
        pass
    
    @abstractmethod
    def succeed(self, token):
        pass
    
    def __and__(self, other):
        if not isinstance(other, UpdateTrigger):
            return NotImplemented
        else:
            return AndTrigger(self, other)
        
    def __or__(self, other):
        if not isinstance(other, UpdateTrigger):
            return NotImplemented
        else:
            return OrTrigger(self, other)
        
    def __not__(self):
        return NotTrigger(self)

class DoNothingOnSuccessTrigger(UpdateTrigger):
    def succeed(self, token):
        pass

class TrueTrigger(DoNothingOnSuccessTrigger):
    def check(self):
        return True, None

class FalseTrigger(DoNothingOnSuccessTrigger):
    def check(self):
        return False, None

class TwoArgTrigger(UpdateTrigger):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def succeed(self, token):
        left_token, right_token = token
        if left_token is not None:
            self.left.succeed(left_token)
        if right_token is not None:
            self.right.succeed(right_token)
        
class AndTrigger(TwoArgTrigger):
    def check(self):
        left_result, left_token = self.left.check()
        right_result, right_token = self.right.check()
        return left_result and right_result, (left_token, right_token)

class OrTrigger(TwoArgTrigger):
    def check(self):
        left_result, left_token = self.left.check()
        right_result, right_token = self.right.check()
        return left_result or right_result, (left_token, right_token)
    
class NotTrigger(UpdateTrigger):
    def __init__(self, arg):
        self.arg = arg
    
    def check(self):
        result, token = self.arg.check()
        return not result, token
    
    def succeed(self, token):
        self.arg.succeed(token)


class ModifiedBase(UpdateTrigger):
    def check(self):
        stamp = self.get_stamp()
        try:
            if os.path.exists(self.cache_filename):
                with open(self.cache_filename, 'r') as infile:
                    old_stamp = infile.read()
                if stamp == old_stamp:
                    return False, None
        except:
            pass
        return True, stamp
    
    def succeed(self, token):
        with open(self.cache_filename, 'w') as outfile:
            outfile.write(token)
    
    @abstractmethod
    def get_stamp(self):
        pass

class ObjectModified(ModifiedBase):
    def __init__(self, obj, cache_filename):
        self.obj = obj
        self.cache_filename = cache_filename
        
    def get_stamp(self):
        return pickle.dumps(self.obj)
    
class FileModifiedBase(ModifiedBase):
    def __init__(self, filename, cache_filename=None):
        self.filename = filename
        if cache_filename is None:
            self.cache_filename = filename + ('.cache.%s.pkl' % self.__class__.__name__)
        else:
            self.cache_filename = cache_filename

class TimestampModified(FileModifiedBase):
    def get_stamp(self):
        return str(os.path.getmtime(self.filename))

class ChecksumModified(FileModifiedBase):
    def get_stamp(self):
        return md5(self.filename)
    
def FileModified(filename, cache_filename=None):
    return TimestampModified(filename, cache_filename) | ChecksumModified(filename, cache_filename)

def update_when(trigger, cache_filename=None, cache_filedir=None):
    def _update_when(fun):
        extension = '.function_cache.pkl'
        if cache_filename is None:
            filename = fun.__name__ + extension
        else:
            filename = cache_filename
        if cache_filedir is not None:
            filename = os.path.join(cache_filedir)
        def _run(*args, **kwargs):
            check, token = trigger.check()
            if check:
                result = fun(*args, **kwargs)
                joblib.dump(result, filename)
                trigger.succeed(token)
            else:
                result = joblib.load(filename)
            return result
        _run.__name__ = fun.__name__
        return _run
    return _update_when
