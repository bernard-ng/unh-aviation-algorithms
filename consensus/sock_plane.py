import socket
import select
import json

HOST = '127.0.0.1'  # Adresse du serveur
PORT = 65432  # Port d'écoute du serveur (non privilégié)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}
proposals = []


def receive_message(client_socket):
    try:
        message = client_socket.recv(4096)
        if not message:
            return False
        return json.loads(message.decode('utf-8'))
    except:
        return False


def send_message_to_all(message):
    for client_socket in clients:
        client_socket.send(json.dumps(message).encode('utf-8'))


def consensus(proposals):
    occurrences = {}

    # Traverse the array to count occurrences of each element
    for element in proposals:
        occurrences[element] = occurrences.get(element, 0) + 1

    # Find the most common element
    most_common = None
    max_occurrences = 0

    for element, count in occurrences.items():
        if count >= max_occurrences:
            most_common = element
            max_occurrences = count

    return most_common


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]}")
        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # Traitement de la proposition de consensus
            if message['type'] == 'select_target':
                proposals.append(message['data'])
                print(f"Received proposal for target: {message['data']}")

                message = "Received proposal wait for consensus"
                notified_socket.send(message.encode())

                if len(proposals) == len(clients):
                    consensus = consensus(proposals)
                    decision_message = {"type": "decision", "data": consensus}
                    send_message_to_all(decision_message)
                    print("Consensus : ", consensus)

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
