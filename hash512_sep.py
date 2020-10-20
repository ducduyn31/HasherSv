import time
from hashlib import sha512
from optparse import OptionParser

import psutil

parser = OptionParser()


def exec(filepath):
    with open(file_path, 'rb') as f:
        hasher = sha512()

        buffer = f.read()

        tik = time.perf_counter_ns()
        # buffer = f.read(1 << 16)
        # while len(buffer) > 0:
        #     hasher.update(buffer)
        #     buffer = f.read(1 << 16)

        hasher.update(buffer)

        hex = hasher.hexdigest()
        tok = time.perf_counter_ns()
        elapsed_time = tok - tik

    return elapsed_time, hex


def main(file_path):
    psutil.Process().nice(-20)
    results = []

    for i in range(1):
        results.append(exec(file_path))

    return sorted(results, key=lambda x: x[0])[0]


if __name__ == '__main__':
    parser.add_option('-i', '--input', help='File to hash')
    (options, args) = parser.parse_args()
    file_path = options.input

    main(file_path)
