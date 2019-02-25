#!/bin/bash

cp one-vm-list.py ~/.local/bin
chmod +x ~/.local/bin/one-vm-list.py
mkdir -p ~/.local/etc/onevm
cp onesh-completion.sh ~/.local/etc/onevm
grep -q "onesh-completion.sh" ~/.bashrc || echo "source ~/.local/etc/onevm/onesh-completion.sh" >> ~/.bashrc
