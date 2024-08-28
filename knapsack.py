import pandas as pd
from collections import defaultdict, Counter

def load_players_from_spreadsheet(file_path):
    # Load the spreadsheet into a DataFrame
    df = pd.read_excel(file_path, engine='odf')
    
    # Convert the DataFrame to a list of dictionaries
    players = df.to_dict(orient='records')
    return players

def dict_to_tuple(d):
    """Convert a dictionary to a sorted tuple."""
    return tuple(sorted(d.items()))

def knapsack_fantasy_football(players, budget, position_limits):
    """
    Solve the fantasy football knapsack problem with standard positions.
    
    Args:
    - players (list of dicts): Each dict contains 'name', 'position', 'value', and 'cost'.
    - budget (int): Total budget available.
    - position_limits (dict): Position constraints (e.g., {'RB': 2, 'WR': 3, 'QB': 1, 'TE': 1, 'K': 1, 'D': 1}).
    
    Returns:
    - best_team (list of dicts): The best team configuration.
    - best_value (int): The highest value achievable within the constraints.
    """
    
    # Initialize DP table: defaultdict to hold best values for given cost and position counts
    dp = defaultdict(lambda: (0, []))
    
    # Initial state: no budget spent, no players selected
    initial_team = dict_to_tuple(Counter())
    dp[(0, initial_team)] = (0, [])
    
    # Track progress
    processed_states = 0
    total_states = len(players) * 10000  # Estimate of total states

    for player in players:
        current_dp = list(dp.items())  # Snapshot to avoid modifying during iteration
        
        for (spent_budget, team), (value, team_list) in current_dp:
            new_budget = spent_budget + player['cost']
            if new_budget > budget:
                continue
            
            # Convert tuple back to dictionary for updates
            team_dict = dict(team)
            new_team = team_dict.copy()
            new_team[player['position']] = new_team.get(player['position'], 0) + 1
            
            # Check if the team respects hard position limits
            if all(new_team.get(pos, 0) <= position_limits.get(pos, float('inf')) for pos in position_limits):
                # Check if this new team configuration is better
                new_value = value + player['value']
                new_team_list = team_list + [player]
                new_team_tuple = dict_to_tuple(new_team)
                
                current_value, current_team_list = dp.get((new_budget, new_team_tuple), (0, []))
                if new_value > current_value:
                    dp[(new_budget, new_team_tuple)] = (new_value, new_team_list)
        
        # Debug: Print progress
        processed_states += len(current_dp)
        progress_percentage = (processed_states / total_states) * 100
        print(f"Progress: {progress_percentage:.2f}%")
    
    # Debug: Print final DP state before extracting the best configuration
    print("\nFinal DP table before extracting the best configuration:")
    for k, v in dp.items():
        spent_budget, team = k
        print(f"  Budget spent: {spent_budget}, Team composition: {dict(team)}, Current value: {v[0]}")
    
    if not dp:
        raise ValueError("No valid team configuration could be created within the given budget and position limits.")
    
    # Extract the best value configuration
    best_value, best_team = max(dp.values(), key=lambda x: x[0])
    
    return best_team, best_value

# Example usage
file_path = '/home/sam/Projects/fantasyFootball/knapsack1.ods'  # Path to your spreadsheet
players = load_players_from_spreadsheet(file_path)

budget = 196
position_limits = {'RB': 2, 'WR': 4, 'QB': 2, 'TE': 1, 'K': 1, 'D': 1}

best_team, best_value = knapsack_fantasy_football(players, budget, position_limits)

print("Best team configuration:")
for player in best_team:
    print(player)

print(f"Total Value: {best_value}")
