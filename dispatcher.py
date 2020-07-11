import os, shutil
import shlex
import subprocess as sp
import multiprocessing as mp
from argparse import ArgumentParser
import time
from datetime import datetime

def dispatcher_args():
    parser = ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--tasks-per-allocation", type=int, default=1, 
        help="Number of tasks allocated to each computing server per one job submission")
    parser.add_argument("--num-machines", type=int, default=4, 
        help="Number of machines you want to use")
    parser.add_argument("--num-processes", type=int, default=1, 
        help="Number of processes for parallelism on the computing server to run multiple jobs")
    parser.add_argument("--slurm-args", type=str, required=True, 
        help="Arguments for sbatch, all arguments should be enclosed in one pair of double quote mark")
    parser.add_argument("--template", help="Path to template file")

    args = parser.parse_args()
    if args.template == None:
        args.template = os.path.join(os.path.dirname(__file__), "template.sbatch")
    return args

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

def batch_run(args, worker_args, **mapping):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    mapping["cmd"] = " ".join(worker_args)
    mapping["time"] = timestamp

    with open(args.template, "r") as fp:
        formatted_batch = fp.read().format_map(mapping)
    
    with open("job.sbatch", "w") as fp:
        fp.write(formatted_batch)
    
    sbatch_args = ["sbatch"] + shlex.split(args.slurm_args) + ["job.sbatch"]

    print(sbatch_args)

    sp.run(sbatch_args, check=True)

    try:
        os.remove("job.sbatch")
    except:
        pass

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

    for i, job in enumerate(worker_jobs):
        while num_machines - len(running_jobs()) <= 0:
            time.sleep(5)
        batch_run(args, job, job_index=i)
        



if __name__ == "__main__":
    args = dispatcher_args()
    watch(args)

# %%
