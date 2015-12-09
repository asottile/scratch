# Add the following to ~/.bash_profile
# export PYTHONSTARTUP=~/.pythonrc.py
import readline
import rlcompleter  # noqa
readline.parse_and_bind('tab: complete')
