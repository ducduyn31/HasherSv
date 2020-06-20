import math
import os
import time
from hashlib import sha512
from optparse import OptionParser

parser = OptionParser()

if __name__ == '__main__':
    parser.add_option('-i', '--input', help='File to hash')
    parser.add_option('-n', '--samples', default=1, help='# of samples')
    parser.add_option('-b', '--blocksize', default=128, help='Sample block size')
    (options, args) = parser.parse_args()
    file_path = options.input
    file_size = os.path.getsize(file_path)
    block_size = int(options.blocksize)
    n = int(options.samples)

    with open(file_path, 'rb') as f:
        hasher = sha512()
        tik = time.perf_counter_ns()

        blocks = math.ceil(file_size / block_size)
        space = blocks // (n + 1)
        current_block = 0

        while current_block < blocks:
            f.seek(current_block * block_size, 0)
            buffer = f.read(block_size)
            hasher.update(buffer)
            current_block += space

        f.seek((blocks - 1) * block_size, 0)
        buffer = f.read(block_size)
        hasher.update(buffer)

        hex = hasher.hexdigest()
        tok = time.perf_counter_ns()
        elapsed_time = tok - tik

    print(elapsed_time)
    print(hex)
