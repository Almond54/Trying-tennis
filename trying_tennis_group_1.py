import random


P0FS  = 0.76
P0FSW = 0.74
P0SS  = 0.94
P0SSW = 0.41
P1FS  = 0.70
P1FSW = 0.71
P1SS  = 0.92
P1SSW = 0.60

s = input("Use default input parameters? (yes/no) >> ")
if s.lower() != "yes" and s.lower() != "y":
    print("Please input the following information for Player 0, then Player 1:")
    print("-Probability of a legal first serve")
    print("-Probability of winning the point on the first serve")
    print("-Probability of a legal second serve")
    print("-Probability of winning the point on the second serve")
    P0FS  = float(input("Player 0 first serve            >> "))
    P0FSW = float(input("Player 0 wins with first serve  >> "))
    P0SS  = float(input("Player 0 second serve           >> "))
    P0SSW = float(input("Player 0 wins with second serve >> "))
    P1FS  = float(input("Player 1 first serve            >> "))
    P1FSW = float(input("Player 1 wins with first serve  >> "))
    P1SS  = float(input("Player 1 second serve           >> "))
    P1SSW = float(input("Player 1 wins with second serve >> "))
assert min(P0FS, P0FSW, P0SS, P0SSW, P1FS, P1FSW, P1SS, P1SSW) >= 0 and max(P0FS, P0FSW, P0SS, P0SSW, P1FS, P1FSW, P1SS, P1SSW) <= 1, "Error: All probabilites must be between 0 and 1"

def makePlayer(name = "player", first_legal = 0.9, first_win = 0.9, second_legal = 0.9, second_win = 0.9):
    """
    Taking in the appropriate probablities this function returns a player dictionary with a blank scoreboard
    """
    return{"name": name ,
           "first_legal": first_legal,
           "first_win": first_win, 
           "second_legal": second_legal, 
           "second_win": second_win, 
           "rounds_won_per_game": [], 
           "games_won_per_set": [], 
           "sets_won": [0]
           }

class player():
    def __init__(self, name = "player", first_legal = 0.9, first_win = 0.9, second_legal = 0.9, second_win = 0.9):
        self.name = name
        self.first_legal = first_legal
        self.first_win = first_win
        self.second_legal = second_legal
        self.second_win = second_win
        self.scoreboard = []
    def calculate_points(self):
        pass
    


def makeGame(playerZero, playerOne):
    temp = {
        "players": (playerZero, playerOne),
        "startServer": 
    }
    return temp

def makeSet(playerZero, playerOne):


def makeSet(playerZero, playerOne)
DefaultPlayer1 = makePlayer("Jim" ,0.76, 0.74, 0.94, 0.41)
DefaultPlayer2 = makePlayer("Bob", 0.7, 0.71, 0.92, 0.6)

def choose_server(playerZero, playerOne):
    """
    Returns a random integer 0 or 1 corresponding to a player number.
    """
    return random.randint(0, 1)

def point_winner(server, playerZero, playerOne):
    """
    Given 2 player dictionaries and a server it simulates a round of tennis and returns the winner
    """
    if server == 0:
        startingPlayer = playerZero
        otherPlayer = playerOne
    else:
        startingPlayer = playerOne
        otherPlayer = playerZero
    print(f"The server is {startingPlayer['name']}")
    if random.random() <= startingPlayer["first_legal"]:
        print(f"{startingPlayer['name']}'s first serve is legal")
        if random.random() <= startingPlayer["first_win"]:
            print(f"{startingPlayer['name']} won this point on the first serve")
            return startingPlayer
        print(f"{otherPlayer['name']} won this point on the second serve")
    else:
        print(f"{startingPlayer['name']}'s first serve is not legal")
        if random.random() <= startingPlayer["second_legal"]:
            print(f"{startingPlayer['name']}'s second serve is legal")
            if random.random() <= startingPlayer["second_win"]:
                print(f"{startingPlayer['name']} won on the second serve")
                
                return startingPlayer
            print(f"{otherPlayer['name']} won after the second serve")
    return otherPlayer

#its giving a random server every time they play a point so we need to get it to give a server then play the whole game with the 
# same server, which we can do by getting another function to give a server at the start, but idk if theres a better way to do it


def play_game(playerZero, playerOne , server = choose_server()):
    """
    Given two players this simulates a game of tennis and returns the winner.
    """
    
    playerZero["rounds_won_per_game"].append(0)
    playerOne["rounds_won_per_game"].append(0)

    #I have changed the while statement to be more readble the logic is now in its own function
    while game_ongoing(playerZero["rounds_won_per_game"][-1], playerOne["rounds_won_per_game"][-1]):
        if point_winner(server, playerZero, playerOne) == playerZero:
            playerZero["rounds_won_per_game"][-1] += 1
        else:
            playerOne["rounds_won_per_game"][-1] += 1
    if playerZero["rounds_won_per_game"][-1] > playerOne["rounds_won_per_game"][-1]:
        game_winner = playerZero
        playerZero["games_won_per_set"][-1] += 1
    else:
        game_winner = playerOne
        playerOne["games_won_per_set"][-1] += 1
    return game_winner

def game_ongoing(p0PointsWon, p1PointsWon):
    """
    This functions takes the parameters required to check if a game of tennis is ongoing and then returns true of false if it is ongoing
    """
    if p0PointsWon >= 4 or p1PointsWon >= 4: #Do any players have 4 or greater points?
        if abs(p0PointsWon - p1PointsWon) >= 2: #Is the difference between their points 2 or more
            return False
    return True

def play_set(playerZero, playerOne):
    """
    Given 2 players, this function simulates a set of tennis and returns the winner of the set.
    """
    playerZero["games_won_per_set"].append(0)
    playerOne["games_won_per_set"].append(0)
    server = choose_server()
    while set_ongoing(playerZero["games_won_per_set"][-1], playerOne["games_won_per_set"][-1]):
        play_game(playerZero, playerOne, server) == playerZero
        server = (server + 1) % 2
    if playerZero["games_won_per_set"][-1] > playerOne["games_won_per_set"][-1]:
        set_winner = playerZero
        playerZero["sets_won"][-1] += 1
    else:
        set_winner = playerOne
        playerOne["sets_won"][-1] += 1
    return set_winner

def set_ongoing(p0GamesWon, p1GamesWon):
    """
    This function takes the parameters required to check if a set of tennis is ongoing and then returns true or false
    """
    if p0GamesWon > 6 or p1GamesWon >6:
        if abs(p0GamesWon - p1GamesWon) >= 2:
            return False
    return True

def play_match(playerZero, playerOne):
    """
    Given 2 players, this function simulates a match of tennis and returns the winner of the match.

    """
    playerZero["sets_won"][-1] = 0 
    playerOne["sets_won"][-1] = 0
    while playerZero["sets_won"] < 3 and playerOne["sets_won"] < 3:
        if play_set(playerZero, playerOne) == playerZero:
            playerZero["sets_won"][-1] += 1
        else:
            playerOne["sets_won"][-1] += 1
    if playerZero["sets_won"][-1] > playerOne["sets_won"][-1]:
        match_winner = playerZero
    else:
        match_winner = playerOne
    return match_winner
#for x in range(5):
#    print(play_game(DefaultPlayer1, DefaultPlayer2))
print(play_set(DefaultPlayer1, DefaultPlayer2))
#print(play_match(DefaultPlayer1, DefaultPlayer2))