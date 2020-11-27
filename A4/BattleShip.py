'''
Sources: 
https://www.pluralsight.com/guides/different-ways-create-numpy-arrays
https://docs.python.org/3/library/functions.html
https://www.w3schools.com/python/ref_string_isalnum.asp
https://www.geeksforgeeks.org/python-check-if-element-exists-in-list-of-lists/
https://www.geeksforgeeks.org/python-how-to-get-subtraction-of-tuples/
https://www.kammerl.de/ascii/AsciiSignature.php
https://www.asciiart.eu/logos/biohazards
https://www.asciiart.eu/weapons/explosives
http://www.asciiworld.com/-Death-Co-.html
'''

import os, sys, numpy as np, random, itertools, copy

ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
clear = lambda: os.system('cls')

class player:
    def __init__(self, ships, Attacks, Grid, shipPositions, Status, prevAttacks):
        self.ships = ships
        self.Attacks = Attacks
        self.Grid = Grid
        self.shipPositions = shipPositions
        self.Status = Status
        self.prevAttacks = prevAttacks
'''
ships: list of tuples of (shipName, spacesItTakes)
Attacks: grid (list of list) containing player attacked coordinates
Grid: grid (list of list) showing where a player's ships are
shipPositions: dictionary of [shipName] = list of tuples of ship's coordinates
Status: describing if a player is a npc or person (npc, player1, player2) = (0, 1, 2) 
prevAttacks: to keep track of previous npc attacks
'''

def main():
    
    # rules of the game
    rules = '''\nWelcome to BattleShip, this game is originonally played on four 10x10 boards
(two boards per player: one board for showing a player's attacks on his opponent's board, and the
other for housing the player's own ships). To play this game, both players will:
    
    1) Place their ships on their own board.
    2) Take turns attacking their opponent by entering coordinates to simulate
        missle attacks (e.g. A1), and recording their attacks on their attack board.
    3) The player with no more live ships on their own board loses.
                
NOTE: Please play on full screen on terminal for better visual.

Good Luck!
            '''
    print(rules)
    
    # take inputted game mode and check for validity
    gModeRequirement = ['classic', 'salvo', 'realtime']
    environmentRequirement = ['pvp', 'pve']
    gMode = input('Please enter a game mode (classic, salvo, realtime), environment type (pvp, pve) and\nboard-size (5 <= board-size <= 26).\n(e.g. \'classic pvp 10\') Game Mode:').lower()
    if gMode.lower() == 'quit':
        sys.exit()
    gMode = gMode.split()

    # check for incorrect inputs
    while len(gMode) != 3 or gMode[2].isnumeric() == False or int(gMode[2]) > 26 or int(gMode[2]) < 5 or gMode[0] not in gModeRequirement or gMode[1] not in environmentRequirement:
        gMode = input('Please enter a correct input mentioned above.:').lower()
        if gMode == 'quit':
            sys.exit()
        gMode = gMode.split()
    
    # initialize players
    ships = [('carrier', 5), ('battleship', 4), ('cruiser', 3), ('submarine', 3), ('destroyer', 2)]
    shipPositions1 = {}
    shipPositions2 = {}
    shipGrid1 = np.zeros((int(gMode[2]), int(gMode[2])))  
    shipGrid2 = np.zeros((int(gMode[2]), int(gMode[2])))
    attackGrid1 = np.zeros((int(gMode[2]), int(gMode[2])))
    attackGrid2 = np.zeros((int(gMode[2]), int(gMode[2])))
    Status = 2 if gMode[1] == 'pvp' else 0
    
    '''
    gridSize = len(player.Grid)
    gridSpaces = list(itertools.product(range(gridSize),range(gridSize)))
    player.prevAttacks = copy.deepcopy(gridSpaces)
    '''
    prevAttacks=list(itertools.product(range(int(gMode[2])),range(int(gMode[2]))))
    
    player1 = player(ships, attackGrid1, shipGrid1, shipPositions1, 1, prevAttacks) 
    player2 = player(ships, attackGrid2, shipGrid2, shipPositions2, Status, prevAttacks)

    # initalize game choice
    if gMode[0] == 'classic':
        classic(1, player1, player2)
    elif gMode[0] == 'salvo':
        classic(2, player1, player2)
    elif gMode[0] == 'realtime':
        print('Mode has not yet been implemented.')


def classic(mode, player1, player2):
    planningPhase()
    getShipCoords(player1)
    clearScreen()
    
    # generate player2 ship coords for PvE or PvP 
    if player2.Status == 0:
        generateShipCoords(player2)
    else:
        getShipCoords(player2)
        clearScreen()
    
    attackPhase()
    gameCondition = True
    while gameCondition == True:
        # player1 attacks
        attackCoord(mode, player1, player2)
        if any(1 in row for row in player2.Grid) == False:
            lose1='''
  _____          __  __ ______    ______      ________ _____      _____  _           __     ________ _____    __  __          _______ _   _  _____  
 / ____|   /\   |  \/  |  ____|  / __ \ \    / /  ____|  __ \    |  __ \| |        /\\\ \   / /  ____|  __ \  /_ | \ \        / /_   _| \ | |/ ____| 
| |  __   /  \  | \  / | |__    | |  | \ \  / /| |__  | |__) |   | |__) | |       /  \\\ \_/ /| |__  | |__) |  | |  \ \  /\  / /  | | |  \| | (___   
| | |_ | / /\ \ | |\/| |  __|   | |  | |\ \/ / |  __| |  _  /    |  ___/| |      / /\ \\\   / |  __| |  _  /   | |   \ \/  \/ /   | | | . ` |\___ \  
| |__| |/ ____ \| |  | | |____  | |__| | \  /  | |____| | \ \ _  | |    | |____ / ____ \| |  | |____| | \ \   | |    \  /\  /   _| |_| |\  |____) | 
 \_____/_/    \_\_|  |_|______|  \____/   \/   |______|_|  \_(_) |_|    |______/_/    \_\_|  |______|_|  \_\  |_|     \/  \/   |_____|_| \_|_____(_)
            
            '''
            print(lose1)
            break
        
        # player2 attacks
        attackCoord(mode, player2, player1)
        if any(1 in row for row in player1.Grid) == False:
            lose2='''
  _____          __  __ ______    ______      ________ _____      _____  _           __     ________ _____    ___   __          _______ _   _  _____  
 / ____|   /\   |  \/  |  ____|  / __ \ \    / /  ____|  __ \    |  __ \| |        /\\\ \   / /  ____|  __ \  |__ \  \ \        / /_   _| \ | |/ ____| 
| |  __   /  \  | \  / | |__    | |  | \ \  / /| |__  | |__) |   | |__) | |       /  \\\ \_/ /| |__  | |__) |    ) |  \ \  /\  / /  | | |  \| | (___   
| | |_ | / /\ \ | |\/| |  __|   | |  | |\ \/ / |  __| |  _  /    |  ___/| |      / /\ \\\   / |  __| |  _  /    / /    \ \/  \/ /   | | | . ` |\___ \  
| |__| |/ ____ \| |  | | |____  | |__| | \  /  | |____| | \ \ _  | |    | |____ / ____ \| |  | |____| | \ \   / /_     \  /\  /   _| |_| |\  |____) | 
 \_____/_/    \_\_|  |_|______|  \____/   \/   |______|_|  \_(_) |_|    |______/_/    \_\_|  |______|_|  \_\ |____|     \/  \/   |_____|_| \_|_____(_)        
            
            '''
            print(lose2)
            break

# prints ascii
def attackPhase():
    phase = '''
       _______ _______       _____ _  __  _____  _    _           _____ ______   ____  ______ _____ _____ _   _  _____ 
    /\|__   __|__   __|/\   / ____| |/ / |  __ \| |  | |   /\    / ____|  ____| |  _ \|  ____/ ____|_   _| \ | |/ ____|
   /  \  | |     | |  /  \ | |    | ' /  | |__) | |__| |  /  \  | (___ | |__    | |_) | |__ | |  __  | | |  \| | (___  
  / /\ \ | |     | | / /\ \| |    |  <   |  ___/|  __  | / /\ \  \___ \|  __|   |  _ <|  __|| | |_ | | | | . ` |\___ \ 
 / ____ \| |     | |/ ____ \ |____| . \  | |    | |  | |/ ____ \ ____) | |____  | |_) | |___| |__| |_| |_| |\  |____) |
/_/    \_\_|     |_/_/    \_\_____|_|\_\ |_|    |_|  |_/_/    \_\_____/|______| |____/|______\_____|_____|_| \_|_____/ 
    
Each player will now take turns to enter coordinates on their attack board
to attempt to sink their opponents ships. Somewhat similar to the planning phase, 
enter a single coordinate to attack your opponent (e.g. A1).
    
====>Player1 will start first.'''
    print(phase)
    clearScreen()

# npc generates its own attack coordinates
def generateAttackCoords(mode, player):
    attackCoord = []
    
    if mode == 1:
        coordLength = 1
    elif mode == 2:
        coordLength = len(player.shipPositions)

    # check if random attackCoord is valid (not already hit)
    for i in range(coordLength):
        while True:
            coord = random.choice(player.prevAttacks)
            if player.Attacks[coord[0]][coord[1]] == 0:
                attackCoord.append(ALPHABET[coord[0]] + str(coord[1]+1))
                player.prevAttacks.remove(coord)
                break
    
    player2Strike(attackCoord)
    
    return attackCoord

def player2Strike(attackCoord):
    warning = '''

////////////////////////////////////////////////////////////////////
|       __          __     _____  _   _ _____ _   _  _____         |
|       \ \        / /\   |  __ \| \ | |_   _| \ | |/ ____|        |
|        \ \  /\  / /  \  | |__) |  \| | | | |  \| | |  __         |
|         \ \/  \/ / /\ \ |  _  /| . ` | | | | . ` | | |_ |        |
|          \  /\  / ____ \| | \ \| |\  |_| |_| |\  | |__| |        |
|           \/  \/_/    \_\_|  \_\_| \_|_____|_| \_|\_____|        |
|                                                                  |
///////////////////////////////////////////////////////////////////

                            uuuuuuu
                        uu$$$$$$$$$$$uu
                     uu$$$$$$$$$$$$$$$$$uu
                    u$$$$$$$$$$$$$$$$$$$$$u
                   u$$$$$$$$$$$$$$$$$$$$$$$u
                  u$$$$$$$$$$$$$$$$$$$$$$$$$u
                  u$$$$$$$$$$$$$$$$$$$$$$$$$u
                  u$$$$$$"   "$$$"   "$$$$$$u
                  "$$$$"      u$u       $$$$"
                   $$$u       u$u       u$$$
                   $$$u      u$$$u      u$$$
                    "$$$$uu$$$   $$$uu$$$$"
                     "$$$$$$$"   "$$$$$$$"
                       u$$$$$$$u$$$$$$$u
                        u$"$"$"$"$"$"$u
            uuu         $$u$ $ $ $ $u$$       uuu
           u$$$$         $$$$$u$u$u$$$       u$$$$
            $$$$$uu       "$$$$$$$$$"     uu$$$$$$
          u$$$$$$$$$$$uu     """""    uuuu$$$$$$$$$$
          $$$$"""$$$$$$$$$$uuu   uu$$$$$$$$$"""$$$"
           """      ""$$$$$$$$$$$uu ""$"""
                    uuuu ""$$$$$$$$$$uuu
            u$$$uuu$$$$$$$$$uu ""$$$$$$$$$$$uuu$$$
            $$$$$$$$$$""""           ""$$$$$$$$$$$"
            "$$$$$"                      ""$$$$""
                $$$"                         $$$$"
    
    Enemy incoming at these coordinate(s), prepare yourself!:'''
    attackedCoords = '    '
    for coord in attackCoord:
        attackedCoords += coord  + ' '
    attackedCoords += '\n'
    print(warning)
    print(attackedCoords)
    #clearScreen()
    
    
# gets a player to attack a enemy cordinate
def attackCoord(mode, attacker, reciever):
    alpha = ALPHABET[:len(attacker.Grid)]
    
    # if player is human, ask for attack coordinates
    if attacker.Status > 0:
        # two player game? (player2.Status == 2)
        if reciever.Status > 0:
            if attacker.Status == 1:
                cmd = '''
                
     _____  _           __     ________ _____  __ 
    |  __ \| |        /\\\ \   / /  ____|  __ \/_ |
    | |__) | |       /  \\\ \_/ /| |__  | |__) || |
    |  ___/| |      / /\ \\\   / |  __| |  _  / | |
    | |    | |____ / ____ \| |  | |____| | \ \ | |
    |_|    |______/_/    \_\_|  |______|_|  \_\|_|
           _______ _______       _____ _  ___ 
        /\|__   __|__   __|/\   / ____| |/ / |
       /  \  | |     | |  /  \ | |    | ' /| |
      / /\ \ | |     | | / /\ \| |    |  < | |
     / ____ \| |     | |/ ____ \ |____| . \|_|
    /_/    \_\_|     |_/_/    \_\_____|_|\_(_)
    
    Player{}, your attack board holds all your previous attacks and your position grid
    holds all your placed ships. 

        Are you ready?
            
        Press enter to view these boards in private.'''
                cmd = input(cmd.format(attacker.Status))
                if cmd.lower() == 'quit':
                    sys.exit()
            else:
                
                cmd = '''
                
     _____  _           __     ________ _____  ___  
    |  __ \| |        /\\\ \   / /  ____|  __ \|__ \ 
    | |__) | |       /  \\\ \_/ /| |__  | |__) |  ) |
    |  ___/| |      / /\ \\\   / |  __| |  _  /  / / 
    | |    | |____ / ____ \| |  | |____| | \ \ / /_ 
    |_|    |______/_/    \_\_|  |______|_|  \_\____|
           _______ _______       _____ _  ___ 
        /\|__   __|__   __|/\   / ____| |/ / |
       /  \  | |     | |  /  \ | |    | ' /| |
      / /\ \ | |     | | / /\ \| |    |  < | |
     / ____ \| |     | |/ ____ \ |____| . \|_|
    /_/    \_\_|     |_/_/    \_\_____|_|\_(_)
    
    Player{}, your attack board holds all your previous attacks and your position grid
    holds all your placed ships. 

        Are you ready?
            
        Press enter to view these boards in private.'''
                cmd = input(cmd.format(attacker.Status))
                if cmd.lower() == 'quit':
                    sys.exit()
        
        # player1 attacks always when player2 is a npc
        else:
            
            cmd = '''
 _____  _           __     ________ _____  __ 
|  __ \| |        /\\\ \   / /  ____|  __ \/_ |
| |__) | |       /  \\\ \_/ /| |__  | |__) || |
|  ___/| |      / /\ \\\   / |  __| |  _  / | |
| |    | |____ / ____ \| |  | |____| | \ \ | |
|_|    |______/_/    \_\_|  |______|_|  \_\|_|
       _______ _______       _____ _  ___ 
    /\|__   __|__   __|/\   / ____| |/ / |
   /  \  | |     | |  /  \ | |    | ' /| |
  / /\ \ | |     | | / /\ \| |    |  < | |
 / ____ \| |     | |/ ____ \ |____| . \|_|
/_/    \_\_|     |_/_/    \_\_____|_|\_(_)


Player{}, attack quickly before the enemy destroys you!'''
            print(cmd.format(attacker.Status))
            
        print('\nPlayer{} Attack Board:'.format(attacker.Status))
        showGrid(attacker.Attacks)
        print('\nPlayer{} Position Board:'.format(attacker.Status))
        showGrid(attacker.Grid)
        # size of possible coordinate
        coordLength = len(str(len(attacker.Grid)))+1
        while True:
            valid = True
            if mode == 1:
                attackCoord = input('\nEnter a valid coordinate you wish attack:').upper().split()
                if attackCoord[0].lower() == 'quit':
                    sys.exit()
                if len(attackCoord) != 1:
                    valid = False
            elif mode == 2:
                attackCoord = input('\nEnter {} valid coordinates you wish attack:'.format(len(attacker.shipPositions))).upper().split()
                if attackCoord[0].lower() == 'quit':
                    sys.exit()
                if len(attackCoord) != len(attacker.shipPositions):
                    valid = False
            
            for coord in attackCoord:
                if (len(coord) <= coordLength) == False or (len(coord) >= coordLength) == False or coord[0] not in alpha or coord[1:].isnumeric() == False or (int(coord[1:]) >= 1) == False or (int(coord[1:]) <= len(attacker.Grid)) == False or attacker.Attacks[alpha.index(coord[0])][int(coord[1])-1] == 2 or attacker.Attacks[alpha.index(coord[0])][int(coord[1])-1] == 3:
                    valid = False
            if valid == True:
                break
    
    # npc generates an attack       
    else:
        attackCoord = generateAttackCoords(mode, attacker)
    
    for coord in attackCoord:
        coord = ( alpha.index(coord[0]), int(coord[1])-1 )
        hitCondition(attacker, coord, reciever)
    clearScreen()

# check if attacked coordinate has hit or miss and add attack to players attack grid
def hitCondition(attacker, coord, reciever):
    hit = '''
                 _    _ _____ _______ _                 
 ______ ______  | |  | |_   _|__   __| |  ______ ______ 
|______|______| | |__| | | |    | |  | | |______|______|
 ______ ______  |  __  | | |    | |  | |  ______ ______ 
|______|______| | |  | |_| |_   | |  |_| |______|______|
                |_|  |_|_____|  |_|  (_)                
                
Asset Destroyed:               
                             ____
                     __,-~~/~    `---.
                   _/_,---(      ,    )
               __ /        <    /   )  \___
- ------===;;;'====------------------===;;;===----- -  -
                  \/  ~"~"~"~"~"~\~"~)~"/
                  (_ (   \  (     >    \)
                   \_( _ <         >_>'
                      ~ `-i' ::>|--"
                          I;|.|.|
                         <|i::|i|`.
                        (` ^'"`-' ")
---------------------------------------------------------
    '''
    
    miss = '''
                 __  __ _____  _____ _____ _                 
 ______ ______  |  \/  |_   _|/ ____/ ____| |  ______ ______ 
|______|______| | \  / | | | | (___| (___ | | |______|______|
 ______ ______  | |\/| | | |  \___ \\\___ \| |  ______ ______ 
|______|______| | |  | |_| |_ ____) |___) |_| |______|______|
                |_|  |_|_____|_____/_____/(_)                
                
Asset is still Active:

                     \|/   __/___            
                    __|___/______|           
            _______/_____\_______\_____     
            \              < < <       |    
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    '''
    
    # input miss or hit values for attacker.Attacks grid
    if reciever.Grid[coord[0]][coord[1]] == 1:
        print(hit)
        reciever.Grid[coord[0]][coord[1]] = -1
        attacker.Attacks[coord[0]][coord[1]] = 2
        # remove coordinates for an attacked ship and remove ship with no coordinates
        for ship in list(reciever.shipPositions.keys()):
            if coord in reciever.shipPositions[ship]:
                reciever.shipPositions[ship].remove(coord)
                # check if ship exists on enemy board after attack
                if not reciever.shipPositions[ship]:
                    sink ='''
    ===================================================
    ====Enemy {} has just been sunk, Good Hit!====
    ==================================================='''
                    print(sink.format(ship))
                    del reciever.shipPositions[ship]

    else:

        if attacker.Status == 0:
            
            enemyMiss = '''
Enemy has missed you! Don't celebrate yet, they're still out there....'''
            print(enemyMiss)

        print(miss)
        attacker.Attacks[coord[0]][coord[1]] = 3

# print ascii
def planningPhase():
    
    shipInfo = '''
 _____  _               _   _ _   _ _____ _   _  _____   _____  _    _           _____ ______   ____  ______ _____ _____ _   _  _____ 
|  __ \| |        /\   | \ | | \ | |_   _| \ | |/ ____| |  __ \| |  | |   /\    / ____|  ____| |  _ \|  ____/ ____|_   _| \ | |/ ____|
| |__) | |       /  \  |  \| |  \| | | | |  \| | |  __  | |__) | |__| |  /  \  | (___ | |__    | |_) | |__ | |  __  | | |  \| | (___  
|  ___/| |      / /\ \ | . ` | . ` | | | | . ` | | |_ | |  ___/|  __  | / /\ \  \___ \|  __|   |  _ <|  __|| | |_ | | | | . ` |\___ \ 
| |    | |____ / ____ \| |\  | |\  |_| |_| |\  | |__| | | |    | |  | |/ ____ \ ____) | |____  | |_) | |___| |__| |_| |_| |\  |____) |
|_|    |______/_/    \_\_| \_|_| \_|_____|_| \_|\_____| |_|    |_|  |_/_/    \_\_____/|______| |____/|______\_____|_____|_| \_|_____/     

There are 5 ships open to each player and here are the spaces they consume on the grid;
carrier: 5-spaces, battleship: 4-spaces, cruiser: 3-spaces, submarine: 3-spaces , destroyer: 2-spaces.

Each player will enter their ships into their respective position board. Once ships are placed their 
position can't be changed. 

====> Player1 will begin first.
    '''
    print(shipInfo)
    clearScreen()

# npc generates its own random ship coordinates
def generateShipCoords(player):
    #random.seed(10)
    player.shipPositions = {'carrier': [(0,1)], 'battleship': [], 'cruiser': [], 'submarine': [], 'destroyer' : []}
    spacesTaken = []

    # create list(np.array) of player.grid, np.array.dim(gridSize, gridSize)
    gridSize = len(player.Grid)
    gridSpaces = list(itertools.product(range(gridSize),range(gridSize)))
    npArray = np.asarray(gridSpaces, np.dtype('int,int') )
    npArray = npArray.reshape([gridSize, gridSize])
    coordGrid = npArray.tolist()
    coordGridTranspose = np.transpose(npArray).tolist()

    # find all horizontal/vertical placements per ship
    for ship in player.ships:

        shipSize = ship[1]
        maxGroup = (gridSize - shipSize) + 1
        horizontal = []
        vertical = []
        allPlacements = []
        # get all possible placements for a ship
        for j in range(gridSize):
            groupT = []
            group = []
            for i in range(maxGroup):
                group.append(coordGrid[j][i:i+shipSize])
                groupT.append(coordGridTranspose[j][i:i+shipSize])
            horizontal.extend(group)
            vertical.extend(groupT)

        # allPlacements points to horizontal, then extends
        allPlacements = horizontal
        allPlacements.extend(vertical)

        while True:
            valid = True
            index = random.randint(0,len(allPlacements)-1)
            if any(item in allPlacements[index] for item in spacesTaken):
                valid = False
            if valid == True:
                break
            
        spacesTaken.extend(allPlacements[index])
        
        for coord in allPlacements[index]:
            player.Grid[coord[0]][coord[1]] = 1
        
        player.shipPositions[ship[0]] = allPlacements[index]  

# get ship coordinates from a player and create their position board
def getShipCoords(player):
    if player.Status == 1:
        msg ='''
 _____  _           __     ________ _____  __ 
|  __ \| |        /\\\ \   / /  ____|  __ \/_ |
| |__) | |       /  \\\ \_/ /| |__  | |__) || |
|  ___/| |      / /\ \\\   / |  __| |  _  / | |
| |    | |____ / ____ \| |  | |____| | \ \ | |
|_|    |______/_/    \_\_|  |______|_|  \_\|_|

Please enter the set of coordinates for each ship within the grid (e.g. carrier, 5-spaces:A1 A5)\nNote: Each set of coordinates given must consume the correct amount of spaces on the grid.
        
        '''
    else:
        msg = '''
        
 _____  _           __     ________ _____  ___  
|  __ \| |        /\\\ \   / /  ____|  __ \|__ \ 
| |__) | |       /  \\\ \_/ /| |__  | |__) |  ) |
|  ___/| |      / /\ \\\   / |  __| |  _  /  / / 
| |    | |____ / ____ \| |  | |____| | \ \ / /_ 
|_|    |______/_/    \_\_|  |______|_|  \_\____|

Please enter the set of coordinates for each ship within the grid (e.g. carrier, 5-spaces:A1 A5)\nNote: Each set of coordinates given must consume the correct amount of spaces on the grid.
        
    '''
    
    print(msg)
    showGrid(player.Grid)
    i = 0
    # (row,col) per coord
    coord1 = (0,0)
    coord2 = (0,0)
    egString = 'a'+ str(len(player.Grid))
    alpha = ALPHABET[:len(player.Grid)]
    spacesTaken = []
    while i < len(player.ships):
        shipCoord = input('\n{} {}-spaces:'.format(player.ships[i][0], player.ships[i][1])).upper().split()
        if shipCoord[0].lower() == 'quit':
            sys.exit()
        spacesToBeTaken = []

        # check for incorrect inputs
        if len(shipCoord) == 2 and len(shipCoord[0]) >= 2 and len(shipCoord[1]) >= 2 and len(shipCoord[0]) <= len(egString) and len(shipCoord[1]) <= len(egString) and shipCoord[0][0] in alpha and shipCoord[1][0] in alpha and shipCoord[0][1:].isnumeric() and shipCoord[1][1:].isnumeric():
            
            # check for diagonal placements
            coord1 = (alpha.index(shipCoord[0][0]), int(shipCoord[0][1:]))
            coord2 = (alpha.index(shipCoord[1][0]), int(shipCoord[1][1:]))
            subCoords = tuple(map(lambda i, j: i - j, coord1, coord2))
            
            # switch coordinate inputs so that coord1 < coord2 in position
            if subCoords[0] > 0 or subCoords[1] > 0:
                tempCoord = coord1
                coord1 = coord2
                coord2 = tempCoord
            
            # horizontal placement
            if subCoords[0] == 0 and abs(subCoords[1])+1 == int(player.ships[i][1]):
                for col in range(coord1[1]-1, coord2[1]):
                    #spacesToBeTaken.append(''.join(str((coord1[0],col))))
                    spacesToBeTaken.append((coord1[0],col))
                    
                # add ship placement coordinate to player's grid, and ship position dictionary
                if any(item in spacesToBeTaken for item in spacesTaken) == False:
                    for col in range(coord1[1]-1, coord2[1]):    
                        player.Grid[coord1[0]][col] = 1
                    player.shipPositions[player.ships[i][0]] = spacesToBeTaken
                    spacesTaken.extend(spacesToBeTaken)
                    i += 1
                else:
                    print('Ship placement overlaps another, try again.\n')
                
            # vertical placement
            elif subCoords[1] == 0 and abs(subCoords[0])+1 == int(player.ships[i][1]):
                for row in range(coord1[0], coord2[0]+1):
                    #spacesToBeTaken.append(''.join(str((row, coord1[1]-1))))
                    spacesToBeTaken.append((row, coord1[1]-1))
                    
                # add ship placement coordinate to player's grid, and ship position dictionary
                if any(item in spacesToBeTaken for item in spacesTaken) == False:
                    for row in range(coord1[0], coord2[0]+1):
                        player.Grid[row][coord1[1]-1] = 1
                    player.shipPositions[player.ships[i][0]] = spacesToBeTaken
                    spacesTaken.extend(spacesToBeTaken)
                    i += 1
                else:
                    print('\nShip placement overlaps another, try again.\n')
            else:
                print('\nDiagonal placement error or Space taken error, try again.\n')
        else:
            print('\nInvalid input, try again.\n')
        print('\n')
        showGrid(player.Grid)
    
# show a player's grid
def showGrid(grid):
    
    alpha = ALPHABET[:len(grid)]
    row = 0
    rowStr = ' ' + alpha[row] + ' |'
    separater = '---|'
    numberRow = '   |'
    
    # print number row (topmost row)
    for j in range(1, len(grid)+1):
        
        # construct number row
        if j < 10:
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
        if grid[row][i%(len(grid))] == 1:
            rowStr += ' O |'
            separater += '---|'
        elif grid[row][i%(len(grid))] == -1:
            rowStr += ' X |'
            separater += '---|'
        elif grid[row][i%(len(grid))] == 2:
            rowStr += ' H |'
            separater += '---|'
        elif grid[row][i%(len(grid))] == 3:
            rowStr += ' M |'
            separater += '---|'
        else:
            rowStr += '   |'
            separater += '---|'
        
        # print the last row
        if i == ( len(grid)*len(grid) )-1:
            print(rowStr)
            print(separater)
   
def clearScreen():
    user = input('\nPress enter to clear screen/continue.')
    if user.lower() == 'quit':
        sys.exit()
    else:
        clear() 
    
if __name__ == "__main__":
    main()