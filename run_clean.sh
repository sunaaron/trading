#!/bin/bash
cd /home/ubuntu/workspace/trading
rm ./data/*
source env/bin/activate
python main.py
deactivate