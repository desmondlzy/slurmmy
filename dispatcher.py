import os, shutil
import subprocess as sp
import multiprocessing as mp
from argparse import ArgumentParser
import time

def dispatcher_args():
    parser = ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--tasks-per-machine", type=int, default=1)
    parser.add_argument("--num-machines", type=int, default=3)
    parser.add_argument("--num-processes", type=int, default=1)
    parser.add_argument("--slurmargs", type=str, required=True)

    return parser.parse_args()

def invoke_worker(args, start, stop):
    slurmargs = ["srun"] + [arg for arg in args.slurmargs.split()]
    childargs = slurmargs + [
        "python", os.path.join(os.path.dirname(__file__), "worker.py"), 
        args.file,
        "--start", str(start),
        "--stop", str(stop),
        "--num-processes", str(args.num_processes)
    ]
    print(" ".join(childargs))
    sp.check_call(childargs)

def watch(args):
    num_machines = args.num_machines
    tasks_per_machine = args.tasks_per_machine

    with open(args.file, "r") as fp:
        tasks = [line.strip() for line in fp.readlines()]

    num_tasks = len(tasks)
    start_range = range(0, num_tasks, tasks_per_machine)

    print(f"Dispatcher ready, num_tasks: {num_tasks}, num_machines: {num_machines}, tasks_per_machine: {tasks_per_machine}")
    jobs = [
        (args, start, min(start + tasks_per_machine, num_tasks)) 
        for start in start_range
    ]

    with mp.Pool(num_machines) as p:
        p.starmap(invoke_worker, jobs)


if __name__ == "__main__":
    args = dispatcher_args()
    watch(args)

# %%
