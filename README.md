Slummy
=================

Tens of thousands of machine learning tasks to submit and run through slurm? Little quotas and long time waiting? Out-of-box automated scripts for your use!

Minimal Usage
-----------------
Write all your jobs into a text file, say `fabulous-ml-tuning.txt`
```
python tensortorch.py --hyperparameter 1
python tensortorch.py --hyperparameter 2
python tensortorch.py --hyperparameter 3
...
python tensortorch.py --hyperparameter 100000
```
Feed the text file to `slurmmy/dispatcher.py`.
```
git clone https://github.com/desmondlzy/slummy.git 
python slummy/dispatcher.py fabulous-ml-tuning.txt --slurmargs="--gres=gpu:1"
```
Have a cup of coffee or go to sleep!