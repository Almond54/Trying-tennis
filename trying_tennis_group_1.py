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
    Taking in the appropriate probablities this function returns a player dictionary 
    """
    return{"name": name ,
           "first_legal": first_legal,
           "first_win": first_win, 
           "second_legal": second_legal, 
           "second_win": second_win, 
           "rounds_won_per_game": [0], 
           "games_won": [0], 
           "sets_won": [0]
           }

DefaultPlayer1 = makePlayer("Jim" ,0.76, 0.74, 0.94, 0.41)
DefaultPlayer2 = makePlayer("Bob", 0.7, 0.71, 0.92, 0.6)

def choose_server():
    """
    Returns a random integer 0 or 1 corresponding to a player number.
    """
    return random.randint(0, 1)

def point_winner(server, playerZero, playerOne):
    """
    Given a starting server, the probabilities of legal serves and the probability of winning their respective serve, 
    the function returns the winner of a point according to the probabilities given.
    """
    if server == 0:
        startingPlayer = playerZero
        otherPlayer = playerOne
    else:
        startingPlayer = playerOne
        otherPlayer = playerZero
    print(f"The server is {startingPlayer}")
    if random.random() <= startingPlayer["first_legal"]:
        print("The server first serve is legal")
        if random.random() <= startingPlayer["first_win"]:
            print("the server won on the first serve")
            return startingPlayer
        print("the server lost on the first serve")
    else:
        print("The server first serve is not legal")
        if random.random() <= startingPlayer["second_legal"]:
            print("The server's second serve is legal")
            if random.random() <= startingPlayer["second_win"]:
                print("the server won on the second serve")
                
                return startingPlayer
            print("the server lost the second serve")
    return otherPlayer

#its giving a random server every time they play a point so we need to get it to give a server then play the whole game with the 
# same server, which we can do by getting another function to give a server at the start, but idk if theres a better way to do it


def play_game(playerZero, playerOne):
    """
    Given a starting server, the probabilities of legal serves and the probability of winning their respective serve, return the 
    winner of a game of tennis between player 0 and player 1 with the same player serving throughout.
    """
    server = choose_server()
    playerZero["rounds_won_per_game"][-1] = 0
    playerOne["rounds_won_per_game"][-1] = 0
    rounds = 0
    while abs(playerZero["rounds_won_per_game"][-1] - playerOne["rounds_won_per_game"][-1]) < 2 or rounds <= 4:
        if point_winner(server, playerZero, playerOne) == playerZero:
            playerZero["rounds_won_per_game"][-1] += 1
        else:
            playerOne["rounds_won_per_game"][-1] += 1
        rounds += 1
    if playerZero["rounds_won_per_game"][-1] > playerOne["rounds_won_per_game"][-1]:
        game_winner = playerZero
        playerZero["games_won"][-1] += 1
    else:
        game_winner = playerOne
        playerOne["games_won"][-1] += 1
    return game_winner

def play_set(playerZero, playerOne):
    """
    Given a starting server, the probabilities of legal serves and the probability of winning their respective serve, returns 
    the winner of the set of tennis between player 0 and player 1 where the starting server alternates between games.
    """
    playerZero["games_won"][-1] += 1
    playerOne["games_won"][-1] += 1
    games = 0
    while abs(playerZero["rounds_won_per_game"][-1] - playerOne["rounds_won_per_game"][-1]) < 2 or games <= 6:
        if play_game(playerZero, playerOne) == playerZero:
            playerZero["games_won"][-1] += 1
        else:
            playerOne["games_won"][-1] += 1
        start_server = (start_server + 1) % 2
        games += 1
    if playerZero["games_won"][-1] > playerOne["games_won"][-1]:
        set_winner = playerZero
        playerZero["sets_won"][-1] += 1
    else:
        set_winner = playerOne
        playerOne["sets_won"][-1] += 1
    return set_winner

def play_match(playerZero, playerOne):
    """
    Given a starting server, the probabilities of legal serves and the probability of winning their respective serve, returns 
    the winner of a full match of tennis between player 0 and player 1 of the first to win 3 sets, with the server alternating 
    between games.
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

print(play_game(DefaultPlayer1, DefaultPlayer2))
#print(play_set(DefaultPlayer1, DefaultPlayer2))
#print(play_match(DefaultPlayer1, DefaultPlayer2))