import pandas as pd
import os
from datetime import datetime
import uuid

def safe_read_csv(file_path, default_columns):
    """Safely read CSV file with proper error handling"""
    try:
        # Check if file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            df = pd.read_csv(file_path)
            # Check if DataFrame is empty or has wrong columns
            if df.empty or not all(col in df.columns for col in default_columns):
                return create_empty_dataframe(default_columns)
            return df
        else:
            return create_empty_dataframe(default_columns)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, Exception) as e:
        print(f"Error reading {file_path}: {e}")
        return create_empty_dataframe(default_columns)

def create_empty_dataframe(columns):
    """Create an empty DataFrame with specified columns"""
    return pd.DataFrame(columns=columns)

def ensure_data_directory():
    """Ensure data directory exists"""
    if not os.path.exists('data'):
        os.makedirs('data')

def initialize_data_files():
    """Initialize all CSV data files with proper headers"""
    ensure_data_directory()
    
    # Users file
    users_columns = ['user_id', 'username', 'email', 'password_hash', 'is_admin', 'created_at']
    users_df = safe_read_csv('data/users.csv', users_columns)
    users_df.to_csv('data/users.csv', index=False)
    
    # Contests file
    contests_columns = ['contest_id', 'name', 'match_id', 'entry_fee', 'prize_pool', 'max_participants', 'created_by', 'created_at', 'status']
    contests_df = safe_read_csv('data/contests.csv', contests_columns)
    contests_df.to_csv('data/contests.csv', index=False)
    
    # Teams file
    teams_columns = ['team_id', 'user_id', 'contest_id', 'team_name', 'players', 'captain', 'vice_captain', 'total_points', 'created_at']
    teams_df = safe_read_csv('data/teams.csv', teams_columns)
    teams_df.to_csv('data/teams.csv', index=False)
    
    # Performances file
    performances_columns = ['performance_id', 'match_id', 'player_name', 'team_name', 'runs', 'balls_faced', 'fours', 'sixes', 'wickets', 'overs_bowled', 'runs_conceded', 'catches', 'stumpings', 'run_outs', 'total_points']
    performances_df = safe_read_csv('data/performances.csv', performances_columns)
    performances_df.to_csv('data/performances.csv', index=False)
    
    # Results file
    results_columns = ['result_id', 'contest_id', 'match_id', 'user_id', 'team_id', 'total_points', 'rank', 'prize_amount', 'created_at']
    results_df = safe_read_csv('data/results.csv', results_columns)
    results_df.to_csv('data/results.csv', index=False)

def save_contest(name, match_id, entry_fee, prize_pool, max_participants, created_by):
    """Save new contest with error handling"""
    try:
        contests_columns = ['contest_id', 'name', 'match_id', 'entry_fee', 'prize_pool', 'max_participants', 'created_by', 'created_at', 'status']
        contests_df = safe_read_csv('data/contests.csv', contests_columns)
        
        contest_id = str(uuid.uuid4())
        new_contest = {
            'contest_id': contest_id,
            'name': name,
            'match_id': match_id,
            'entry_fee': entry_fee,
            'prize_pool': prize_pool,
            'max_participants': max_participants,
            'created_by': created_by,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        contests_df = pd.concat([contests_df, pd.DataFrame([new_contest])], ignore_index=True)
        contests_df.to_csv('data/contests.csv', index=False)
        return contest_id
    except Exception as e:
        print(f"Error saving contest: {e}")
        return None

def save_team(user_id, contest_id, team_name, players, captain, vice_captain):
    """Save user team with validation for one team per contest"""
    try:
        teams_columns = ['team_id', 'user_id', 'contest_id', 'team_name', 'players', 'captain', 'vice_captain', 'total_points', 'created_at']
        teams_df = safe_read_csv('data/teams.csv', teams_columns)
        
        # Check if user already has a team in this contest
        existing_team = teams_df[
            (teams_df['user_id'] == user_id) & 
            (teams_df['contest_id'] == contest_id)
        ]
        
        if not existing_team.empty:
            print(f"User {user_id} already has a team in contest {contest_id}")
            return None  # User already has a team in this contest
        
        team_id = str(uuid.uuid4())
        new_team = {
            'team_id': team_id,
            'user_id': user_id,
            'contest_id': contest_id,
            'team_name': team_name,
            'players': ','.join(players),
            'captain': captain,
            'vice_captain': vice_captain,
            'total_points': 0,
            'created_at': datetime.now().isoformat()
        }
        
        teams_df = pd.concat([teams_df, pd.DataFrame([new_team])], ignore_index=True)
        teams_df.to_csv('data/teams.csv', index=False)
        return team_id
    except Exception as e:
        print(f"Error saving team: {e}")
        return None

def get_contests():
    """Get all contests with error handling"""
    contests_columns = ['contest_id', 'name', 'match_id', 'entry_fee', 'prize_pool', 'max_participants', 'created_by', 'created_at', 'status']
    return safe_read_csv('data/contests.csv', contests_columns)

def get_user_teams(user_id):
    """Get teams for a specific user with error handling"""
    teams_columns = ['team_id', 'user_id', 'contest_id', 'team_name', 'players', 'captain', 'vice_captain', 'total_points', 'created_at']
    teams_df = safe_read_csv('data/teams.csv', teams_columns)
    
    if not teams_df.empty:
        return teams_df[teams_df['user_id'] == user_id]
    return teams_df

def get_performances(match_id):
    """Get performances for a specific match"""
    performances_columns = ['performance_id', 'match_id', 'player_name', 'team_name', 'runs', 'balls_faced', 'fours', 'sixes', 'wickets', 'overs_bowled', 'runs_conceded', 'catches', 'stumpings', 'run_outs', 'total_points']
    performances_df = safe_read_csv('data/performances.csv', performances_columns)
    
    if not performances_df.empty:
        return performances_df[performances_df['match_id'] == match_id]
    return performances_df

def save_performance(match_id, player_name, team_name, performance_data):
    """Save player performance with error handling"""
    try:
        performances_columns = ['performance_id', 'match_id', 'player_name', 'team_name', 'runs', 'balls_faced', 'fours', 'sixes', 'wickets', 'overs_bowled', 'runs_conceded', 'catches', 'stumpings', 'run_outs', 'total_points']
        performances_df = safe_read_csv('data/performances.csv', performances_columns)
        
        # Check if performance already exists
        existing = performances_df[
            (performances_df['match_id'] == match_id) & 
            (performances_df['player_name'] == player_name)
        ]
        
        if not existing.empty:
            # Update existing performance
            idx = existing.index[0]
            for key, value in performance_data.items():
                if key in performances_df.columns:
                    performances_df.loc[idx, key] = value
        else:
            # Add new performance
            performance_id = str(uuid.uuid4())
            new_performance = {
                'performance_id': performance_id,
                'match_id': match_id,
                'player_name': player_name,
                'team_name': team_name,
                **performance_data
            }
            
            performances_df = pd.concat([performances_df, pd.DataFrame([new_performance])], ignore_index=True)
        
        performances_df.to_csv('data/performances.csv', index=False)
        return True
    except Exception as e:
        print(f"Error saving performance: {e}")
        return False

def update_contest_status(contest_id, new_status):
    """Update contest status"""
    try:
        contests_columns = ['contest_id', 'name', 'match_id', 'entry_fee', 'prize_pool', 'max_participants', 'created_by', 'created_at', 'status']
        contests_df = safe_read_csv('data/contests.csv', contests_columns)
        
        if not contests_df.empty:
            contests_df.loc[contests_df['contest_id'] == contest_id, 'status'] = new_status
            contests_df.to_csv('data/contests.csv', index=False)
            return True
        return False
    except Exception as e:
        print(f"Error updating contest status: {e}")
        return False

def get_leaderboard(contest_id):
    """Get leaderboard for a specific contest"""
    teams_columns = ['team_id', 'user_id', 'contest_id', 'team_name', 'players', 'captain', 'vice_captain', 'total_points', 'created_at']
    teams_df = safe_read_csv('data/teams.csv', teams_columns)
    
    users_columns = ['user_id', 'username', 'email', 'password_hash', 'is_admin', 'created_at']
    users_df = safe_read_csv('data/users.csv', users_columns)
    
    if not teams_df.empty and not users_df.empty:
        contest_teams = teams_df[teams_df['contest_id'] == contest_id]
        
        if not contest_teams.empty:
            # Merge with users to get usernames
            leaderboard = contest_teams.merge(users_df[['user_id', 'username']], on='user_id', how='left')
            
            # Sort by total points and add rank
            leaderboard = leaderboard.sort_values('total_points', ascending=False).reset_index(drop=True)
            leaderboard['rank'] = range(1, len(leaderboard) + 1)
            
            return leaderboard
    
    return pd.DataFrame()

def update_team_points(team_id, total_points):
    """Update team total points"""
    try:
        teams_columns = ['team_id', 'user_id', 'contest_id', 'team_name', 'players', 'captain', 'vice_captain', 'total_points', 'created_at']
        teams_df = safe_read_csv('data/teams.csv', teams_columns)
        
        if not teams_df.empty:
            teams_df.loc[teams_df['team_id'] == team_id, 'total_points'] = total_points
            teams_df.to_csv('data/teams.csv', index=False)
            return True
        return False
    except Exception as e:
        print(f"Error updating team points: {e}")
        return False

def get_all_teams():
    """Get all teams"""
    teams_columns = ['team_id', 'user_id', 'contest_id', 'team_name', 'players', 'captain', 'vice_captain', 'total_points', 'created_at']
    return safe_read_csv('data/teams.csv', teams_columns)