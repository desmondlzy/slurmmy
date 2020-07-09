import multiprocessing as mp
import subprocess as sp
import os
from argparse import ArgumentParser

def worker_args():
    parser = ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--start", type=int)
    parser.add_argument("--stop", type=int)
    parser.add_argument("--num-processes", type=int, default=1)

    return parser.parse_args()

def shell_run(cmd):
    return sp.check_call(cmd, shell=True)

if __name__ == "__main__":
    args = worker_args()

    start = args.start
    stop  = args.stop
    n_proc = args.num_processes

    print(os.getcwd())

    with open(args.file, "r") as fp:
        all_tasks = fp.readlines()
    
    tasks = [task.strip() for task in all_tasks[start:stop]]

    if args.num_processes > 1:
        with mp.Pool(n_proc) as p:
            p.map(shell_run, tasks)
    elif n_proc == 1:
        for task in tasks:
            sp.check_call(task, shell=True)
    else:
        raise ValueError(f"Num processes should be strictly postive, get {n_proc}")