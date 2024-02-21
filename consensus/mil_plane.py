import socket
import json
import select
import sys

def create_client_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1',  65432))  # Remplacez 'adresse_serveur' et 'port_serveur'
    client_socket.setblocking(False)
    return client_socket

def send_proposal(client_socket):
    target_to_select = input("Entrez la cible à sélectionner : ")
    message = json.dumps({"type": "select_target", "data": target_to_select})
    client_socket.sendall(message.encode('utf-8'))
    print("Proposition envoyée. Continuez à écouter les messages...")

def main_loop(client_socket):
    print("En attente de messages... (Appuyez sur 'p' puis 'Entrée' pour proposer une cible)")
    while True:
        ready_to_read, _, _ = select.select([client_socket, sys.stdin], [], [], 1)
        for ready in ready_to_read:
            if ready == client_socket:
                try:
                    message = client_socket.recv(4096)
                    if message:
                        print(f"Message reçu : {message.decode('utf-8')}")
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
