from jobrun.running import depend, Runner
from nose.tools import assert_equal
import warnings
import os


def test_depend():
    def a():
        pass
    
    @depend(a)
    def b():
        pass

    assert_equal(b.inputs, (a,))

def test_run_order():
    def a():
        pass
    
    @depend(a)
    def b():
        pass
    
    @depend(b)
    def c():
        pass
    
    @depend(a)
    def d():
        pass
    
    runner = Runner([a,b,c,d], lambda:'test_log')
    order = runner.run_order()
    orders = dict(zip(order, range(len(order))))
    assert orders[a] < orders[b]
    assert orders[a] < orders[d]
    assert orders[b] < orders[c]

def test_run():
    def a():
        print 'a'
    
    @depend(a)
    def b():
        print 'b'
    
    @depend(b)
    def c():
        print 'c'
    
    @depend(a)
    def d():
        warnings.warn('d')
    
    runner = Runner([a,b,c,d], lambda:'test_log')
    runner.run()
    with open('test_log', 'r') as infile:
        log = infile.read()
        
    assert 'Running a' in log
    assert 'Running b' in log
    assert 'Running c' in log
    assert 'Running d' in log
    
    if os.path.exists('test_log'):
        os.remove('test_log')
    

        
if __name__ == '__main__':
    # This code will run the test in this file.'
    import sys
    import nose
    module_name = sys.modules[__name__].__file__

    result = nose.run(argv=[sys.argv[0],
                            module_name,
                            '-s','-v'])