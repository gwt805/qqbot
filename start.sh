#!/bin/bash

str=$"\n"

cd /home/linux1/qqbot

nohup /home/linux1/anaconda3/bin/python app.py > /dev/null 2>&1 &

sstr=$(echo -e $str)

echo $sstr