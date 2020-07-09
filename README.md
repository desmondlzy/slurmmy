Slummy
=================

Tens of thousands of machine learning tasks to submit and run through [slurm](https://slurm.schedmd.com/documentation.html)? Little quotas, long-time waiting, don't want to get stuck in front of the terminal, waiting and waiting? Out-of-box automated scripts for your use!

Quick start
-----------------
Put the shell commands for the jobs into a text file, say `fabulous-ml-tuning-tasks.txt`. Each command takes one line.
```
python tensortorch.py --hyperparameter 1
python tensortorch.py --hyperparameter 2
python tensortorch.py --hyperparameter 3
...
python tensortorch.py --hyperparameter 100000
```

Feed the text file to `slurmmy/dispatcher.py`. Change `--slurmargs` as per your own setting.
```
git clone https://github.com/desmondlzy/slummy.git 
python slummy/dispatcher.py fabulous-ml-tuning-tasks.txt --slurmargs="--gres=gpu:1"
```
The program will keep watching the slurm queue, and submit new tasks via `srun` once there is an avaiable machine.

You shall be all set! Have a cup of :coffee: or go to :sleeping:! (You may want to use `nohup` or `tmux` to keep it running after your current session ends...)

Usage
------------------
Always invoke `dispatcher.py` as the entry point, which provides you with these command line arguments (inspect them via `-h`)

- `--tasks-per-machine`: Number of tasks (number of lines of commands in the input file) allocated to one server each time. (default: 1)
- `--num-machines`: Number of worker machines you want to use. It should not exceed the maximum number available to you as per your slurm configuration. (default: 2)
- `--num-processes`: Number of processes to launch on each worker machine to run the allocated task using process-level parallelism (via `multiprocessing.Pool`). If set to 1, no parallelism will be conducted. *Usually, this number shouldn't exceed the number of cores applied through slurm for each task (i.e. `-c`).* (default: 1)
- `--slurmargs`: The arguments that will be directly passed to `srun`. All arguments should be enclosed in a pair of double quotation marks. For example, `--slurmargs="--gres=gpu:1 -c=10"`. Refer to the their [cheatsheet](https://slurm.schedmd.com/pdfs/summary.pdf) for more information.

Notes
------------------
The scripts hosted here were written for my own developing environment, where the number of pending jobs is quite limited and the `array` and `ntask` feature of slurm doesn't work very well.