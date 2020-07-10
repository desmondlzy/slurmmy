import os, shutil
import shlex
import subprocess as sp
import multiprocessing as mp
from argparse import ArgumentParser
import time

def dispatcher_args():
    parser = ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--tasks-per-allocation", type=int, default=1)
    parser.add_argument("--num-machines", type=int, default=3)
    parser.add_argument("--num-processes", type=int, default=1)
    parser.add_argument("--slurmargs", type=str, required=True)
    return parser.parse_args()

def username():
    homedir = os.path.expanduser("~")
    _, user = os.path.split(homedir)
    return user

def prepare_worker_args(args, start, stop): 
    worker_args = [
        "python", os.path.join(os.path.dirname(__file__), "worker.py"), 
        shlex.quote(args.file),
        "--start", str(start),
        "--stop", str(stop),
        "--num-processes", str(args.num_processes)
    ]
    return worker_args

def running_jobs():
    args = ["squeue", "--users", username()]
    lines = sp.check_output(args).decode("utf-8").splitlines()[1:]

    return lines

def batch_run(args, worker_args):
    with open("template.sbatch", "r") as fp:
        formatted_batch = fp.read().format(worker_args)
    
    with open("job.sbatch", "w") as fp:
        fp.write(formatted_batch)
    
    sbatch_args = ["sbatch", args.slurmargs]
    sp.check_call(sbatch_args + ["job.sbatch"])

    try:
        os.remove("job.sbatch")


def watch(args):
    num_machines = args.num_machines
    tasks_per_allocation = args.tasks_per_allocation

    with open(args.file, "r") as fp:
        tasks = [line.strip() for line in fp.readlines()]

    num_tasks = len(tasks)
    start_range = range(0, num_tasks, tasks_per_allocation)

    worker_jobs = [
        prepare_worker_args(args, start, min(start + tasks_per_allocation, num_tasks)) 
        for start in start_range
    ]

    # with mp.Pool(num_machines) as p:
    #     p.starmap(invoke_worker, worker_jobs)

    for job in worker_jobs:
        while num_machines - len(running_jobs()) <= 0:
            time.sleep(5)
        batch_run(args, job)
        



if __name__ == "__main__":
    args = dispatcher_args()
    watch(args)

# %%
