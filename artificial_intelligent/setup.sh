#!/bin/bash


usage() {
  cat <<EOF
Usage: $(basename "$0") [options]
[No description available]
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi
cd "AI Project/AI_P1_2406778_DarisDzakwanHoesien/AI_P1_2406778_DarisDzakwanHoesien" || exit 1

python3 -m venv venv_ai_p1

source venv_ai_p1/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

python pacman.py -h
