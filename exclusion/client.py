import socket
import json
import select
import sys
from enum import Enum

class State(Enum):
    AU_SOL = "AU_SOL"
    TAXI = 'TAXI'
    DECOLLAGE = "DECOLLAGE"
    EN_VOL = "EN_VOL"
    ATTERRISSAGE = "ATTERRISSAGE"


def create_client_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1',  65432))
    client_socket.setblocking(False)
    return client_socket

def send_proposal(client_socket):
    data = {
        'id': 720,
        'altitude': 3000,
        'fuel': 1000,
        'speed': 500,
        'distance': 5,
        'crew': 14,
        'passengers': 500,
        'level': 'medical',
        'state': str(State.EN_VOL),
        'requested_next_state': str(State.EN_VOL),
        'action': 'transition'
    }

    action = input("#Airplane : request transition to state : ")
    data['requested_next_state'] = action


    message = json.dumps(data)
    client_socket.sendall(message.encode('utf-8'))
    print("#Airplane : request sent awainting confirmation...")

def main_loop(client_socket):
    print("press p to send a proposal")
    while True:
        ready_to_read, _, _ = select.select([client_socket, sys.stdin], [], [], 1)
        for ready in ready_to_read:
            if ready == client_socket:
                try:
                    message = client_socket.recv(4096)
                    if message:
                        print(f"#Control : {message.decode('utf-8')}")
                    else:
                        print("Connexion fermée par le serveur")
                        return
                except Exception as e:
                    print(f"Erreur lors de la réception du message : {e}")
            elif ready == sys.stdin:
                user_input = sys.stdin.readline().strip()
                if user_input.lower() == 'p':
                    send_proposal(client_socket)

client_socket = create_client_socket()
main_loop(client_socket)
