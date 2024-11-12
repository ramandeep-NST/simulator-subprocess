import os
import subprocess
import timeit



POINTS = {
    ("Cooperate", "Cooperate"): (3, 3),
    ("Cooperate", "Defect"): (0, 5),
    ("Defect", "Cooperate"): (5, 0),
    ("Defect", "Defect"): (1, 1)
}

# Function to simulate a game round between two players
# 
def play_rounds(player1_name, player2_name, player1_script, player2_script, rounds=1000):
    score1, score2 = 0, 0
    moves1, moves2 = [], []
    
    # Start the players as subprocesses
    player1_process = subprocess.Popen(['python3', player1_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    player2_process = subprocess.Popen(['python3', player2_script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    
    # # Give both players their first move (initially "Cooperate")
    # player1_process.stdin.write("Cooperate\n")

    # player1_process.stdin.flush()
    # player2_process.stdin.write("Cooperate\n")
    
    # player2_process.stdin.flush()
   
    for i in range(rounds):

        
        # Get the last moves of both players
        last_move1 = moves1[-1] if moves1 else "None"
        last_move2 = moves2[-1] if moves2 else "None"

        # Provide the opponent's last move as input for each player
        player1_process.stdin.write(f"{last_move2}\n")
        player1_process.stdin.flush()
        player2_process.stdin.write(f"{last_move1}\n")
        player2_process.stdin.flush()
        
        # Read the players' moves
        # !!!!!!!!! we need to wait here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! write a checker here ...
        # O(1), O(n), O(n*n), 
        # avg(player ko input deke usko out dene me kitna time lagta h) 
        # rounds = 1000
        move1 = player1_process.stdout.readline().strip()
        move2 = player2_process.stdout.readline().strip()

        move1 = validate_move(move1)
        move2 = validate_move(move2)

        # if move1 == "stop":
        #     print(f"{player1_name} decided to stop the game.")
        #     break
        # if move2 == "stop":
        #     print(f"{player2_name} decided to stop the game.")
        #     break

        moves1.append(move1)
        moves2.append(move2)

        # Calculate points for the round
        points1, points2 = POINTS[(move1, move2)]
        score1 += points1
        score2 += points2
        if i == 0 or i == 500 or i == 999:
            print(f"Round {i + 1}: {player1_name} played {move1}, {player2_name} played {move2}")
            print(f"Points: {player1_name} = {points1}, {player2_name} = {points2}")

        
        


      

    # Terminate the processes
    player1_process.terminate()
    player2_process.terminate()

    return score1, score2

# Validate move (ensure it is either Cooperate or Defect)
def validate_move(move):
    if move not in {"Cooperate", "Defect"}:
        print(f"Invalid move '{move}' encountered. Defaulting to 'Cooperate'.")
        return "Cooperate"
    return move

# Run the tournament where each player plays against every other player
def run_tournament(player_scripts, rounds=10):
    leaderboard = {name: 0 for name in player_scripts}
    visited = set()  # To keep track of which pairs have already played
    
    #print(player_scripts)
    for name1, script1 in player_scripts.items():
        sum=0
        start = timeit.default_timer()
        for name2, script2 in player_scripts.items():
            if name1 != name2 and (name1, name2) not in visited and (name2, name1) not in visited:
                print(f"\nStarting match between {name1} and {name2}")
                 
                score1, score2 = play_rounds(name1, name2, script1, script2, rounds)
                
    
                # print(score1)
                # print(score2)
                leaderboard[name1] += score1
                leaderboard[name2] += score2
                # print(leaderboard)
                # print("Hello")
                visited.add((name1, name2))
                visited.add((name2,name1))
        end = timeit.default_timer()
        sum = sum + (end - start)
        print(sum)
    # Sort the leaderboard by score in descending order
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)

    return sorted_leaderboard

# Simulate the tournament
def simulate(directory, rounds=10):
    # Get the list of player scripts
    player_scripts = {}  # maps player with simulation strategy path
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            player_name = filename.split(".")[0]  # Use the filename (without .py) as the player name
            player_scripts[player_name] = os.path.join(directory, filename)

    leaderboard = run_tournament(player_scripts, rounds)
 

    print("\nTournament Results:")
    for name, score in leaderboard:
        print(f"Player {name}: {score} points")
 
       # Initialize a Rank dictionary to store ranks
    Rank = {}
    r = 0  
    prev_score = None   

    # Iterate through the sorted leaderboard and assign ranks
    for i, (name, score) in enumerate(leaderboard):
        if prev_score is None or score != prev_score:
            r = r+1
            Rank[name] = r  
        else:
            Rank[name] = r  

         
        prev_score = score


    # Print ranks
    print("\nPlayer             Rank")
    print("_____________________________")
    for name, rank in Rank.items():
        print(f"Player-{name}              {rank}")

# Run the simulation
simulate("/Users/ramandeepsingh/Desktop/strategies", rounds=500)

