#!/bin/bash
#SBATCH --job-name={job_index}
#SBATCH --output={job_index}-{time}.log
pwd
{cmd}