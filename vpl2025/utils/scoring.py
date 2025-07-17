import pandas as pd
from utils.constants import CAPTAIN_MULTIPLIER, VICE_CAPTAIN_MULTIPLIER

# Cricket Scoring System for 7-player format
CRICKET_SCORING_SYSTEM = {
    "batting": {
        "run": 1,
        "boundary": 1,
        "six": 2,
        "fifty": 8,
        "century": 16,
        "duck": -2
    },
    "bowling": {
        "wicket": 25,
        "maiden_over": 12,
        "three_wickets": 4,
        "four_wickets": 8,
        "five_wickets": 16,
        "lbw_bowled": 8
    },
    "fielding": {
        "catch": 8,
        "stumping": 12,
        "run_out_direct": 12,
        "run_out_indirect": 6,
        "three_catches": 4
    },
    "other": {
        "playing_seven": 4,  # Updated from playing_xi
        "captain_multiplier": CAPTAIN_MULTIPLIER,
        "vice_captain_multiplier": VICE_CAPTAIN_MULTIPLIER
    },
    "economy_rate": {
        "below_5": 6,
        "5_to_599": 4,
        "6_to_7": 2,
        "10_to_11": -2,
        "11_to_12": -4,
        "above_12": -6
    },
    "strike_rate": {
        "above_170": 6,
        "150_to_170": 4,
        "130_to_150": 2,
        "60_to_70": -2,
        "50_to_60": -4,
        "below_50": -6
    }
}

def calculate_batting_points(runs, balls_faced, fours, sixes, is_out):
    """Calculate batting points based on performance"""
    points = 0
    
    # Base runs
    points += runs * CRICKET_SCORING_SYSTEM['batting']['run']
    
    # Boundary bonuses
    points += fours * CRICKET_SCORING_SYSTEM['batting']['boundary']
    points += sixes * CRICKET_SCORING_SYSTEM['batting']['six']
    
    # Milestone bonuses
    if runs >= 100:
        points += CRICKET_SCORING_SYSTEM['batting']['century']
    elif runs >= 50:
        points += CRICKET_SCORING_SYSTEM['batting']['fifty']
    
    # Duck penalty
    if is_out and runs == 0:
        points += CRICKET_SCORING_SYSTEM['batting']['duck']
    
    # Strike rate bonus/penalty
    if balls_faced >= 10:
        strike_rate = (runs / balls_faced) * 100
        if strike_rate > 170:
            points += CRICKET_SCORING_SYSTEM['strike_rate']['above_170']
        elif strike_rate >= 150:
            points += CRICKET_SCORING_SYSTEM['strike_rate']['150_to_170']
        elif strike_rate >= 130:
            points += CRICKET_SCORING_SYSTEM['strike_rate']['130_to_150']
        elif strike_rate <= 70:
            points += CRICKET_SCORING_SYSTEM['strike_rate']['60_to_70']
        elif strike_rate <= 60:
            points += CRICKET_SCORING_SYSTEM['strike_rate']['50_to_60']
        elif strike_rate < 50:
            points += CRICKET_SCORING_SYSTEM['strike_rate']['below_50']
    
    return points

def calculate_bowling_points(wickets, overs_bowled, runs_conceded, maidens):
    """Calculate bowling points based on performance"""
    points = 0
    
    # Wickets
    points += wickets * CRICKET_SCORING_SYSTEM['bowling']['wicket']
    
    # Wicket bonuses
    if wickets >= 5:
        points += CRICKET_SCORING_SYSTEM['bowling']['five_wickets']
    elif wickets >= 4:
        points += CRICKET_SCORING_SYSTEM['bowling']['four_wickets']
    elif wickets >= 3:
        points += CRICKET_SCORING_SYSTEM['bowling']['three_wickets']
    
    # Maiden overs
    points += maidens * CRICKET_SCORING_SYSTEM['bowling']['maiden_over']
    
    # Economy rate bonus/penalty
    if overs_bowled >= 2:
        economy_rate = runs_conceded / overs_bowled
        if economy_rate < 5:
            points += CRICKET_SCORING_SYSTEM['economy_rate']['below_5']
        elif economy_rate < 6:
            points += CRICKET_SCORING_SYSTEM['economy_rate']['5_to_599']
        elif economy_rate <= 7:
            points += CRICKET_SCORING_SYSTEM['economy_rate']['6_to_7']
        elif economy_rate >= 10 and economy_rate <= 11:
            points += CRICKET_SCORING_SYSTEM['economy_rate']['10_to_11']
        elif economy_rate > 11 and economy_rate <= 12:
            points += CRICKET_SCORING_SYSTEM['economy_rate']['11_to_12']
        elif economy_rate > 12:
            points += CRICKET_SCORING_SYSTEM['economy_rate']['above_12']
    
    return points

def calculate_fielding_points(catches, stumpings, run_outs):
    """Calculate fielding points"""
    points = 0
    
    # Catches
    points += catches * CRICKET_SCORING_SYSTEM['fielding']['catch']
    if catches >= 3:
        points += CRICKET_SCORING_SYSTEM['fielding']['three_catches']
    
    # Stumpings
    points += stumpings * CRICKET_SCORING_SYSTEM['fielding']['stumping']
    
    # Run outs
    points += run_outs * CRICKET_SCORING_SYSTEM['fielding']['run_out_direct']
    
    return points

def calculate_total_player_points(performance_data):
    """Calculate total points for a player"""
    batting_points = calculate_batting_points(
        performance_data.get('runs', 0),
        performance_data.get('balls_faced', 0),
        performance_data.get('fours', 0),
        performance_data.get('sixes', 0),
        performance_data.get('is_out', False)
    )
    
    bowling_points = calculate_bowling_points(
        performance_data.get('wickets', 0),
        performance_data.get('overs_bowled', 0),
        performance_data.get('runs_conceded', 0),
        performance_data.get('maidens', 0)
    )
    
    fielding_points = calculate_fielding_points(
        performance_data.get('catches', 0),
        performance_data.get('stumpings', 0),
        performance_data.get('run_outs', 0)
    )
    
    # Playing 7 bonus
    total_points = batting_points + bowling_points + fielding_points + CRICKET_SCORING_SYSTEM['other']['playing_seven']
    
    return total_points

def calculate_team_points(team_players, performances, captain, vice_captain):
    """Calculate total points for a 7-player fantasy team"""
    total_points = 0
    
    for player in team_players:
        player_performance = performances.get(player, {})
        player_points = calculate_total_player_points(player_performance)
        
        # Apply captain/vice-captain multipliers
        if player == captain:
            player_points *= CRICKET_SCORING_SYSTEM['other']['captain_multiplier']
        elif player == vice_captain:
            player_points *= CRICKET_SCORING_SYSTEM['other']['vice_captain_multiplier']
        
        total_points += player_points
    
    return total_points

def update_all_team_points(match_id):
    """Update points for all teams after match completion"""
    from utils.data_manager import get_all_teams, update_team_points, get_performances
    
    # Get all performances for this match
    match_performances = get_performances(match_id)
    
    # Convert to dictionary for easier lookup
    performances_dict = {}
    for _, perf in match_performances.iterrows():
        performances_dict[perf['player_name']] = perf.to_dict()
    
    # Get all teams
    teams_df = get_all_teams()
    
    for _, team in teams_df.iterrows():
        team_players = team['players'].split(',')
        team_points = calculate_team_points(
            team_players,
            performances_dict,
            team['captain'],
            team['vice_captain']
        )
        
        update_team_points(team['team_id'], team_points)
