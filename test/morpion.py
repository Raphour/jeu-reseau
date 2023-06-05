import tkinter as tk
from tkinter import messagebox


# Fonction pour vérifier si un joueur a gagné
def check_win(player):
    # Vérifier les lignes
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Vérifier les colonnes
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Vérifier les diagonales
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False


# Fonction pour gérer le clic sur une case
def cell_clicked(row, col):
    global current_player

    # Vérifier si la case est déjà occupée
    if board[row][col] != "":
        return

    # Mettre à jour la case avec le symbole du joueur actuel
    board[row][col] = current_player
    buttons[row][col].config(text=current_player)

    # Vérifier si le joueur actuel a gagné
    if check_win(current_player):
        messagebox.showinfo("Fin de partie", f"Le joueur {current_player} a gagné !")
        reset_game()
        return

    # Vérifier s'il y a match nul
    if all(all(cell != "" for cell in row) for row in board):
        messagebox.showinfo("Fin de partie", "Match nul !")
        reset_game()
        return

    # Changer de joueur
    current_player = "O" if current_player == "X" else "X"


# Fonction pour réinitialiser le jeu
def reset_game():
    global current_player

    # Réinitialiser le tableau et les boutons
    board = [["" for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", state=tk.NORMAL)

    # Définir le joueur de départ
    current_player = "X"


# Création de la fenêtre principale
window = tk.Tk()
window.title("Jeu de Morpion")

# Création des boutons pour chaque case
buttons = []
for row in range(3):
    button_row = []
    for col in range(3):
        button = tk.Button(window, text="", width=10, height=5,
                           command=lambda r=row, c=col: cell_clicked(r, c))
        button.grid(row=row, column=col, padx=5, pady=5)
        button_row.append(button)
    buttons.append(button_row)

# Initialisation du tableau et du joueur actuel
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"

# Bouton de réinitialisation
reset_button = tk.Button(window, text="Réinitialiser", command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

# Lancement de la boucle principale
window.mainloop()
