PIPE_NAME = '/tmp/mt_waker_pipe'

if __name__ == '__main__':
    f = open(PIPE_NAME, 'w')
    f.write('bye')
    f.close()
