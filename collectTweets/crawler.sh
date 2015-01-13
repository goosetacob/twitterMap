#!/bin/bash
echo "Welcome, this project was developed by Gustavo Blanco & Michael De La Torre for CS172: Intro to Information Retreival @ UC Riverside"

##necessary dependancies 
echo 'installing Twitter API'
sudo easy_install twitter &
echo 'installing LXML libary'
sudo pip install lxml &
echo 'installing REQUESTS LIBARY'
sudo pip install requests &

echo 'creating DB dir to store all tweets'
mkdir DB
echo 'running our Python Program'
python init.py
