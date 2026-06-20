#!/bin/bash

# Create virtual environment

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]
Create virtual environment
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi
python3 -m venv venv_ai_p1

# Activate virtual environment
source venv_ai_p1/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
