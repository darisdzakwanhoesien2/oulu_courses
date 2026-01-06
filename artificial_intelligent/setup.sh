#!/bin/bash

cd "AI Project/AI_P1_2406778_DarisDzakwanHoesien/AI_P1_2406778_DarisDzakwanHoesien" || exit 1

python3 -m venv venv_ai_p1

source venv_ai_p1/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

python pacman.py -h
