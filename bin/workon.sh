#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJ_ROOT=${THIS_DIR}/..

pushd ${PROJ_ROOT} >> /dev/null

export VIRTUAL_ENV_DISABLE_PROMPT=1

if [ ! -d "venv" ]; then
    ./bin/create_venv.sh
else
    source venv/bin/activate
fi

# Invoke tab-completion
_complete_invoke() {
    local candidates
    candidates=`invoke --complete -- ${COMP_WORDS[*]}`
    COMPREPLY=( $(compgen -W "${candidates}" -- $2) )
}

# If running from zsh, run autoload for tab completion
if [ "$(ps -o comm= -p $$)" = "zsh" ]; then
    autoload bashcompinit
    bashcompinit
fi
complete -F _complete_invoke -o default invoke inv

# Pick up project-specific binaries
export PATH=${PROJ_ROOT}/bin:${PATH}

export PS1="(faasm-exp) $PS1"

popd >> /dev/null

