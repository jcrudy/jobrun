import sys
import logging

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
    
    def flush(self):
        [h.flush() for h in self.logger.handlers]

# class LoggerWriter:
#     def __init__(self, logger, level):
#         # self.level is really like using log.debug(message)
#         # at least in my case
#         self.logger = logger
#         self.level = level
# 
#     def write(self, message):
#         # if statement reduces the amount of newlines that are
#         # printed to the logger
#         if message != '\n':
#             self.level(message)
#         self.flush()
# 
#     def flush(self):
#         [h.flush() for h in self.logger.handlers]

class LogCapture(object):
    def __init__(self, filename, suppress_printing=True):
        self.filename = filename
        self.suppress_printing = suppress_printing
    
    def __enter__(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
#         logging.basicConfig(filename=self.filename, level=logging.DEBUG,
#                             format='%(asctime)s %(levelname)-8s %(message)s',
#                             datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler(self.filename)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(0)
        self.log = logging.getLogger()
        self.log.setLevel(0)
        self.log.addHandler(handler)
        if not self.suppress_printing:
            self.log.addHandler(logging.StreamHandler(sys.stdout))
        
        sys.stdout = StreamToLogger(self.log)
        sys.stderr = StreamToLogger(self.log)
        return self.log
    
    def exception(self, *args, **kwargs):
        return self.log.exception(*args, **kwargs)
    
    def info(self, *args, **kwargs):
        return self.log.info(*args, **kwargs)
    
    def warning(self, *args, **kwargs):
        return self.log.warning(*args, **kwargs)
    
    def error(self, *args, **kwargs):
        return self.log.error(*args, **kwargs)
    
    def __exit__(self, *args):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        

