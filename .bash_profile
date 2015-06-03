if [ "$TERM" == "xterm" ]; then
    # Gnome terminal supports 256 colors, but doesn't have a way to edit $TERM
    export TERM=xterm-256color
fi

export TOXENV=py27
export BENCH=false

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

export PIP_DOWNLOAD_CACHE=/home/asottile/.pip/cache
export PYTHONSTARTUP=~/.pythonrc.py

