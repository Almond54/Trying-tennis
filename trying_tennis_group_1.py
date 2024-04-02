import random
import randomname


class Tennis():
    """
    This class represents a basic object of tennis (either a round, game, set, match, or tourney) as each of these subtypes of scoring has:
        > Players
        > A record of what has happened at that scope
        > A winner
    """
    def __init__(self, players, tracked = True):
        self.players = players
        self.record = []
        self.winner = "Undecided"
        if tracked == True:
            self.players[0].scoreboard.append(self)
            self.players[1].scoreboard.append(self)

class player():
    """
    A tennis player object that store their:
        >Name
        >Probabilites of winning on serves
        >A scoreboard
    and provides fuctions to calcuate the number of rounds, games and sets won respectivly
    """
    def __init__(self, name = "player", first_legal = 0.9, first_win = 0.9, second_legal = 0.9, second_win = 0.9):
        """
        This function is the initializion for a new player.
        """
        self.name = name
        self.first_legal = first_legal
        self.first_win = first_win
        self.second_legal = second_legal
        self.second_win = second_win
        self.scoreboard = []
    def rounds_won_in_match(self, matchNum):
        """
        By passing in a match object this function will return the amount of rounds won
        """
        matchList = [i for i in self.scoreboard if type(i) == tennisMatch] # This is a list of all matches in the scoreboard
        num = 0
        assert len(matchList) >= matchNum, "Invalid match number! or no matches on this player"

        # The following lines iterate through every round in the tennis match
        for set in matchList[matchNum].record:
            for game in set.record:
                for round in game.record:
                    if round.winner == self.name:
                        num += 1
        return num


            
    def service_games_won(self, matchNum):
        """
        This function returns the number of service games won in a match
        """
        matchList = [i for i in self.scoreboard if type(i) == tennisMatch] # This is a list of all matches in the scoreboard
        num = 0
        assert len(matchList) >= matchNum, "Invalid match number! or no matches on this player"
        for set in matchList[matchNum].record:
            for game in set.record:
                if game.winner == self.name and game.server.name == self.name:
                    num += 1
        return num

    def percentageOfPoints(self, matchNum):
        """
        This function returns a tuple of the the percentages of where each point was scored
        """
        matchList = [i for i in self.scoreboard if type(i) == tennisMatch] # This is a list of all matches in the scoreboard
        FirstServeNum = 0
        SecondServeNum = 0
        roundsWon = self.rounds_won_in_match(matchNum)
        assert len(matchList) >= matchNum, "Invalid match number! or there are no matches on this player"
        for set in matchList[matchNum].record:
            for game in set.record:
                if game.winner == self.name and game.server.name == self.name:
                    for round in game.record:
                        if round.record == 1:
                            FirstServeNum += 1
                        else:
                            SecondServeNum += 1
        return ((FirstServeNum/roundsWon) * 100, (SecondServeNum/roundsWon) * 100, ((roundsWon - (FirstServeNum + SecondServeNum))/roundsWon) * 100)

    
class roundOfTennis(Tennis):
    """
    This class represents a singular round of tennis including:
        > The Names of the players involved
        > A record of what happened during the round
        > The winner of the round
    """

    def __init__(self, players,server , tracked = True):
        super().__init__(players, tracked)
        self.server = server
        self.record = 0
    
    def play(self):
        """
        This function plays the set of tennis changing the record as appropiate
        """
        if self.winner == "Undecided": #This is so you can't play a round thats already decided!
            if self.server == self.players[0]:
                otherplayer = self.players[1]

            else:
                otherplayer = self.players[0]

            if random.random() <= self.server.first_legal:
                if random.random() <= self.server.first_win:
                    self.record = 1 # We will read the results depending on record number
                    self.winner = self.server.name
                else:
                    self.record = 2
                    self.winner = otherplayer.name
            else:
                #If the first serve is not legal
                if random.random() <= self.server.second_legal:

                    if random.random() <= self.server.second_win:
                        self.record = 3
                        self.winner = self.server.name
                    
                    #If the server doesn't win the second serve
                    else:
                        self.record = 4
                        self.winner = otherplayer.name
                else:
                    self.record = 5
                    self.winner = otherplayer.name
    
    def __repr__(self):
        if self.record == 0:
            return "The round is currenly ongoing please use the play() function"
        elif self.record == 1:
            return f"The round was won by {self.winner} on the first serve"
        elif self.record == 2:
            return f"The round was won by {self.winner} after {self.server.name} lost after a legal first serve"
        elif self.record == 3:
            return f"The round was won by {self.winner} on the second serve"
        elif self.record == 4:
            return f"The round was won by {self.winner} after {self.server.name} lost after a legal second serve"
        elif self.record == 5:
            return f"The round was won by {self.winner} after {self.server.name} failed to make a legal serve"


class game(Tennis):
    """
    This class represents a singular game of tennis including:
        > The Names of the players involved
        > A record of what happened during the game
        > The winner of the game
    """
    def __init__(self, players, server, tracked = True):
        super().__init__(players, tracked)
        self.server = server
    
    def play(self):
        if self.winner == "Undecided":
            rounds = self.record
            ongoing = True
            pointsList = []

            while ongoing:
                rounds.append(roundOfTennis(self.players, self.server, False)) # Adding a round to the game
                rounds[-1].play() #Playing the round 
                pointsList.append(rounds[-1].winner) #Adds the name of the winner to pointsList

                playerZeroPoints = pointsList.count(self.players[0].name)
                playerOnePoints = pointsList.count(self.players[1].name)

                if playerZeroPoints >= 4 or playerOnePoints >= 4: #Do the players have more than for points?
                    if abs(playerZeroPoints - playerOnePoints) >= 2: #Is there difference greater than 2?
                        ongoing = False
                        if playerZeroPoints > playerOnePoints:
                            self.winner = self.players[0].name
                        else:
                            self.winner = self.players[1].name
                        


    def __repr__(self):
        if self.winner == "Undecided":
            return "The game has not run yet! please run it using the play() functions"
        else:
            numberOfPoints =  sum([1 for x in self.record if x.winner == self.winner])
            return f"The game's winner is {self.winner} who scored {numberOfPoints} points"   

    

class tennisSet(Tennis):
    """
    This class represents a set of tennis including:
        > The Names of the players involved
        > A record of the games during the set
        > The winner of the set
    """
    def __init__(self, players, tracked = True):
        super().__init__(players, tracked)
        self.server = choose_server(players[0], players[1])


    def play(self):
        if self.winner == "Undecided":
            games = self.record
            ongoing = True
            gameWinnerList = []

            while ongoing:
                games.append(game(self.players, self.server, False)) # Adding a game to the game
                
                #This is just alternating the servers between games               
                if self.players[0] == self.server:
                    self.server = self.players[1]
                else:
                    self.server = self.players[0]

                games[-1].play() #Playing the game 
                gameWinnerList.append(games[-1].winner) #Adds the name of the winner to gameList

                playerZeroGamesWon = gameWinnerList.count(self.players[0].name) #Getting the number of times player 0 has won
                playerOneGamesWon = gameWinnerList.count(self.players[1].name) # Getting the number of times player 1 has won

                if playerZeroGamesWon >= 6 or playerOneGamesWon >= 6: #Do the players have more than for points?
                    if abs(playerZeroGamesWon - playerOneGamesWon) >= 2: #Is there difference greater than 2?
                        ongoing = False
                        if playerZeroGamesWon > playerOneGamesWon:
                            self.winner = self.players[0].name
                        else:
                            self.winner = self.players[1].name
                        


    def __repr__(self):
        if self.winner == "Undecided":
            return "The set has not run yet! please run it using the play() functions"
        else:
            numberOfGamesWonByWinner =  sum([1 for x in self.record if x.winner == self.winner])
            nubmerOfGamesWonByLoser = sum([1 for x in self.record if x.winner != self.winner])
            return f"The set's winner is {self.winner} who won {numberOfGamesWonByWinner} games where as the opponent only won {nubmerOfGamesWonByLoser} games"

class tennisMatch(Tennis):
    def __init__(self, players, tracked = True):
        super().__init__(players, tracked)
        
    def play(self):
        if self.winner == "Undecided":
            ongoing = True
            sets = self.record
            setWinnerList = []
            while ongoing:
                sets.append(tennisSet(self.players, False)) #Adds a set to the record
                sets[-1].play() #plays the current set
                setWinnerList.append(sets[-1].winner)

                playerZeroSetsWon = setWinnerList.count(self.players[0].name)
                playerOneSetsWon = setWinnerList.count(self.players[1].name)

                if playerZeroSetsWon >= 3:
                    self.winner = self.players[0].name
                    ongoing = False

                if playerOneSetsWon >= 3:
                    self.winner = self.players[1].name
                    ongoing = False

    def __repr__(self):
        if self.winner == "Undecided":
            return "The match hasn't started yet! please use play() to start the match"
        else:
            return f"The winner of the match is {self.winner}"



DefaultPlayer1 = player("Jim" ,0.76, 0.74, 0.94, 0.41)
DefaultPlayer2 = player("Bob", 0.7, 0.71, 0.92, 0.6)

def choose_server(playerZero, playerOne):
    """
    Returns a random integer 0 or 1 corresponding to a player number.
    """
    return random.choice([playerZero, playerOne])

def read_players(file):
    """
    This function will extract the player dictionaries from a text file returning a list of all the player dictionaries
    """
    players = []
    with open(file, "r") as f:
        for line in f:
            stats = line.split(" ")
            players.append(player(stats[0], float(stats[1]), float(stats[2]), float(stats[3]), float(stats[4])))
    
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
    This class manages a tourney of tennis players of single elimination style
    """
    def __init__(self, players):
        """
        Initilization for the tourney
        """
        while ((len(players) & (len(players)-1) == 0) and len(players) != 0) != True: #using bit manipulations to check if we have a power of 2 for the number of players
            del players[-1] #delete the last players in the list until the number of players is a power of 2
        
        self.players = players

        self.players_remaining = players

        self.players_eliminated = []


    def create_pairings(self):
        self.players_remaining = random.shuffle(self.players_remaining)


    def play_bracket(self):
        nextBracket = []
        for i in range(0, len(self.players_remaining) - 1, 2):
            ongoingMatch = tennisMatch([self.players_remaining[i], self.players_remaining[i + 1]])
            ongoingMatch.play()
            #The following if else chooses the correct winner object to parse into the next braket
            if ongoingMatch.winner == ongoingMatch.players[0]: 
                winnerObject = ongoingMatch.players[0]
                loserObject = ongoingMatch.players[1]
            else:
                winnerObject = ongoingMatch.players[1]
                loserObject = ongoingMatch.players[0]
            nextBracket.append(winnerObject)
            self.players_eliminated.append(loserObject)
        self.players_remaining = nextBracket




#create_players(18)
#test = read_players("players.txt")

bigTest = tourney(test)
print(len(bigTest.players_remaining))
bigTest.play_bracket()
print(len(bigTest.players_remaining))