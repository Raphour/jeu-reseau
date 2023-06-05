import socket

# Création du socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Adresse du serveur
server_address = ('localhost', 8000)

# Envoi de données au serveur
while True:

    message = input("Message : ")
    if message.replace(" ", "") != "":

        client_socket.sendto(message.encode(), server_address)

        # Attente de la réponse du serveur
        response, _ = client_socket.recvfrom(1024)

        # Afficher la réponse reçue
        print("Réponse du serveur:", response.decode())
    else:
        break

# Fermeture du socket client
client_socket.close()