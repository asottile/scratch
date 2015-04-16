# Add the following to ~/.bash_profile
# export PYTHONSTARTUP=~/.pythonrc.py

import readline
import rlcompleter
readline.parse_and_bind('tab: complete')
