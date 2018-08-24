# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=1000
HISTFILESIZE=2000

PS1='\[\e]0;\u@\h: \w\a\]\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '

[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"
[ -x /usr/bin/dircolors ] && eval "$(dircolors -b)"
[ -f /etc/bash_completion ] && . /etc/bash_completion

[ -f ~/.bash_aliases ] && . ~/.bash_aliases
[ -d "$HOME/bin" ] && export PATH="${HOME}/bin:${PATH}"

PROMPT_COMMAND='if [ -d .git -a ! -x .git/hooks/pre-commit -a -e .pre-commit-config.yaml ] && which pre-commit >& /dev/null; then pre-commit install; fi; '"$PROMPT_COMMAND"
eval "$(aactivator init)"

export PYTHONSTARTUP=~/.pythonrc.py
export EDITOR=nano VISUAL=nano

export DEBEMAIL="asottile@umich.edu" DEBFULLNAME="Anthony Sottile"

if [ -d ~/.bashrc.d ]; then
    for f in ~/.bashrc.d/*.sh; do
        . "$f"
    done
    unset f
fi
