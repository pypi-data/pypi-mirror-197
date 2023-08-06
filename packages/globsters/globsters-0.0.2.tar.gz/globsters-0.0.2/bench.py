import fnmatch
import time

import globsters
from globsters import Globsters

data = [
    "file.txt",
    "file.py",
    "file.exe",
    "file.PY",
]

iterations = 100_000


def fnmatch_bench():
    for i in range(iterations):
        for d in data:
            fnmatch.fnmatch(d, "*.py")


def globsters_bench():
    globster_matcher = globsters.globster("*.py", case_insensitive=True, cache=False)
    for i in range(iterations):
        for d in data:
            globster_matcher(d)


def globsters_bench_cached_pattern():
    for i in range(iterations):
        for d in data:
            globsters.globster("*.py", case_insensitive=True, cache=True)(d)


def do_match():
    globster_matcher = globsters.globster("*.py", case_insensitive=True)
    for d in data:
        fn_res = fnmatch.fnmatch(d, "*.py")
        gl_res = globster_matcher(d)
        if fn_res != gl_res:
            print(f"fn_res: {fn_res}, gl_res: {gl_res} ~ '{d}'")
            assert fnmatch == globster_matcher


def main():
    do_match()
    ti_a = time.perf_counter()
    fnmatch_bench()
    tf_a = time.perf_counter()
    dt_a = tf_a - ti_a
    print(f"fnmatch_bench: {dt_a:.3f} seconds")

    ti_b = time.perf_counter()
    globsters_bench()
    tf_b = time.perf_counter()
    dt_b = tf_b - ti_b
    print(f"globsters_bench: {dt_b:.3f} seconds")

    ti_b = time.perf_counter()
    globsters_bench_cached_pattern()
    tf_b = time.perf_counter()
    dt_b = tf_b - ti_b
    print(f"globsters_bench_cached_pattern: {dt_b:.3f} seconds")


if __name__ == "__main__":
    main()
