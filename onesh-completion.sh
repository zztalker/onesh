#!/usr/bin/bash

alias onesh='one-vm-list.py ssh'
alias onesync='one-vm-list.py rsync'
alias onels='one-vm-list.py listvms'
alias onescp='one-vm-list.py scp'
alias oneping='one-vm-list.py ping'

_onesh_completions()
{
  COMPREPLY=($(compgen -W "$(one-vm-list.py listvms)" -- "${COMP_WORDS[1]}"))
}

complete -F _onesh_completions onesh
complete -F _onesh_completions onesync
complete -F _onesh_completions onescp
complete -F _onesh_completions oneping

