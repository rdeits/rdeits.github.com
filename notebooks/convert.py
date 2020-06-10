import argparse
import os
import subprocess
from contextlib import contextmanager


# https://stackoverflow.com/a/24176022/641846
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.abspath(os.path.expanduser(newdir)))
    try:
        yield
    finally:
        os.chdir(prevdir)


parser = argparse.ArgumentParser()
parser.add_argument("notebook", type=str)
args = parser.parse_args()

folder = os.path.dirname(os.path.relpath(args.notebook, os.path.dirname(__file__)))
print("folder:", folder)

with cd(os.path.dirname(__file__)):
    os.environ["NBCONVERT_NOTEBOOK_FOLDER"] = folder
    subprocess.check_call(["jupyter", "nbconvert", "--debug", "--config", "nbconvert_config.py", args.notebook])

