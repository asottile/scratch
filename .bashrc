# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# it's unclear why this changed between 18.04 and 20.04
umask 0022

HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=-1
HISTFILESIZE=-1

command_not_found_handle() {
    if [ -x "venv/bin/$1" ]; then
        echo 'you forgot to activate ./venv -- I gotchu' 1>&2
        exe="venv/bin/$1"
        shift
        "$exe" "$@"
        return $?
    else
        echo "$0: $1: command not found" 1>&2
        return 127
    fi
}

PS1='\[\e]0;\u@\h: \w\a\]\[\033[1;92m\]\u@\h\[\033[m\]:\[\033[1;94m\]\w\[\033[m\]\n\$ '

[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"
[ -x /usr/bin/dircolors ] && eval "$(dircolors -b)"
[ -f /etc/bash_completion ] && . /etc/bash_completion

[ -f ~/.bash_aliases ] && . ~/.bash_aliases
[ -d "$HOME/bin" ] && export PATH="${HOME}/bin:${PATH}"

PROMPT_COMMAND='if [ -d .git -a ! -x .git/hooks/pre-commit -a -e .pre-commit-config.yaml ] && command -v pre-commit >& /dev/null; then pre-commit install --hook-type pre-commit; fi; '"$PROMPT_COMMAND"
eval "$(aactivator init)"

export PYTHONSTARTUP=~/.pythonrc.py
export EDITOR=babi VISUAL=babi

export DEBEMAIL="asottile@umich.edu" DEBFULLNAME="Anthony Sottile"

export PIP_DISABLE_PIP_VERSION_CHECK=1
export VIRTUALENV_NO_PERIODIC_UPDATE=1

if [ -d ~/.bashrc.d ]; then
    for f in ~/.bashrc.d/*.sh; do
        . "$f"
    done
    unset f
fi
