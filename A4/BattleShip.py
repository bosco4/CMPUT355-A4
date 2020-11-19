'''
Sources: 
https://www.pluralsight.com/guides/different-ways-create-numpy-arrays
https://docs.python.org/3/library/functions.html
'''

import sys, numpy as np

class player:
    def __init__(self, ships, playerAttacks, playerGrid, playerStatus):
        self.ships = ships
        self.playerAttacks = playerAttacks
        self.playerGrid = playerGrid
        self.playerStatus = playerStatus

def main():
    
    # rules of the game
    rules = '''\nWelcome to BattleShip, this game is originonally played on four 10x10 boards
(two boards per player: one board for showing a player's attacks on his opponent's board, and the
other for housing the player's own ships). To play this game, players will:
    
    1) Place their ships on their own board.
    2) Take turns attacking their opponent by entering coordinates to simulate
        missle attacks (e.g. A1), and recording these attacks on their attack board.
    3) The player with no more live ships on their own board loses.
                
Good Luck!\n
            '''
    print(rules)
    
    # take inputted game mode and check for validity
    gModeRequirement = ['classic', 'salvo', 'realtime']
    environmentRequirement = ['pvp', 'pve']
    gMode = input('Please enter a game mode (classic, salvo, realtime), environment type (pvp, pve) and board-size (num <= 26).\ne.g. \'classic pvp 10\':\n').lower()
    gMode = gMode.split()

    while len(gMode) != 3 or int(gMode[2]) > 26 or isinstance(int(gMode[2]), int) == False or gMode[0] not in gModeRequirement or gMode[1] not in environmentRequirement:
        gMode = input('Please enter a correct input mentioned above.\n').lower()
        gMode = gMode.split()
    
    # initialize players
    ships = ['carrier', 'battleship', 'cruiser', 'submarine', 'destroyer']
    playerAttacks = []
    playerGrid = np.zeros((int(gMode[2]), int(gMode[2])))
    # determines if player2 is an npc or player
    playerStatus = True if gMode[1] == 'pvp' else False
    player1 = player(ships, playerAttacks, playerGrid, True) 
    player2 = player(ships, playerAttacks, playerGrid, playerStatus)

    # initalize game choice
    if gMode[0] == 'classic':
        classic(player1, player2)
    elif gMode[0] == 'salvo':
        pass
    elif gMode[0] == 'realtime':
        pass

def classic(player1, player2):
    placeShips(player1, player2)

# set up the board (grid) for both players
def placeShips(player1, player2):
    print('\nPlayer 1:')
    print('Please place your ships using a grid coordinate system (e.g. Carrier A1 A6)\n')
    showGrid(player1.playerGrid)    

# show a player's grid
def showGrid(grid):
    
    ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    alpha = ALPHABET[:len(grid)]
    row = 0
    rowStr = ' ' + alpha[row] + ' |'
    separater = '---|'
    numberRow = '   |'
    
    # print number row (topmost row)
    for j in range(1, len(grid)+1):
        
        # construct number row
        if j < len(grid) and j < 10:
            numberRow += ' ' + str(j) + ' |'
            separater += '---|'
        else:
            numberRow += ' ' + str(j) + '|'
            separater += '---|'
        
        if j == len(grid):
            print(numberRow)
            print(separater)
            separater = '---|'
    
    # print rows with letters and player ship positions 
    for i in range( len(grid)*len(grid) ):
        
        # print each row row
        if i % (len(grid)) == 0 and i != 0:
            print(rowStr)
            print(separater)
            row += 1
            rowStr = ' ' + alpha[row] + ' |'
            separater = '---|'

        # construct grid based on a player's array values
        if grid[row][i%(len(grid))] != 0:
            rowStr += ' O |'
            separater += '---|'
        else:
            rowStr += '   |'
            separater += '---|'
        
        # print the last row
        if i == ( len(grid)*len(grid) )-1:
            print(rowStr)
            print(separater)
            
    
if __name__ == "__main__":
    main()