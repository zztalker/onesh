#!/usr/bin/bash

alias onesh='one-vm-list.py ssh'
alias onesync='one-vm-list.py rsync'

_onesh_completions()
{
  COMPREPLY=($(compgen -W "$(one-vm-list.py listvms)" -- "${COMP_WORDS[1]}"))
}

complete -F _onesh_completions onesh
complete -F _onesh_completions onesync
