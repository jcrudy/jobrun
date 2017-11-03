from jobrun.log_capturing import LogCapture
import os
import warnings

def test_log_capturing():
    try:
        with LogCapture('log_file') as log:
            print 'The quick brown fox'
            warnings.warn('jumped over')
            log.error('the lazy dog')
            
        with open('log_file', 'r') as infile:
            log = infile.read()
        assert 'The quick brown fox' in log
        assert 'jumped over' in log
        assert 'the lazy dog' in log
    finally:
        if os.path.exists('log_file'):
            os.remove('log_file')
    

if __name__ == '__main__':
    # This code will run the test in this file.'
    import sys
    import nose
    module_name = sys.modules[__name__].__file__

    result = nose.run(argv=[sys.argv[0],
                            module_name,
                            '-s','-v'])