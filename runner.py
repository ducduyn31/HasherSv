import os
from optparse import OptionParser

from logger import log_to_db

parser = OptionParser()

if __name__ == '__main__':
    parser.add_option('-i', '--input', help='File to hash')
    parser.add_option('-n', '--samples', default=1, help='# of samples')
    parser.add_option('-b', '--blocksize', default=128, help='Sample block size')
    (options, args) = parser.parse_args()
    file_path = options.input
    block_size = int(options.blocksize)
    n = int(options.samples)

    full_hash_stream = os.popen('python hash512.py -i {}'.format(file_path))
    output = full_hash_stream.read()[1:-2].split(',')
    full_hash_time = int(output[0])
    full_hash_hex = output[1][2:-1]

    tactical_hash_stream = os.popen('python sampling_n_hash.py -i {} -n {}'.format(file_path, n))
    output2 = tactical_hash_stream.read()[1:-2].split(',')
    tactical_hash_time = int(output2[0])
    tactical_hash_hex = output2[1][2:-1]

    log_to_db(file_path, full_hash_hex, n, tactical_hash_hex, os.path.getsize(file_path), full_hash_time,
              tactical_hash_time)

    print(full_hash_hex, int(full_hash_time))
    print(tactical_hash_hex, int(tactical_hash_time))
