#!/usr/bin/env python3
import subprocess as sp
import sys
import os

BACKUP_NAME = 'linux4coder-projects.tar'
HOME = os.getenv('HOME')
PROJECTS_DIR = 'projects'
if len(sys.argv) != 2:
    print('Wrong args count', file=sys.stderr)
    sys.exit(1)
TAR_CMD = ['tar', 'czf', sys.argv[1] + os.sep + BACKUP_NAME, PROJECTS_DIR]
os.chdir(HOME)
with sp.Popen(TAR_CMD, universal_newlines=True, stdout=sp.PIPE, stderr=sp.PIPE) as p:
    out, err = p.communicate()
    if p.returncode != 0:
        print(err, file=sys.stderr)
