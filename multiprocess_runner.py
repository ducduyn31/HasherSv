import multiprocessing
import os
import time
from contextlib import closing
from optparse import OptionParser

import hash512_sep
import sampling_n_hash_sep
from logger_2 import log_to_db

parser = OptionParser()


def combine_result(t1, t2):
    t1.get()


if __name__ == '__main__':
    start = time.time()
    parser.add_option('-i', '--input', help='File List of File to hash')
    parser.add_option('-n', '--samples', default=1, help='# of samples')
    parser.add_option('-b', '--blocksize', default=128, help='Sample block size')
    parser.add_option('-q', action="store_true", dest="quite")
    parser.add_option('-r', action="store_true", dest="remove")
    (options, args) = parser.parse_args()
    file_list = options.input
    block_size = int(options.blocksize)
    n = int(options.samples)
    isQuite = bool(options.quite)
    willRemove = bool(options.remove)

    with open(file_list, 'r') as fl:
        files = fl.read().splitlines()

    processes = []

    with closing(multiprocessing.Pool(processes=multiprocessing.cpu_count())) as pool:

        for f in files:
            a = pool.apply_async(hash512_sep.main, [f])
            b = pool.apply_async(sampling_n_hash_sep.main, [f, block_size, n])
            full_hash_time, full_hash_hex = a.get()
            tactical_io_time, tactical_hash_time, tactical_hash_hex = b.get()
            c = pool.apply_async(log_to_db, [f, full_hash_hex, n, tactical_hash_hex, os.path.getsize(f), full_hash_time,
                                             tactical_hash_time, tactical_io_time, willRemove])
            processes.append(c)

    [process.wait() for process in processes]

    print('That took {} seconds'.format(time.time() - start))
