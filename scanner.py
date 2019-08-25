import subprocess
from subprocess import call
import os
import requests
import threading


global_timer = 15   #seconds to send devices info to post api
name_of_file = "info"
output_file = "output"
server_ip = "10.22.136.99"
server_port = "5000"
pwd = os.getcwd()

print(f"Current working path = {pwd}")

def GetJsonParsingFile():
    cmd = [f"cut -d ' ' -f1,6 {pwd}/{output_file}"]
    process = subprocess.run(cmd, shell=True, check=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout
    print(output)
    list_info = []
    print("LIINNNNNEEEEES:")
    for line in output.splitlines():
        print(line)
        list_info.append(line.strip(',').split(','))
        if len(list_info[-1]) == 2:
            list_info[-1][1] = list_info[-1][1].strip()   # clean space of intensity
    list_info.pop() # Remove last empty element, (EOF?)
    print(list_info)
    return list_info

def SendStuffToApi():
    # Here send everything to post request
    print('Sending stuff!!!')
    try:
        r = requests.post(url=f'http://{server_ip}:{server_port}/AddDevices', json=GetJsonParsingFile())
        print("Info sent succesfully!")
        print("Response object: ")
        print(r)
    except Exception as e:
        print("ERROR! Sending post /AddDevices. ERROR!")
        print(e)

call(["airmon-ng", "start", "wlan0"])

print("wlan0 in monitor mode...")

while True:
    cmd = ["airodump-ng", "wlan0mon", "-w", f"{pwd}/{name_of_file}", "--output-format", "csv"]
    print(cmd)

    thread_list = []  # starts empty

    try:
        print("About to run airodump-ng...")
        subprocess.run(cmd, timeout=global_timer)
    except subprocess.TimeoutExpired:
        print('Moving everything to different file')

    cmd = [f"sed -e '1,/Station MAC, First time seen,/d' \
            {pwd}/{name_of_file}-01.csv > {pwd}/{output_file}"]
    try:
        subprocess.run(cmd, shell=True, check=True, timeout=global_timer-1)
    except subprocess.TimeoutExpired:
        print('Failed to move stuff of file') 

    cmd = ["rm", f"{pwd}/{name_of_file}-01.csv"]
    subprocess.run(cmd, timeout=global_timer-1)
    print (f"File {pwd}/{name_of_file}-01.csv deleted")
    thread1 = threading.Thread(target = SendStuffToApi)
    thread1.start()
    # thread1.join()
    # exit()

    # Use this command to get useful peice of information then cut it
    # sed -e 1,/Station MAC, First time seen,/d test-01.csv
