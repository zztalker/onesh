#!/usr/bin/bash

alias onesh='one-vm-list.py ssh'

_onesh_completions()
{
  COMPREPLY=($(compgen -W "$(one-vm-list.py listvms)" -- "${COMP_WORDS[1]}"))
}

complete -F _onesh_completions onesh
