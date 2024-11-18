# Function to print the game board
def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

# Function to check if a player has won
def check_winner(board, player):
    # Check rows, columns, and diagonals
    for row in board:
        if all([spot == player for spot in row]):
            return True
    
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True

    return False

# Function to check for a draw
def check_draw(board):
    return all([spot != ' ' for row in board for spot in row])

# Main function to run the game
def tic_tac_toe():
    # Initialize the board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    turn = 0
    
    while True:
        print_board(board)
        current_player = players[turn % 2]
        print(f"Player {current_player}'s turn.")
        
        # Get row and column input from the player
        try:
            row = int(input("Enter row (0, 1, or 2): "))
            col = int(input("Enter column (0, 1, or 2): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        # Check if the spot is already taken
        if board[row][col] != ' ':
            print("Spot already taken! Choose another.")
            continue

        # Place the player's mark on the board
        board[row][col] = current_player

        # Check if the current player has won
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        # Check if the game is a draw
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch turns
        turn += 1

# Run the game
tic_tac_toe()
