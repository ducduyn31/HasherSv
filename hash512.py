from hashlib import sha512
from optparse import OptionParser
import time
parser = OptionParser()

if __name__ == '__main__':
    parser.add_option('-i', '--input', help='File to hash')
    (options, args) = parser.parse_args()
    file_path = options.input

    with open(file_path, 'rb') as f:
        hasher = sha512()

        tik = time.perf_counter_ns()
        buffer = f.read(1 << 16)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = f.read(1 << 16)

        tok = time.perf_counter_ns()
        elapsed_time = tok - tik

    print(elapsed_time / 10**9)
