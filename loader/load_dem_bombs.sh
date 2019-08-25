#!/bin/bash

curr_path=$(pwd)
file_name=rasps_list.txt
file_path=$curr_path/$file_name
rasp_binary_path=~/Desktop/.files
repo_url=https://github.com/AaronGarcia97/pypl-meter-rasp

# Receive IP/HOST and command to execute over ssh.
function ExecuteLine() {
	local curr_ip="$1"
	local line="$2"
	if [ "$#" -ne 2 ]; then
		echo "Illegal number of parameters"
		exit 2
	fi
	echo "Executing '$line' command..."
	ssh root@$curr_ip $line
}

# Verifies dependencies are install, receive ip/host.
#   git, aircrack-ng
function Setup() {
	# setup each individual pi
	# verify dependencies are there, etc
	# download from github and create directory
	local curr_ip="$1"
	echo "Starting to Setup..."
	ExecuteLine $curr_ip "echo toor | sudo -s"
	echo "Got root access in $curr_ip..."
	ExecuteLine $curr_ip "yes | apt-get install python3"
	ExecuteLine $curr_ip "yes | apt-get install git"
	ExecuteLine $curr_ip "yes | apt-get install aircrack-ng"
	echo "Dependencies installed..."
}

# Loads everything, main logic and runs binary
function Load() {
	local curr_ip="$1"
	# Setup everything
	Setup $curr_ip
	echo "Starting to Load..."
	# Create hidden directory and clone "binary"
	ExecuteLine $curr_ip "mkdir -p $rasp_binary_path"
	ExecuteLine $curr_ip "yes | git clone $repo_url $rasp_binary_path"
	# Kill process if exists
	ExecuteLine $curr_ip "kill $(ps aux | grep scanner | awk '{print $2}')"
	echo "Eliminated last process if existed..."
	# Run it again, hiding output and send to bg?
	ExecuteLine $curr_ip "python3 $rasp_binary_path/pypl-meter-rasp/scanner.py &"
	echo "New binary succesfully loaded and running..."
}

echo "Starting..."

# Send individual ip_address as parameter
ip_address=$1
Load $ip_address

# This is not iterating appropiately, not sure why
#while IFS= read -r ip_address
#do
	# For each raspberry pi
#	echo "START: $ip_address"
	# Load $ip_address
#	echo "DONE: $ip_address"

#done < "$file_path"
