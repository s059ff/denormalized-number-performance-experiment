import argparse
import json
import os
import pathlib
import timeit

from fenv import set_ftz, unset_ftz

os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_NUM_THREADS"] = "1"

import numpy as np  # noqa: E402

import cpuinfo  # noqa: E402

FLT_MIN = 1.175494351e-38


def to_binary(a: np.ndarray):
    return a.view(np.int32)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", type=int, default=1000)
    parser.add_argument("-n", type=int, default=1 << 20)
    parser.add_argument("--ftz", action="store_true")
    return parser.parse_args()


def main():
    logs = {}

    args = parse_args()
    key, value = "args", vars(args)
    logs[key] = value
    print(f"{key}: {value}")

    key, value = "cpuinfo", cpuinfo.get_cpu_info()
    logs[key] = value
    print(f"{key}: {value}")

    if args.ftz:
        set_ftz()
        print("ftz/daz: enabled")
    else:
        unset_ftz()
        print("ftz/daz: disabled")

    np.random.seed(12345)

    norm = np.random.normal(0.0, 1.0, args.n).astype(np.float32)
    denorm = np.random.uniform(FLT_MIN / 10, FLT_MIN, args.n).astype(np.float32)
    nan = np.full(args.n, np.nan, dtype=np.float32)

    def task_template(a: np.ndarray):
        return (
            0.0
            + a / 1.08
            - a / 1.07
            + a / 1.06
            - a / 1.05
            + a / 1.04
            - a / 1.03
            + a / 1.02
            - a / 1.01
        ).flat[0]

    def task_normal():
        return task_template(norm)

    def task_denormal():
        return task_template(denorm)

    def task_nan():
        return task_template(nan)

    for task in [task_normal, task_denormal, task_nan]:
        key, value = f"{task.__name__}.result", float(task())
        logs[key] = value
        print(f"{key}: {value}")

        key, value = f"{task.__name__}.result.hex", f"{to_binary(task()):032b}"
        logs[key] = value
        print(f"{key}: {value}")

    for task in [task_normal, task_denormal, task_nan]:
        durations = np.array(timeit.repeat(task, repeat=args.r, number=1))
        durations *= 1000

        key, value = f"{task.__name__}.time.avg", np.average(durations)
        logs[key] = value
        print(f"{key}: {value}")

        key, value = f"{task.__name__}.time.min", np.min(durations)
        logs[key] = value
        print(f"{key}: {value}")

        key, value = f"{task.__name__}.time.max", np.max(durations)
        logs[key] = value
        print(f"{key}: {value}")

        key, value = f"{task.__name__}.time.std", np.std(durations)
        logs[key] = value
        print(f"{key}: {value}")

    with open(f"{pathlib.Path(__file__).stem}.log", "a+") as stream:
        stream.write(json.dumps(logs))
        stream.write("\n")


if __name__ == "__main__":
    main()
