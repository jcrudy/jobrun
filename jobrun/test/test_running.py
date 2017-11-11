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
    
    @depend(a,b)
    def d():
        pass
    
    runner = Runner([b,c,d,a], lambda:'test_log')
    order = runner.run_order()
    orders = dict(zip(order, range(len(order))))
    assert orders[a] < orders[b]
    assert orders[a] < orders[d]
    assert orders[b] < orders[c]
    assert orders[b] < orders[d]

def test_run():
    def a():
        print 'a'
        return {'a':1}
    
    @depend(a)
    def b(a):
        print 'b'
        return {'b': 2}
    
    @depend(b)
    def c(b):
        print 'The quick brown fox'
    
    @depend(a,b)
    def d(a, b):
        warnings.warn('d')
        return {'d': a + b}
    
    runner = Runner([a,b,c,d], lambda:'test_log')
    result = runner.run()
    with open('test_log', 'r') as infile:
        log = infile.read()
        
    assert 'Running a' in log
    assert 'Running b' in log
    assert 'Running c' in log
    assert 'Running d' in log
    assert 'warning' in log
    assert 'The quick brown fox' in log
    assert_equal(result[d]['d'], 3)
    
    if os.path.exists('test_log'):
        os.remove('test_log')
    
    @depend(d)
    def e(d):
        raise ValueError('Hello')
    
    runner = Runner([a,b,c,d,e], lambda:'test_log')
    try:
        result = runner.run()
    except:
        pass
    with open('test_log', 'r') as infile:
        log = infile.read()
    assert 'Hello' in log
        
if __name__ == '__main__':
    # This code will run the test in this file.'
    import sys
    import nose
    module_name = sys.modules[__name__].__file__
 
    result = nose.run(argv=[sys.argv[0],
                            module_name,
                            '-s','-v'])