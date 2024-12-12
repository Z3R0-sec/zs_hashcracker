from pwn import *
import sys
import hashlib
from termcolor import colored

if len(sys.argv) < 3 or len(sys.argv) > 4:
    print(colored("Invalid arguments", "red", attrs=["bold"]))
    print(colored("Usage: {} <hash_type> <hash_value> [wordlist]".format(sys.argv[0]), "yellow"))
    exit()

hash_type = sys.argv[1].lower()
wanted_hash = sys.argv[2]
password_file = sys.argv[3] if len(sys.argv) == 4 else "passwords.txt"
attempts = 0

def calculate_hash(password, hash_type):
    hash_object = hashlib.new(hash_type)
    hash_object.update(password.encode('latin-1'))
    return hash_object.hexdigest()

try:
    with open(password_file, "r", encoding='latin-1') as password_list:
        passwords = password_list.readlines()
except FileNotFoundError:
    print(colored(f"Error: Wordlist file '{password_file}' not found!", "red", attrs=["bold"]))
    exit()

with log.progress(colored(f"Attempting to crack: {wanted_hash}!", "cyan", attrs=["bold"])) as p:
    for password in passwords:
        password = password.strip("\n") 
        if not password: 
            continue
        password_hash = calculate_hash(password, hash_type)  
        p.status(colored(f"[{attempts}] Trying password: {password}", "blue"))

        if password_hash == wanted_hash:
            p.success(colored(f"Password found after {attempts} attempts!", "green", attrs=["bold"]))
            print(colored(f"'{password}' hashes to {wanted_hash}", "magenta", attrs=["bold"]))
            exit(0)
        
        attempts += 1

    p.failure(colored(f"Password hash not found after {attempts} attempts!", "red", attrs=["bold"]))