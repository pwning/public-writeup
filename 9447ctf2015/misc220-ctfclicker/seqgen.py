import ctypes
import scrypt
import sys
import time
import multiprocessing
from itertools import product
import struct
import signal

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def scrypt_break(prefix):
    start = time.time()
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for cand in product(alphabet, repeat=17):
        test = prefix + ''.join(cand)
        if scrypt.hash(test, 'NaCl', 2048, 8, 16, 20).startswith('\xff'):
            end = time.time()
            print >> sys.stderr, "DEBUG: time elapsed %.3f seconds; %s, %s" % (end - start, prefix.encode('hex'), test.encode('hex'))
            return test

if __name__ == '__main__':
    delay = int(sys.argv[1])
    ts = (int(time.time()) + delay) >> 4
    print "precomputing %d seconds in advance" % delay
    print "ts range %d-%d" % (ts*16, ts*16+15)
    print "datetime range %s  -  %s" % (time.ctime(ts*16), time.ctime(ts*16+15))

    libc = ctypes.CDLL('libc.so.6')
    libc.srand(ts)

    seq = [libc.rand() for i in xrange(100)]
    sseq = [struct.pack('<I', x) for x in seq]

    pool = multiprocessing.Pool(initializer=init_worker)
    try:
        result = pool.map(scrypt_break, sseq)
    except KeyboardInterrupt:
        print "Caught KeyboardInterrupt; exiting"
        pool.terminate()
        pool.join()
        exit()

    for i, j in zip(sseq, result):
        print i.encode('hex'), j.encode('hex')
