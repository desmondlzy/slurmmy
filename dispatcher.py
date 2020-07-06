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

def username():
    homedir = os.path.expanduser("~")
    _, user = os.path.split(homedir)

    return user

def running_jobs():
    args = [f"squeue --users={username()}"]
    lines = sp.check_output(args, shell=True).decode("utf-8").splitlines()[1:]

    return lines

def watch(args):
    num_machines = args.num_machines
    tasks_per_machine = args.tasks_per_machine

    with open(args.file, "r") as fp:
        tasks = [line.strip() for line in fp.readlines()]

    print("Dispatcher started, number of tasks:", len(tasks))

    cur = 0
    while cur < len(tasks):

        try:
            num_idle_machines = num_machines - len(running_jobs())
        except sp.CalledProcessError:
            num_idle_machines = num_machines

        if num_idle_machines == 0:
            time.sleep(5)

        elif num_idle_machines > 0:
            start, stop = cur, min(cur + tasks_per_machine, len(tasks))
            cur += tasks_per_machine

            print(f"{num_idle_machines} idle, submit {start} - {stop - 1}")
            print("Number of tasks to run:", len(tasks) - cur)

            child_args = args.slurmargs + " " + " ".join([
                "python", os.path.join(os.path.dirname(__file__), "worker.py"), 
                args.file,
                "--start", str(start),
                "--stop", str(stop),
                "--num-processes", str(args.num_processes)
            ])
            print(child_args)

            sp.check_call(child_args, shell=True)


if __name__ == "__main__":
    args = dispatcher_args()
    watch(args)

# %%
