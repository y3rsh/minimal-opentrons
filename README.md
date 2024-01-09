# Minimum Opentrons

## Required

1. Python 3.10.11
  1. It is recommended to use [pyenv](https://github.com/pyenv/pyenv)
  1. `pyenv install 3.10.11`
1. [git](https://git-scm.com/) or [GitHub Desktop](https://desktop.github.com/)

## How to

1. navigate to the directory you want to work in
1. clone the repo
    1. `git clone https://github.com/y3rsh/minimal-opentrons.git`
1. setup the local version of python with pyenv
    1. `pyenv local 3.10.11`
1. run the script.  This will create a virtual environment and install the opentrons packages
    1. `python setup.py <commit hash or branch name or tag>`
        1. You may use a commit hash, branch name, or tag
        1. Recents examples of tags that can be found at <https://github.com/Opentrons/opentrons/tags> are `v7.1.1`, `v7.1.0`, `v7.0.2`
    1. `python setup.py v7.1.1`

## Use the virtual environment

1. Windows
    1. `.\.venv_v7.1.1\Scripts\Activate.ps1`
2. Use simulate
    1. `python -m opentrons.simulate --help`
