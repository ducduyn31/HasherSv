import math
import os
import time
from hashlib import sha512
from optparse import OptionParser

import psutil

process = psutil.Process(os.getpid())
parser = OptionParser()


def exec(filepath, block_size, n):
    file_size = os.path.getsize(filepath)

    with open(filepath, 'rb') as f:
        hasher = sha512()
        tik = time.perf_counter_ns()

        blocks = math.ceil(file_size / block_size)
        space = blocks // (n + 1)
        current_block = 0

        file_buffer = []

        while current_block < blocks:
            f.seek(current_block * block_size, 0)
            buffer = f.read(block_size)
            # hasher.update(buffer)
            file_buffer.append(buffer)
            current_block += space

        f.seek((blocks - 1) * block_size, 0)
        buffer = f.read(block_size)
        file_buffer.append(buffer)

        midtik = time.perf_counter_ns()
        io_time = midtik - tik

        for b in file_buffer:
            hasher.update(b)

        hex = hasher.hexdigest()
        tok = time.perf_counter_ns()
        elapsed_time = tok - midtik

    return io_time, elapsed_time, hex


def main(file_path, block_size, n):
    psutil.Process().nice(-20)
    results = []

    for i in range(1):
        results.append(exec(file_path, block_size, n))

    return sorted(results, key=lambda x: x[0])[0]


if __name__ == '__main__':
    parser.add_option('-i', '--input', help='File to hash')
    parser.add_option('-n', '--samples', default=1, help='# of samples')
    parser.add_option('-b', '--blocksize', default=64, help='Sample block size')
    (options, args) = parser.parse_args()
    file_path = options.input
    block_size = int(options.blocksize)
    n = int(options.samples)

    # process.nice(0)
    # print(process.nice())
    main(file_path, block_size, n)
