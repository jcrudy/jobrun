from jobrun.caching import TimestampModified, update_when, FileModified,\
    ChecksumModified, InfileOutfileTimestamp, ObjectModified
import os
from nose.tools import assert_equal
import time

def test_update_when_file_modified():
    runcount = [0]
    @update_when(FileModified('test_data'))
    def read_the_data():
        runcount[0] = runcount[0] + 1
        with open('test_data', 'r') as infile:
            data = infile.read()
        return data
    
    # Create test file
    assert not os.path.exists('test_data')
    try:
        with open('test_data', 'w') as outfile:
            outfile.write('a')
        
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        time.sleep(1)
        with open('test_data', 'w') as outfile:
            outfile.write('a')
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 2)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 2)
        with open('test_data', 'w') as outfile:
            outfile.write('b')
        assert_equal(read_the_data(), 'b')
        assert_equal(runcount[0], 3)
        assert_equal(read_the_data(), 'b')
        assert_equal(runcount[0], 3)
    finally:
        if os.path.exists('test_data'):
            os.remove('test_data')
        if os.path.exists('test_data.cache.TimestampModified.pkl'):
            os.remove('test_data.cache.TimestampModified.pkl')
        if os.path.exists('test_data.cache.ChecksumModified.pkl'):
            os.remove('test_data.cache.ChecksumModified.pkl')
        if os.path.exists('read_the_data.function_cache.pkl'):
            os.remove('read_the_data.function_cache.pkl')

def test_update_when_timestamp_modified():
    runcount = [0]
    @update_when(TimestampModified('test_data'))
    def read_the_data():
        runcount[0] = runcount[0] + 1
        with open('test_data', 'r') as infile:
            data = infile.read()
        return data
    
    # Create test file
    assert not os.path.exists('test_data')
    try:
        with open('test_data', 'w') as outfile:
            outfile.write('a')
        
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        time.sleep(1)
        with open('test_data', 'w') as outfile:
            outfile.write('a')
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 2)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 2)
        time.sleep(1)
        with open('test_data', 'w') as outfile:
            outfile.write('b')
        assert_equal(read_the_data(), 'b')
        assert_equal(runcount[0], 3)
        assert_equal(read_the_data(), 'b')
        assert_equal(runcount[0], 3)
    finally:
        if os.path.exists('test_data'):
            os.remove('test_data')
        if os.path.exists('test_data.cache.TimestampModified.pkl'):
            os.remove('test_data.cache.TimestampModified.pkl')
        if os.path.exists('test_data.cache.ChecksumModified.pkl'):
            os.remove('test_data.cache.ChecksumModified.pkl')
        if os.path.exists('read_the_data.function_cache.pkl'):
            os.remove('read_the_data.function_cache.pkl')

def test_update_when_checksum_modified():
    runcount = [0]
    @update_when(ChecksumModified('test_data'))
    def read_the_data():
        runcount[0] = runcount[0] + 1
        with open('test_data', 'r') as infile:
            data = infile.read()
        return data
    
    # Create test file
    assert not os.path.exists('test_data')
    try:
        with open('test_data', 'w') as outfile:
            outfile.write('a')
        
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        time.sleep(1)
        with open('test_data', 'w') as outfile:
            outfile.write('a')
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        with open('test_data', 'w') as outfile:
            outfile.write('b')
        assert_equal(read_the_data(), 'b')
        assert_equal(runcount[0], 2)
        assert_equal(read_the_data(), 'b')
        assert_equal(runcount[0], 2)
    finally:
        if os.path.exists('test_data'):
            os.remove('test_data')
        if os.path.exists('test_data.cache.TimestampModified.pkl'):
            os.remove('test_data.cache.TimestampModified.pkl')
        if os.path.exists('test_data.cache.ChecksumModified.pkl'):
            os.remove('test_data.cache.ChecksumModified.pkl')
        if os.path.exists('read_the_data.function_cache.pkl'):
            os.remove('read_the_data.function_cache.pkl')

def test_infile_outfile_timestamp():
    runcount = [0]
    @update_when(InfileOutfileTimestamp(['test_infile'], ['test_outfile']))
    def read_the_data():
        runcount[0] = runcount[0] + 1
        with open('test_infile', 'r') as infile:
            data = infile.read()
        with open('test_outfile', 'w') as outfile:
            outfile.write(data)
        return data
    
    # Create test file
    assert not os.path.exists('test_infile')
    try:
        with open('test_infile', 'w') as outfile:
            outfile.write('a')
        time.sleep(1)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 1)
        time.sleep(1)
        with open('test_infile', 'w') as outfile:
            outfile.write('a')
        time.sleep(1)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 2)
        assert_equal(read_the_data(), 'a')
        assert_equal(runcount[0], 2)
        
        with open('test_infile', 'w') as outfile:
            outfile.write('b')
        time.sleep(1)
        assert_equal(read_the_data(), 'b')
        assert_equal(runcount[0], 3)
        assert_equal(read_the_data(), 'b')
        assert_equal(runcount[0], 3)
    finally:
        if os.path.exists('test_infile'):
            os.remove('test_infile')
        if os.path.exists('test_outfile'):
            os.remove('test_outfile')
        if os.path.exists('read_the_data.function_cache.pkl'):
            os.remove('read_the_data.function_cache.pkl')


def test_object_modified():
    runcount = [0]
    @update_when(ObjectModified((1,2), 'test_cache'))
    def do_stuff():
        runcount[0] += 1
    
    try:
        do_stuff()
        assert_equal(runcount[0], 1)
        do_stuff()
        assert_equal(runcount[0], 1)
        
        @update_when(ObjectModified((1,2), 'test_cache'))
        def do_stuff():
            runcount[0] += 1
        
        do_stuff()
        assert_equal(runcount[0], 1)
        
        @update_when(ObjectModified((1,3), 'test_cache'))
        def do_stuff():
            runcount[0] += 1
        
        do_stuff()
        assert_equal(runcount[0], 2)
        do_stuff()
        assert_equal(runcount[0], 2)
        
    finally:
        if os.path.exists('test_cache'):
            os.remove('test_cache')
        if os.path.exists('do_stuff.function_cache.pkl'):
            os.remove('do_stuff.function_cache.pkl')
        
if __name__ == '__main__':
    # This code will run the test in this file.'
    import sys
    import nose
    module_name = sys.modules[__name__].__file__

    result = nose.run(argv=[sys.argv[0],
                            module_name,
                            '-s','-v'])