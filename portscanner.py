#when we connect to the server by a port we need to complete response
#TCP 3-way handshake 
import threading
import socket
import sys # to get the argument from the terminal we use this library
import time # to get the time till what time it is scanned
import ipaddress
# We need to create regular expressions to ensure that the input is correctly formatted.
import re

usage="python3 portscanner.py TARGET START_PORT END_PORT"

port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
# Initialising the port numbers, will be using the variables later on.
port_min = 0
port_max = 65535
while True:
    ip_add_entered = input("\nPlease enter the ip address that you want to scan: ")
    try:
        target=socket.gethostbyname(ip_add_entered) # host->IP and store in target    
    except socket.gaierror:  # get address info it it isnt able to convert to ipaddress
        print("Name resolution error")
        sys.exit()
    # If we enter an invalid ip address the try except block will go to the except block and say you entered an invalid ip address.
    try:
        ip_address_obj = ipaddress.ip_address(target)
        # The following line will only execute if the ip is valid.
        print("You entered a valid ip address.")
        break
    except:
        print("You entered an invalid ip address")
    

while True:
    # You can scan 0-65535 ports. This scanner is basic and doesn't use multithreading so scanning all
    # the ports is not advised.
    print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
    port_range = input("Enter port range: ")
    # We pass the port numbers in by removing extra spaces that people sometimes enter. 
    # So if you enter 80 - 90 instead of 80-90 the program will still work.
    port_range_valid = port_range_pattern.search(port_range.replace(" ",""))
    if port_range_valid:
        # We're extracting the low end of the port scanner range the user want to scan.
        start_port = int(port_range_valid.group(1))
        # We're extracting the upper end of the port scanner range the user want to scan.
        end_port = int(port_range_valid.group(2))
        break


start_time=time.time()


print("Scanning:",target)
def scan_port(port):

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#creates a TCP socket object that can be used for network communication over IPv4 addresses.

    #The socket.AF_INET --> (IPv4)
    #To use IPv6 addresses --> socket.AF_INET6
    #SOCK_STREAM is used for TCP connection
    s.settimeout(2)
    conn=s.connect_ex((target,port))#connect with remote target tuple used ----connect IP addr and port
    #connect ex just gives the error number not the error msg when it fails
    if(not conn):
        print("Port {} is OPEN".format(port))
    s.close() #if not closed it uses resourses,security risks and compatibility issues(unexpected behaviour)

#to scan all ports in that range
for port in range(start_port,end_port+1):
    #we have to create a seperate socket connection for each port
    #now to make it faster we will use threading running all the ports at the same time
    thread=threading.Thread(target=scan_port,args=(port,))#as we have to give port as tuple
    thread.start()
end_time=time.time()
print("TIME FOR SCANNING:",end_time-start_time)


    
