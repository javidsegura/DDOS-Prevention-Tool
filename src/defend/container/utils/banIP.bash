#!/bin/bash

# Ban a passed IP address in linux
IP=$1

if [ -z "$IP" ]; then
    echo "No IP address provided"
    exit 1
fi

echo "Banning IP: $IP. INSERT PASSWORD: "
# Try to ban the IP using iptables
if sudo iptables -A INPUT -s $IP -j DROP; then
    echo "Successfully banned IP: $IP"
    exit 0
else
    echo "Failed to ban IP: $IP"
    exit 1
fi