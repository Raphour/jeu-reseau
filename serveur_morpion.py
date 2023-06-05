import socket
import random
import multiprocessing

# Fonction de gestion d'une partie du jeu
def play_game(player1, player2):
    # Sélectionner aléatoirement le joueur qui commence
    current_player = random.choice([player1, player2])
    player1.send(f"Vous êtes le joueur {player1_symbol}".encode())
    player2.send(f"Vous êtes le joueur {player2_symbol}".encode())

    while True:
        # Envoyer la grille et le tour du joueur actuel
        player1.send(f"{board}\nTour du joueur : {current_player}\n".encode())
        player2.send(f"{board}\nTour du joueur : {current_player}\n".encode())

        # Recevoir les coordonnées du coup du joueur actuel
        if current_player == player1:
            coordinates = player1.recv(1024).decode().split(',')
        else:
            coordinates = player2.recv(1024).decode().split(',')

        row, col = int(coordinates[0]), int(coordinates[1])
        symbol = player1_symbol if current_player == player1 else player2_symbol

        # Mettre à jour la grille
        board[row][col] = symbol

        # Vérifier si le joueur actuel a gagné
        if check_winner(board, symbol):
            player1.send("Vous avez gagné !".encode())
            player2.send("Vous avez perdu !".encode())
            break

        # Vérifier s'il y a un match nul
        if check_draw(board):
            player1.send("Match nul !".encode())
            player2.send("Match nul !".encode())
            break

        # Changer de joueur
        current_player = player2 if current_player == player1 else player1

    # Fermer les connexions
    player1.close()
    player2.close()


# Vérifier s'il y a un gagnant
def check_winner(board, symbol):
    # Vérifier les lignes
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == symbol:
            return True

    # Vérifier les colonnes
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == symbol:
            return True

    # Vérifier les diagonales
    if board[0][0] == board[1][1] == board[2][2] == symbol:
        return True
    if board[0][2] == board[1][1] == board[2][0] == symbol:
        return True

    return False


# Vérifier s'il y a un match nul
def check_draw(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return False
    return True


# Création de la grille de jeu
board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

# Création du socket du serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8000))
server_socket.listen(2)

print("En attente de connexions des joueurs...")

# Attente des connexions des joueurs
player1, address1 = server_socket.accept()
player2, address2 = server_socket.accept()

print("Deux joueurs connectés.")

# Assigner des symboles aléatoires aux joueurs
player1_symbol = 'X'
player2_symbol = 'O'

# Créer des processus pour exécuter les parties du jeu
process1 = multiprocessing.Process(target=play_game, args=(player1, player2))
process2 = multiprocessing.Process(target=play_game, args=(player2, player1))

# Démarrer les processus
process1.start()
process2.start()

# Attendre la fin des processus
process1.join()
process2.join()

# Fermer le socket du serveur
server_socket.close()
