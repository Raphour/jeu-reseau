import socket

# Création du socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Liaison du socket à une adresse IP et un port
server_address = ('localhost', 8000)
server_socket.bind(server_address)

print("Le serveur est prêt à écouter...")

while True:
    # Attendre la réception de données
    data, address = server_socket.recvfrom(1024)

    # Afficher les données reçues
    print(f"Reçu depuis {address}: {data.decode()}")

    # Envoyer une réponse au client
    response = "Message bien reçu!"
    server_socket.sendto(response.encode(), address)