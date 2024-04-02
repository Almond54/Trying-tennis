import random
import randomname

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
           "points_won_per_game": [], 
           "games_won_per_set": [0], 
           "sets_won": [0],
           "first_serves": 0,
           "second_serves": 0,
           "points_won_on_first_serve": 0,
           "points_won_on_second_serve": 0
           }

DefaultPlayer0 = makePlayer("Jim" ,0.76, 0.74, 0.94, 0.41)
DefaultPlayer1 = makePlayer("Bob", 0.7, 0.71, 0.92, 0.6)

def choose_server():
    """
    Returns a random integer 0 or 1 corresponding to a player number.
    """
    return random.randint(0, 1)

def point_winner(playerZero, playerOne, server = choose_server()):
    """
    Given 2 player dictionaries and a server it simulates a round of tennis and returns the winner
    """
    if server == 0:
        startingPlayer = playerZero
        otherPlayer = playerOne
    else:
        startingPlayer = playerOne
        otherPlayer = playerZero
    startingPlayer['first_serves'] += 1
    print(f"The server is {startingPlayer['name']}")
    if random.random() <= startingPlayer["first_legal"]:
        print(f"{startingPlayer['name']}'s first serve is legal")
        if random.random() <= startingPlayer["first_win"]:
            startingPlayer['points_won_on_first_serve'] += 1
            print(f"{startingPlayer['name']} won this point on the first serve")
            return startingPlayer
        print(f"{otherPlayer['name']} won this point on the second serve")
    else:
        print(f"{startingPlayer['name']}'s first serve is not legal")
        startingPlayer['second_serves'] += 1
        if random.random() <= startingPlayer["second_legal"]:
            print(f"{startingPlayer['name']}'s second serve is legal")
            if random.random() <= startingPlayer["second_win"]:
                print(f"{startingPlayer['name']} won on the second serve")
                startingPlayer['points_won_on_second_serve'] += 1
                return startingPlayer
            print(f"{otherPlayer['name']} won after the second serve")
    return otherPlayer
    
def game_ongoing(p0PointsWon, p1PointsWon):
    """
    This functions takes the parameters required to check if a game of tennis is ongoing and then returns true of false if it is ongoing
    """
    if p0PointsWon >= 4 or p1PointsWon >= 4: #Do any players have 4 or greater points?
        if abs(p0PointsWon - p1PointsWon) >= 2: #Is the difference between their points 2 or more
            return False
    return True
    
def play_game(playerZero, playerOne , server = choose_server()):
    """
    Given two players this simulates a game of tennis and returns the winner.
    """
    playerZero["points_won_per_game"].append(0)
    playerOne["points_won_per_game"].append(0)
    while game_ongoing(playerZero["points_won_per_game"][-1], playerOne["points_won_per_game"][-1]):
        if point_winner(playerZero, playerOne, server) == playerZero:
            playerZero["points_won_per_game"][-1] += 1
        else:
            playerOne["points_won_per_game"][-1] += 1
    if playerZero["points_won_per_game"][-1] > playerOne["points_won_per_game"][-1]:
        game_winner = playerZero
        playerZero["games_won_per_set"][-1] += 1
    else:
        game_winner = playerOne
        playerOne["games_won_per_set"][-1] += 1
    return game_winner

def set_ongoing(p0GamesWon, p1GamesWon):
    """
    This function takes the parameters required to check if a set of tennis is ongoing and then returns true or false
    """
    if p0GamesWon > 6 or p1GamesWon >6:
        if abs(p0GamesWon - p1GamesWon) >= 2:
            return False
    return True
    
def play_set(playerZero, playerOne, starting_server = choose_server()):
    """
    Given 2 players, this function simulates a set of tennis and returns the winner of the set.
    """
    if playerOne["games_won_per_set"][-1] != 0 and playerZero["games_won_per_set"][-1] != 0:
        playerZero["games_won_per_set"].append(0)
        playerOne["games_won_per_set"].append(0)
    while set_ongoing(playerZero["games_won_per_set"][-1], playerOne["games_won_per_set"][-1]):
        play_game(playerZero, playerOne, starting_server)
        starting_server = (starting_server + 1) % 2
    if playerZero["games_won_per_set"][-1] > playerOne["games_won_per_set"][-1]:
        set_winner = playerZero
        playerZero["sets_won"][-1] += 1
    else:
        set_winner = playerOne
        playerOne["sets_won"][-1] += 1
    return set_winner

def play_match(playerZero, playerOne, starting_server = choose_server()):
    """
    Given 2 players, this function simulates a match of tennis and returns the winner of the match.
    """
    playerZero["sets_won"][-1] = 0 
    playerOne["sets_won"][-1] = 0
    while playerZero["sets_won"][-1] < 3 and playerOne["sets_won"][-1] < 3:
        play_set(playerZero, playerOne, starting_server)
    if playerZero["sets_won"][-1] > playerOne["sets_won"][-1]:
        match_winner = playerZero
    else:
        match_winner = playerOne
    print(f"{match_winner['name']} won the match, winning {sum(match_winner['points_won_per_game'])} points total.")
    for i in range(len(match_winner['games_won_per_set'])):
        print(f"The match winner won {match_winner['games_won_per_set'][i]} games in set {i + 1}")
    print(f"The match winner's percentage of points won on their first serve is {match_winner['points_won_on_first_serve'] / match_winner['first_serves']}")
    print(f"The match winner's percentage of points won on their second serve is {match_winner['points_won_on_second_serve'] / match_winner['second_serves']}")
    return match_winner

def read_players(file):
    """
    This function will extract the player dictionaries from a text file returning a list of all the player dictionaries
    """
    players = []
    with open(file, "r") as f:
        for line in f:
            stats = line.split(" ")
            players.append(makePlayer(stats[0], stats[1], stats[2], stats[3], stats[4]))
    
    return players

def create_players(num):
    """
    This function writes players to a text file called players.txt
    """
    with open("players.txt", "w") as f:
        for x in range(num):
            name = randomname.get_name()
            stats = [random.random() for x in range(4)]
            f.write(f"{name} {stats[0]} {stats[1]} {stats[2]} {stats[3]}\n")

class tourney():
    """
    This class manages a tourney of tennis players
    """
    def __init__(self, players):
        self.players = players
        self.players_remaining = players
        self.players_eliminated = []
    def create_pairings(self):
        pass

#print(point_winner(DefaultPlayer0, DefaultPlayer1))
#print(play_game(DefaultPlayer0, DefaultPlayer1))
#print(play_set(DefaultPlayer0, DefaultPlayer1))
#print(play_match(DefaultPlayer0, DefaultPlayer1))
#create_players(10)
print(read_players("players.txt"))