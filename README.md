Slurmmy
=================

Tens of thousands of machine learning tasks to submit and run through [slurm](https://slurm.schedmd.com/documentation.html)? Little quotas, long-time waiting, don't want to get stuck in front of the terminal, waiting forever? You may find these out-of-box, minimal, zero-extra-dependency automated scripts come in handy.

Quick start
-----------------
Suppose you have some jobs to run. Write you program in the way that each job is invoked by a shell command (probably a script with tunable parameters as input arguments). Then, put the shell commands for those jobs into a text file. Each command takes exactly one line. The text file, say `fabulous-ml.txt`, should look like this,
```
python tensortorch.py --hyperparameter 1
python pyflow.py --hyperparameter 1
python tensortorch.py --hyperparameter 2
python pyflow.py --hyperparameter 2
...
python tensortorch.py --hyperparameter 100000
python pyflow.py --hyperparameter 100000
```

Feed the text file to `slurmmy/dispatcher.py`. (You may change `--slurm-args` as per your own slurm setting.)
```
git clone https://github.com/desmondlzy/slurmmy.git 
python slummy/dispatcher.py fabulous-ml.txt --slurm-args="--gres=gpu:1"
```
The program will keep watching the slurm queue, and submit new tasks via `sbatch` once there is an available machine.

You shall be all set! Have a cup of :coffee: or go to :sleeping: (You may want to use `nohup` or `tmux` to keep it running after your current session expires...)

Usage
------------------
Following the above section, you could leverage the command line arguments (inspect them via `dispatcher.py -h`) as per your own cases and environments to get optimized running scheduling.

- `--slurm-args`: Required arguments for `sbatch`. Everything here should be enclosed in a pair of quotation marks and will be directly passed to `sbatch` during the execution. For example, `--slurm-args="--gres=gpu:1 -c=10"`. Refer to slurm's [cheatsheet](https://slurm.schedmd.com/pdfs/summary.pdf) for more details.
- `--tasks-per-allocation`: Number of tasks (number of lines of commands in the input file) allocated to one server each time. (default: 1)
- `--num-machines`: Number of worker machines you want to use. It should not exceed the maximum number available to you as per your slurm accounting policy. (default: 4)
- `--num-processes`: Number of processes to launch on each worker machine to run the allocated task using process-level parallelism (via `multiprocessing.Pool`). If set to 1, no parallelism will be conducted. *Usually, this number shouldn't exceed the number of cores applied through slurm for each task (i.e. `-c`).* (default: 1)
- `--template`: Path to your template file, see the [template section](#template) for more info.

### Template

Internally, for each submission, Slummy aggregates jobs and accordingly renders the template into a shell script for the use of `sbatch`. You could write your own templates for more flexibility, and pass its path to the `dispatcher.py` via `--template`. Here is a list of placeholders you may include in your templates. You could refer to the [default](./template.sbatch) template as an example.

- `{cmd}`: **Required**, the command line arguments for invoking `worker` will be rendered here.
- `{time}`: Timestamp for the beginning of the submission.
- `{job_index}`: The index of job submission, starting from 0

Notes
------------------
The scripts hosted here were written based on my own need when I was an undergrad in at CUHK in 2020. Everything was targeting the departmental remote machines, where the number of pending jobs is quite limited (only 5) and the `array` and `ntask` feature of slurm didn't work. What's hosted here may not be the best solution to the problem you're facing.

If you're in CUHK CSE and want to squeeze every milisecond out of the computing server, please refer to this blog article ([English](https://desmondlzy.me/blog/slurmmy-intro-en)/[Chinese](https://desmondlzy.me/blog/slurmmy-intro-zh)) I wrote in 2020 for my practices.
