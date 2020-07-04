import multiprocessing as mp
import subprocess as sp
from argparse import ArgumentParser

def worker_args():
    parser = ArgumentParser()
    parser.add_argument("file", required=True)
    parser.add_argument("--start", type=int)
    parser.add_argument("--stop", type=int)
    parser.add_argument("--num-processes", type=int, default=1)

    return parser.parse_args()

if __name__ == "__main__":
    args = worker_args()

    start = args.start
    stop  = args.stop
    n_proc = args.num_processes

    with open(args.file, "r") as fp:
        all_tasks = fp.readlines()
    
    tasks = all_tasks[start:stop]

    if args.num_processes > 1:
        with mp.Pool(n_proc) as p:
            p.map(sp.run, tasks)
    elif n_proc == 1:
        for task in tasks:
            sp.check_call(task)
    else:
        raise ValueError(f"Num processes should be strictly postive, get {n_proc}")