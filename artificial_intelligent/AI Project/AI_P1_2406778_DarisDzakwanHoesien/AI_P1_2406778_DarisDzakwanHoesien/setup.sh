#!/bin/bash

# Create virtual environment
python3 -m venv venv_ai_p1

# Activate virtual environment
source venv_ai_p1/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
