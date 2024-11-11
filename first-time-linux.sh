#!/usr/bin/env bash
# asumsi udh ke install python
sudo apt update
sudo apt install python3-pygame -y
sudo apt install python3-venv
python3 -m venv ~/myenv
source ~/myenv/bin/activate` `pip install staticmap
./main.py
