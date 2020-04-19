import requests

import sys
import json
import datetime

node = "http://localhost:5000"

def change_id():
    id = input("New ID:")
    f = open("my_id.txt", "w")
    f.write(id)

def get_transactions(id):
    r = requests.get(url=node + "/chain")
    chain = r.json()['chain']
    transactions = [ (t, c['timestamp']) for c in chain for t in c['transactions'] if t['sender'] == id or t['recipient'] == id]
    return transactions
    
def display_balance(id):
    transactions = [ t[0] for t in get_transactions(id)]
    sent = sum([ t['amount'] for t in transactions if t['sender'] == id ])
    received = sum([ t['amount'] for t in transactions if t['recipient'] == id ])
    print(f"You have ${received - sent}.\n")

def display_transactions(id):
    transactions = get_transactions(id)
    
    for t, timestamp in transactions:
        value = datetime.datetime.fromtimestamp(timestamp)
        print(f"On {value:%Y-%m-%d %H:%M:%S}:")
        if t['sender'] == id:
            print(f"Sent ${t['amount']} to {t['recipient']}.\n")
        elif t['recipient'] == id:
            print(f"Recieved ${t['amount']} from {t['sender']}.\n")

i = ""
while i not in ['q', 'quit']:
    try:
        f = open("my_id.txt", "r")
        id = f.read()
    except IOError:
        id = input("No saved id, please enter one:")
        f = open("my_id.txt", "w")
        f.write(id)
    finally:
        f.close()

    print("What would you like to do? You can")
    print("* [C]hange your id")
    print("* [D]isplay your current balance")
    print("* [S]ee all transactions")
    print("* [Q]uit")
    i = input(": ").lower()

    if i in ['c']:
        change_id()
    elif i in ['d']:
        display_balance(id)
    elif i in ['s']:
        display_transactions(id)
    