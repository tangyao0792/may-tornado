import sys
import time

def _get_caller_info():
    '''Return caller's file name, function name and line number.'''
    function_name = sys._getframe().f_back.f_back.f_code.co_name
    line_number = sys._getframe().f_back.f_back.f_lineno
    filename = sys._getframe().f_back.f_back.f_code.co_filename
    return filename, function_name, line_number

def log(log_info):
    filename, function_name, line_number = _get_caller_info()
    sys.stderr.write('%s\t%s\t[%s, %s, %s]\n' % (time.ctime(), log_info, filename, function_name, line_number))
    sys.stderr.flush()


if __name__ == '__main__':
    def func_haha():
        log('haah')
    
    def func_papa():
        log('paap')

    def test():
        log('test')
    func_papa()
    func_haha()
    time.sleep(1)
    test()
