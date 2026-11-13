from drafter import *
#from bakery import assert_equal
from dataclasses import dataclass

set_website_title("Real Madrid Season Tracker")
set_site_information(
    author="Cristofer Perez-Perez",
    description="A simple way to track the team and player statistics.",
    sources="Thanks to the Drafter docs and my study group.",
    planning=[],
    links=[]
)
hide_debug_information()







#----- dataclasses -------
@dataclass
class Player:
    '''
stores stats for one player
'''
    name: str
    position: str
    goals: int
    assists: int
    games_played: int
    
@dataclass
class Match:
    ''' stores stats from one player's match'''
    opponent: str
    player_name: str
    goals: int
    assists: int

@dataclass
class State:
    '''
stores information for the tracker
'''
    message: str
    players: list[Player]
    matches: list[Match]
    selected_player: str
 



 #--- home page-----
@route("index")
def home(state: State) -> Page:
    return Page(state, [
        "Season Tracker",
        "Track your favorite players stats here",
        Button("View Roster", roster_page),
        Button("Add Match", add_match_page),
        Button("Match History", history_page),
        Button("Leaders", leaders_page),
        Button("Player Deatails", player_details_page)
        ])




#---- the player roster---
@route
def roster_page(state: State)-> Page:
    '''
displays the roster
'''
    player_txt = ""
    
    for player in state.players:
        player_txt += (
            player.name + " | " + player.position
            + " | Goals:" + str(player.goals)
            + " | Assists:" + str(player.assists)
            + " | Games: " + str(player.games_played)
            + " \n"
            )
    return Page(state, [
        "Real Madrid Roster",
        player_txt,
        Button("Back to home", "index")
        ])


#---add matches-----
@route
def add_match_page(state: State)-> Page:
    '''
where to enter match stats
'''
    return Page(state, [
        "add match stats",
        state.message,
        "enter opponent:",
        TextBox("opponent"),
        "enter player name:",
        TextBox("player_name"),
        "goals scored:",
        TextBox("goals"),
        "assists made:",
        TextBox("assists"),
        Button("Submit match", submit_match),
        Button("Back to home", "index")
        ])
 

#---submit the match stats------
@route
def submit_match(state: State, opponent: str,
                 player_name: str, goals: str,
                 assists: str)-> Page:
    '''
    here is where you'll
    enter and save the match stats
    '''
    if not goals.isdigit() or not assists.isdigit():
        state.message = "You must enter numbers."
        return add_match_page(state)
    
    for player in state.players:
        if player.name.lower() == player_name.strip().lower():
            player.goals += int(goals)
            player.assists += int(assists)
            player.games_played += 1
            state.matches.append(
                Match(opponent, player.name, int(goals), int(assists)))
                
            
            
            state.message = ("stats kept for" + player.name
                             + "against" + opponent)
            return roster_page(state)
    state.message = "Player not found. Chech again."
    return add_match_page(state)
      
      
#---- the match history ------
@route
def history_page(state: State)-> Page:
    match_txt = ""
    
    if len(state.matches) == 0:
        match_txt = "No recorded matches"
        
    for match in state.matches:
        match_txt += (
            match.player_name
            + "vs" + match.opponent
            + " | Goals:" + str(match.goals)
            + " |Assists:" + str(match.assists)
            + "\n")
    
    return Page(state, [
        "match history",
        match_txt,
        Button("Back to home", "index")])



#----- the goal/ assist leader------
@route
def leaders_page(state: State) -> Page:
    top_scorer = ""
    top_assister = ""
    most_goals = -1
    most_assists = -1
    total_goals = 0
    total_assists = 0
    
    for player in state.players:
        total_goals += player.goals
        total_assists += player.assists
        
        if player.goals > most_goals:
            most_goals = player.goals
            top_scorer = player.name
            
        if player.assists > most_assists:
            most_assists = player.assists
            top_assister = player.name
            
    return Page(state, [
        "Club leaders:",
        "top scorer: " + top_scorer,
        "goals: " + str(most_goals),
        "top assister: " + top_assister,
        "assists: " + str(most_assists),
        "Total team goals: " + str(total_goals),
        "Total team assists: " + str(total_assists),
        Button("Back to home", "index")])

    
    
#----last page/ player selection-----
@route
def player_details_page(state: State)-> Page:
    return Page(state, [
        "Player dats",
        "Enter player name: ",
        TextBox("player_name"),
        Button("View their stats", show_player_stats),
        Button("Back to home", "index")])

@route
def show_player_stats(state: State, player_name: str)-> Page:
    for player in state.players:
        if player.name.lower() == player_name.strip().lower():
            state.selected_player = player.name
            
            return Page(state, [
                "player details: " + player.name,
                "position: " + player.position,
                "goals: " + str(player.goals),
                "assists: " + str(player.assists),
                "games played; " + str(player.games_played),
                Button("Choose another Player", player_details_page),
                Button("Back to home", "index")])
        
    state.message = "Error. No player found."
    
    return Page(state, [
        state.message,
        "Check your spelling. Try again.",
        Button("tyr again", player_details_page),
        Button("back to home", "index")])
        
    

      
#---- these are the players that will already be in.----
#--so later u can add/update the roster-----=

def the_starting_players()-> list[Player]:
    return [
        Player("Kylian Mbappe", "Forward", 0, 0, 0),
        Player("Yan Diomande", "Forward", 0, 0, 0),
        Player("Jude Bellingham", "Midfield", 0, 0, 0),
        Player("Federico Valverde", "Midfield", 0, 0, 0),
        Player("Thibaut Courtois", "Goalie", 0, 0, 0)
        ]

start_server(State("Welcome", the_starting_players(), [], ""))


