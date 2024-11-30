#!/bin/bash

# DESCRIPTION: Launch a locust attack on a given IP address


read -p "Enter the number of users: " users
read -p "Enter the spawn rate: " spawn_rate
read -p "Enter IP address: " ip

locust -f stress.py --host=http://$ip:8501  --processes -1 -u $users -r $spawn_rate