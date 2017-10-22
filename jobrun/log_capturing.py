import sys
import logging


class LoggerWriter:
    def __init__(self, level):
        # self.level is really like using log.debug(message)
        # at least in my case
        self.level = level

    def write(self, message):
        # if statement reduces the amount of newlines that are
        # printed to the logger
        if message != '\n':
            self.level(message)

    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to. Not sure if simply 'printing'
        # sys.stderr is the correct way to do it, but it seemed
        # to work properly for me.
        self.level(sys.stderr)

class LogCapture(object):
    def __init__(self, filename):
        self.filename = filename
    
    def __enter__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
#         logging.basicConfig(filename=self.filename, level=logging.DEBUG,
#                             format='%(asctime)s %(levelname)-8s %(message)s',
#                             datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler(self.filename)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.log = logging.getLogger()
        self.log.addHandler(handler)
        
        sys.stdout = LoggerWriter(self.log.info)
        sys.stderr = LoggerWriter(self.log.warning)
        return self.log
    
    def exception(self):
        return self.log.exception()
    
    def info(self, *args, **kwargs):
        return self.log.info(*args, **kwargs)
    
    def warning(self, *args, **kwargs):
        return self.log.warning(*args, **kwargs)
    
    def error(self, *args, **kwargs):
        return self.log.error(*args, **kwargs)
    
    def __exit__(self, *args):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        

