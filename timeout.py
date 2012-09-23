import sys
import signal
 
class TimeoutException(Exception): 
    pass 
 
def timeout(timeout_time, default):
    def timeout_function(f):
        def f2(*args):
            def timeout_handler(signum, frame):
                raise TimeoutException()
 
            old_handler = signal.signal(signal.SIGALRM, timeout_handler) 
            signal.alarm(timeout_time) # triger alarm in timeout_time seconds
            try: 
                retval = f()
            except TimeoutException:
                return default
            finally:
                signal.signal(signal.SIGALRM, old_handler) 
            signal.alarm(0)
            return retval
        return f2
    return timeout_function
