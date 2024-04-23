import os 

def ClearScreen():
    os.system("cls" if os.name == "nt" else "clear")

class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""
    
    def ChooseName(self):
        while True:
            name = input("Enter Your Name: ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name. Use letters only.")

    def ChooseSymbol(self, first_player_symbol=None):
        if first_player_symbol is None:
            while True:
                symbol = input(f"{self.name}, choose your symbol (X or O): ")
                if symbol.upper() == 'X' or symbol.upper() == 'O':
                    self.symbol = symbol.upper()
                    break
                print("Invalid symbol. Use 'X' or 'O' only.")
        else:
            if first_player_symbol.upper() == 'X':
                self.symbol = 'O'
            else:
                self.symbol = 'X'
            print(f"{self.name}, your symbol is {self.symbol}")

class Menu:
    def DisplayMainMenu(self):
        print("Welcome to Tic Tac Toe!")
        print("1. Start Game")
        print("2. Quit Game")
        while True:
            choice = input("Enter your choice (1 or 2): ")
            if choice in ['1', '2']:
                return choice
            else:
                print("Invalid input, please enter a number 1 or 2")
    
    def EndGameMenu(self):
        menu_text = """
Game is Over
1. Restart Game
2. Quit Game
Enter your choice (1 or 2): """
        while True:
            choice = input(menu_text)
            if choice in ['1', '2']:
                return choice
            else:
                print("Invalid input, please enter a number 1 or 2")


class Board:
    def __init__(self):
        self.board = [' ' for _ in range(9)]

    def DisplayBoard(self):
        ClearScreen()
        print('-------------')
        for i in range(3):
            print(f'| {self.board[i*3]} | {self.board[i*3+1]} | {self.board[i*3+2]} |')
            print('-------------')

    def UpdateBoard(self, position, symbol):
        if self.board[position-1] == ' ':
            self.board[position-1] = symbol
            return True
        else:
            return False
        
    def RemovFromBoard(self, position):
        self.board[position-1] = ' '

    def ResetBoard(self):
        self.board = [' ' for _ in range(9)]

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.items:
            return None
        return self.items.pop(0)
        
    def Count(self):
        return len(self.items)

class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.queue = Queue()
        self.cpIndex = 0

    def StartGame(self):
        choice = self.menu.DisplayMainMenu()
        if choice == "1":
            self.SetupPlayers()
            self.PlayGame()
        else:
            self.QuitGame()

    def SetupPlayers(self):
        first_player = self.players[0]
        first_player.ChooseName()
        first_player.ChooseSymbol()
        
        second_player = self.players[1]
        second_player.ChooseName()
        second_player.ChooseSymbol(first_player.symbol)

    def PlayGame(self):
         while True:
            self.PlayTurn()
            if self.CheckWin():
                winner = self.players[self.cpIndex -1].name
                print(f"{winner} wins!")
                choice = self.menu.EndGameMenu()
                if choice == "1":
                    self.RestartGame()
                else:
                    self.QuitGame()
                    break
            elif self.CheckTwoEmpty():
                self.board.RemovFromBoard(self.queue.dequeue())
                print("Game continues...")
                self.board.DisplayBoard()

    def RestartGame(self):
        self.board.ResetBoard()
        self.cpIndex = 0
        self.PlayGame()

    def PlayTurn(self):
        current_player = self.players[self.cpIndex]
        self.board.DisplayBoard()
        print(f"{current_player.name}, your turn ({current_player.symbol})")
        while True:
            try:
                cell_choice = int(input("Choose a cell (1-9): "))
                if 1 <= cell_choice <= 9 and self.board.UpdateBoard(cell_choice, current_player.symbol):
                    self.queue.enqueue(cell_choice)   
                    break
                else:
                    print("Invalid Move. Try again.")
            except ValueError:
                print("Please enter a number between 1-9.")
        self.SwitchPlayer()

    def CheckTwoEmpty(self):
        if self.queue.Count() == 8:
            return True

    def SwitchPlayer(self):
        self.cpIndex = 1 - self.cpIndex

    def CheckWin(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]] != ' ':
                return True
        return False
            
    def QuitGame(self):
        print("Thank you for playing :)")

game = Game()
game.StartGame()
