# Add the following to ~/.bash_profile
# export PYTHONSTARTUP=~/.pythonrc.py
from __future__ import annotations

import readline
import rlcompleter  # imported purely for side-effects

readline.parse_and_bind('tab: complete')
del readline, rlcompleter


def pp(o):
    import pprint
    pprint.pprint(o)


def ppj(o):
    import json
    print(json.dumps(o, indent=2))
