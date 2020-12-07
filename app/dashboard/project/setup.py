#!/usr/bin/python3
import subprocess
import secrets

# Initial setup for the server, generate migrations and such

# Create the secret key
try:
    with open('/app/data/secret_key.txt') as kf:
        print('The secret key already exists, skipping')
except:
    with open('/app/data/secret_key.txt', 'w') as kf:
        # Generate a random secret
        sk = secrets.token_hex(25)
        kf.write(sk)


# Make the migrations
subprocess.run(['python3', 'manage.py', 'makemigrations'], cwd='/app/')
subprocess.run(['python3', 'manage.py', 'migrate'], cwd='/app/')
