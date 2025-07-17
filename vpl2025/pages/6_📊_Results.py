import streamlit as st
import pandas as pd
from utils.auth import check_authentication
from utils.data_manager import get_contests, get_leaderboard, get_performances
from utils.constants import FIXTURES_DATA

st.set_page_config(page_title="Results", page_icon="📊", layout="wide")

if not check_authentication():
    st.stop()

st.title("📊 Results & Leaderboards")

# Get all contests
contests_df = get_contests()

if not contests_df.empty:
    # Contest selection
    contest_names = contests_df['name'].tolist()
    selected_contest_name = st.selectbox("Select Contest", contest_names)
    
    if selected_contest_name:
        contest_info = contests_df[contests_df['name'] == selected_contest_name].iloc[0]
        
        # Contest details
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Entry Fee", f"₹{contest_info['entry_fee']}")
        
        with col2:
            st.metric("Prize Pool", f"₹{contest_info['prize_pool']}")
        
        with col3:
            st.metric("Max Participants", contest_info['max_participants'])
        
        # Match details
        match_info = next((f for f in FIXTURES_DATA if f['match_id'] == contest_info['match_id']), None)
        if match_info:
            st.info(f"Match: {match_info['teams'][0]} vs {match_info['teams'][1]} - {match_info['time']} ({match_info['day']})")
        
        # Leaderboard
        st.markdown("### 🏆 Leaderboard")
        
        leaderboard = get_leaderboard(contest_info['contest_id'])
        
        if not leaderboard.empty:
            # Display leaderboard
            leaderboard_display = leaderboard[['rank', 'username', 'team_name', 'total_points']].copy()
            leaderboard_display.columns = ['Rank', 'User', 'Team Name', 'Total Points']
            
            # Add medals for top 3
            for i, row in leaderboard_display.iterrows():
                if row['Rank'] == 1:
                    leaderboard_display.loc[i, 'Rank'] = "🥇 1st"
                elif row['Rank'] == 2:
                    leaderboard_display.loc[i, 'Rank'] = "🥈 2nd"
                elif row['Rank'] == 3:
                    leaderboard_display.loc[i, 'Rank'] = "🥉 3rd"
                else:
                    leaderboard_display.loc[i, 'Rank'] = f"#{row['Rank']}"
            
            st.dataframe(leaderboard_display, use_container_width=True)
            
            # Team details
            st.markdown("### 👥 Team Details")
            
            for _, team in leaderboard.iterrows():
                with st.expander(f"🏏 {team['team_name']} - {team['username']} (Rank #{team['rank']})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Team Players (7):**")
                        players = team['players'].split(',')
                        for i, player in enumerate(players, 1):
                            if player == team['captain']:
                                st.write(f"{i}. 👑 {player} (Captain - 2x)")
                            elif player == team['vice_captain']:
                                st.write(f"{i}. 🔰 {player} (Vice-Captain - 1.5x)")
                            else:
                                st.write(f"{i}. ⚡ {player}")
                    
                    with col2:
                        st.metric("Total Points", team['total_points'])
                        st.metric("Rank", f"#{team['rank']}")
                        st.write(f"**Created:** {team['created_at']}")
            
            # Match performances
            if match_info and match_info['status'] == 'completed':
                st.markdown("### 🎯 Match Performances")
                
                performances = get_performances(contest_info['match_id'])
                
                if not performances.empty:
                    # Top performers
                    top_performers = performances.nlargest(10, 'total_points')
                    
                    st.subheader("🌟 Top Performers")
                    
                    for i, (_, player) in enumerate(top_performers.iterrows(), 1):
                        with st.expander(f"#{i} {player['player_name']} - {player['total_points']} points"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write("**Batting**")
                                st.write(f"Runs: {player['runs']}")
                                st.write(f"Balls: {player['balls_faced']}")
                                st.write(f"4s: {player['fours']}")
                                st.write(f"6s: {player['sixes']}")
                            
                            with col2:
                                st.write("**Bowling**")
                                st.write(f"Wickets: {player['wickets']}")
                                st.write(f"Overs: {player['overs_bowled']}")
                                st.write(f"Runs Given: {player['runs_conceded']}")
                            
                            with col3:
                                st.write("**Fielding**")
                                st.write(f"Catches: {player['catches']}")
                                st.write(f"Stumpings: {player['stumpings']}")
                                st.write(f"Run Outs: {player['run_outs']}")
                    
                    # Full performance table
                    st.subheader("📋 All Performances")
                    st.dataframe(performances, use_container_width=True)
                else:
                    st.info("No performance data available")
        else:
            st.info("No teams have joined this contest yet")
else:
    st.info("No contests available")

# Overall statistics
st.markdown("### 📈 Overall Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_contests = len(contests_df) if not contests_df.empty else 0
    st.metric("Total Contests", total_contests)

with col2:
    active_contests = len(contests_df[contests_df['status'] == 'active']) if not contests_df.empty else 0
    st.metric("Active Contests", active_contests)

with col3:
    completed_contests = len(contests_df[contests_df['status'] == 'completed']) if not contests_df.empty else 0
    st.metric("Completed", completed_contests)

with col4:
    total_prize_pool = contests_df['prize_pool'].sum() if not contests_df.empty else 0
    st.metric("Total Prize Pool", f"₹{total_prize_pool:,}")
