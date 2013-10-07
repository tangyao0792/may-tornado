import sys
import time

NOTICE = 0
ERROR = 1
WARNING =2

def _get_caller_info():
    '''Return caller's file name, function name and line number.'''
    function_name = sys._getframe().f_back.f_back.f_code.co_name
    line_number = sys._getframe().f_back.f_back.f_lineno
    filename = sys._getframe().f_back.f_back.f_code.co_filename.split('/')[-1]
    return filename, function_name, line_number

def log(log_info, flag=NOTICE):
    buf = ''
    if flag == NOTICE:      # green font
        buf += '\033[1;32;40m'
        buf += 'NOTICE'
        buf += '\033[0m'
    elif flag == ERROR:     # red
        buf += '\033[1;31;40m'
        buf += 'ERROR'
        buf += '\033[0m'
    else:                   # yellow
        buf += '\033[1;33;40m'
        buf += 'WARNING'
        buf += '\033[0m'
        
    filename, function_name, line_number = _get_caller_info()
    buf += '\t%s\t%s\t[%s, %s, %s]\n' % (time.ctime(), log_info, filename, function_name, line_number)
    sys.stderr.write(buf)
    sys.stderr.flush()


if __name__ == '__main__':
    def func_haha():
        log('haah', WARNING)
    
    def func_papa():
        log('paap', ERROR)

    def test():
        log('test')
    func_papa()
    func_haha()
    time.sleep(1)
    test()
