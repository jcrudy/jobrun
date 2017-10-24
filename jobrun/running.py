import networkx
from jobrun.log_capturing import LogCapture
import time
from toolz.dicttoolz import merge
from jobrun.util import none_to_empty_dict

def depend(*dependencies):
    def _depend(fun):
        fun.inputs = dependencies
        return fun
    return _depend

class Runner(object):
    '''
    jobs: and iterable of callables.  Each callable should have an 'inputs' attribute.  The 
          __name__ attributes are used to refer to the jobs in the log file.  All output to stdout
          and stderr is redirected to the log file.
    logfilenamer: Callable that returns the log file name, or a str that is it.
    '''
    def __init__(self, jobs, logfilenamer):
        self.jobs = jobs
        self.logfilenamer = logfilenamer
    
    def create_graph(self):
        graph = networkx.DiGraph()
        for job in self.jobs:
            graph.add_node(job)
        for job in self.jobs:
            if hasattr(job, 'inputs'):
                for inp in job.inputs:
                    graph.add_edge(inp, job)
        return graph
    
    def run_order(self):
        graph = self.create_graph()
        jobs = networkx.topological_sort(graph)
        return jobs
    
    def run(self):
        logfilename = self.logfilenamer() if not isinstance(self.logfilenamer, basestring) else self.logfilenamer
        with LogCapture(logfilename) as log:
            t0 = time.time()
            jobs = self.run_order()
            results = {}
            success = False
            for job in jobs:
                name = job.__name__
                log.info('Running %s' % name)
                t1 = time.time()
                try:
                    results[job] = none_to_empty_dict(job(**merge(*[results[k] for k in (job.inputs if hasattr(job, 'inputs') else [])])))
                    success = True
                except:
                    log.info('Job %s failed.' % name)
                    log.exception('')
                    success = False
                t2 = time.time()
                if success:
                    log.info('Job %s completed in %f seconds.' % (name, t2 - t1))
                else:
                    log.info('Job %s failed in %f seconds.' % (name, t2 - t1))
                    break
            t3 = time.time()
            log.info('Completed all jobs in %f seconds.' % (t3 - t0))
        return results
