import socket
import tkinter as tk
import multiprocessing

# Fonction pour mettre à jour la grille et afficher le tour du joueur
def update_board():
    while True:
        # Recevoir la grille et le tour du joueur actuel
        message = server_socket.recv(1024).decode()
        board_str, player_turn = message.split('\nTour du joueur : ')
        board = [row.split('|') for row in board_str.split('\n')]

        # Mettre à jour la grille
        for i in range(3):
            for j in range(3):
                button = buttons[i][j]
                button.config(text=board[i][j])
                button.config(state=tk.DISABLED)

        # Afficher le tour du joueur actuel
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"Tour du joueur : {player_turn}\n")

# Fonction pour gérer le clic sur une case de la grille
def handle_click(row, col):
    button = buttons[row][col]
    if button["state"] == tk.NORMAL:
        coordinates = f"{row},{col}".encode()
        server_socket.send(coordinates)
        update_board()

# Création de la fenêtre du client
window = tk.Tk()
window.title("Jeu de Morpion")
text_area = tk.Text(window, height=10, width=30)
text_area.grid(row=0, column=0, columnspan=3)

# Connexion au serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(('localhost', 8000))

# Création des boutons de la grille
buttons = []
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(window, text=' ', width=10, height=5,
                           command=lambda r=i, c=j: handle_click(r, c))
        button.grid(row=i+1, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Démarrer un processus séparé pour mettre à jour le jeu en continu
process = multiprocessing.Process(target=update_board)
process.start()

window.mainloop()

# Fermeture de la connexion
server_socket.close()
