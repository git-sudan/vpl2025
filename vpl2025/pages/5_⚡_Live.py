import streamlit as st
import pandas as pd
from utils.auth import check_authentication
from utils.constants import FIXTURES_DATA, TEAMS_DATA
from utils.data_manager import get_performances, save_performance
from utils.scoring import calculate_total_player_points

st.set_page_config(page_title="Live Scoring", page_icon="⚡", layout="wide")

if not check_authentication():
    st.stop()

st.title("⚡ Live Scoring")

# Live matches
live_matches = [f for f in FIXTURES_DATA if f['status'] == 'live']
upcoming_matches = [f for f in FIXTURES_DATA if f['status'] == 'upcoming']

if live_matches:
    st.markdown("### 🔴 Live Matches")
    
    for match in live_matches:
        with st.expander(f"🏏 LIVE: {match['teams'][0]} vs {match['teams'][1]} - {match['time']}"):
            # Get performances for this match
            performances = get_performances(match['match_id'])
            
            if not performances.empty:
                st.subheader("Current Performances")
                
                # Display performances in a nice format
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**{match['teams'][0]}**")
                    team1_players = TEAMS_DATA.get(match['teams'][0], {}).get('players', [])
                    
                    for player in team1_players:
                        player_perf = performances[performances['player_name'] == player['name']]
                        if not player_perf.empty:
                            perf = player_perf.iloc[0]
                            st.write(f"**{player['name']}**: {perf['runs']} runs, {perf['wickets']} wickets - {perf['total_points']} pts")
                        else:
                            st.write(f"**{player['name']}**: No performance data")
                
                with col2:
                    st.markdown(f"**{match['teams'][1]}**")
                    team2_players = TEAMS_DATA.get(match['teams'][1], {}).get('players', [])
                    
                    for player in team2_players:
                        player_perf = performances[performances['player_name'] == player['name']]
                        if not player_perf.empty:
                            perf = player_perf.iloc[0]
                            st.write(f"**{player['name']}**: {perf['runs']} runs, {perf['wickets']} wickets - {perf['total_points']} pts")
                        else:
                            st.write(f"**{player['name']}**: No performance data")
            else:
                st.info("No performance data available yet")
                
            # Admin can update scores
            if st.session_state.is_admin:
                if st.button(f"Update Scores", key=f"update_{match['match_id']}"):
                    st.switch_page("pages/7_⚙️_Admin.py")

if upcoming_matches:
    st.markdown("### 📅 Upcoming Matches")
    
    for match in upcoming_matches[:3]:  # Show next 3 matches
        with st.expander(f"🏏 {match['teams'][0]} vs {match['teams'][1]} - {match['time']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Time:** {match['time']}")
                st.write(f"**Day:** {match['day']}")
            
            with col2:
                st.write(f"**Status:** {match['status'].title()}")
                if st.button(f"Create Contest", key=f"contest_{match['match_id']}"):
                    st.switch_page("pages/4_🏆_Contests.py")

# If no live matches
if not live_matches:
    st.info("No live matches at the moment")
    
    # Show recent completed matches
    completed_matches = [f for f in FIXTURES_DATA if f['status'] == 'completed']
    
    if completed_matches:
        st.markdown("### 🏁 Recent Completed Matches")
        
        for match in completed_matches[-3:]:  # Show last 3 completed matches
            with st.expander(f"🏏 COMPLETED: {match['teams'][0]} vs {match['teams'][1]} - {match['time']}"):
                # Get final performances
                performances = get_performances(match['match_id'])
                
                if not performances.empty:
                    st.subheader("Final Performances")
                    st.dataframe(performances[['player_name', 'team_name', 'runs', 'wickets', 'total_points']], use_container_width=True)
                    
                    if st.button(f"View Results", key=f"results_{match['match_id']}"):
                        st.switch_page("pages/6_📊_Results.py")
                else:
                    st.info("No performance data available")
