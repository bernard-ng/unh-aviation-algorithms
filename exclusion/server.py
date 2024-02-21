import socket
import select
import json

HOST = '0.0.0.0' 
PORT = 65432 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}
proposals = []

def calculate_cost(parameters):
    cost_altitude = parameters.get('altitude', 0) * 0.1
    cost_fuel = parameters.get('fuel', 0) * 0.05
    cost_speed = parameters.get('speed', 0) * 0.2
    cost_distance = parameters.get('distance', 0) * 0.3
    cost_crew = parameters.get('crew', 0) * 10
    cost_passengers = parameters.get('passengers', 0) * 5

    level = parameters.get('level', '')
    cost_level = 0
    if level == 'medical':
        cost_level = 50
    elif level == 'commercial':
        cost_level = 30
    elif level == 'cargo':
        cost_level = 20

    total_cost = (
        cost_altitude +
        cost_fuel +
        cost_speed +
        cost_distance +
        cost_crew +
        cost_passengers +
        cost_level
    )

    return total_cost

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


def exclusion(proposals):
    costs = {}
    hightest_id = -1

    for proposal in proposals:
        cost = calculate_cost(proposal)
        costs[proposal['id']] = cost

        if proposal['id'] > hightest_id:
            hightest_id = proposal['id']

        print(f"Airplane {proposal['id']} cost is {cost}")

    for proposal in proposals:
        if proposal['id'] == hightest_id:
            proposal['socket'].send("ACCEPTED".encode())
        else:
            proposal['socket'].send("REJECTED, request to receive instructions...".encode())
    

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
            print(message)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # Traitement de la proposition de consensus
            if message['action'] == 'transiontion':
                message['socket'] = notified_socket 
                proposals.append(message)
                print(f"Airplane {message['id']} in {message['state']} requests to {message['requested_next_state']}")

                message = "Received request please wait for confirmation"
                notified_socket.send(message.encode())

                if len(proposals) == len(clients):
                    exclusion(proposals)
    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
