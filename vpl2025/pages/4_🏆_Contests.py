import streamlit as st
import pandas as pd
from utils.auth import initialize_auth, check_authentication
from utils.data_manager import save_contest, get_contests, save_team, get_user_teams
from utils.constants import FIXTURES_DATA, TEAMS_DATA, TEAM_BUDGET

st.set_page_config(page_title="Contests", page_icon="🏆", layout="wide")

# Initialize authentication
initialize_auth()

if not check_authentication():
    st.stop()

# Persistent logout button
def show_logout_button():
    if st.session_state.get('authenticated', False):
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("🚪 Logout", type="secondary", key="logout_contests"):
                from utils.auth import logout
                logout()

def check_user_contest_participation(user_id, contest_id):
    """Check if user already has a team in the contest"""
    user_teams = get_user_teams(user_id)
    if not user_teams.empty:
        existing_team = user_teams[user_teams['contest_id'] == contest_id]
        if not existing_team.empty:
            return existing_team.iloc[0].to_dict()
    return None

show_logout_button()

st.title("🏆 Contest Management")

# Tabs for different contest actions
tab1, tab2, tab3 = st.tabs(["🆕 Create Contest", "📝 Join Contest", "📊 My Contests"])

with tab1:
    if st.session_state.is_admin:
        st.subheader("Create New Contest")
        
        with st.form("create_contest"):
            contest_name = st.text_input("Contest Name", placeholder="e.g., VPL Championship")
            
            # Match selection
            match_options = []
            for fixture in FIXTURES_DATA:
                if fixture['status'] == 'upcoming':
                    match_str = f"Match {fixture['match_no']}: {fixture['teams'][0]} vs {fixture['teams'][1]} - {fixture['time']} ({fixture['day']})"
                    match_options.append((fixture['match_id'], match_str))
            
            if match_options:
                selected_match = st.selectbox("Select Match", options=match_options, format_func=lambda x: x[1])
                
                col1, col2 = st.columns(2)
                with col1:
                    entry_fee = st.number_input("Entry Fee (₹)", min_value=0, value=10)
                    max_participants = st.number_input("Max Participants", min_value=2, value=100)
                
                with col2:
                    prize_pool = st.number_input("Prize Pool (₹)", min_value=0, value=int(entry_fee * max_participants * 0.9))
                    st.info(f"Platform fee: ₹{entry_fee * max_participants * 0.1:.0f}")
                
                submitted = st.form_submit_button("Create Contest")
                
                if submitted:
                    contest_id = save_contest(
                        contest_name,
                        selected_match[0],
                        entry_fee,
                        prize_pool,
                        max_participants,
                        st.session_state.user_id
                    )
                    if contest_id:
                        st.success(f"Contest '{contest_name}' created successfully!")
                        st.rerun()
                    else:
                        st.error("Error creating contest")
            else:
                st.warning("No upcoming matches available for contest creation")
    else:
        st.error("Only administrators can create contests")

with tab2:
    st.subheader("Available Contests")
    
    contests_df = get_contests()
    active_contests = contests_df[contests_df['status'] == 'active'] if not contests_df.empty else pd.DataFrame()
    
    if not active_contests.empty:
        for idx, contest in active_contests.iterrows():
            # Get match info to filter players
            match_info = next((f for f in FIXTURES_DATA if f['match_id'] == contest['match_id']), None)
            
            if match_info:
                st.markdown(f"### {contest['name']}")
                st.write(f"**Match:** {match_info['teams'][0]} vs {match_info['teams'][1]}")
                st.write(f"**Time:** {match_info['time']} ({match_info['day']})")
                st.write(f"**Entry Fee:** ₹{contest['entry_fee']} | **Prize Pool:** ₹{contest['prize_pool']}")
                
                # Check if user already has a team in this contest
                existing_team = check_user_contest_participation(st.session_state.user_id, contest['contest_id'])
                
                if existing_team:
                    st.success(f"✅ You're already in this contest with team: {existing_team['team_name']}")
                    
                    with st.expander("View Team Details"):
                        players = existing_team['players'].split(',')
                        for i, player in enumerate(players, 1):
                            if player == existing_team['captain']:
                                st.write(f"{i}. 👑 {player} (Captain - 2x)")
                            elif player == existing_team['vice_captain']:
                                st.write(f"{i}. 🔰 {player} (Vice-Captain - 1.5x)")
                            else:
                                st.write(f"{i}. ⚡ {player}")
                else:
                    # Team creation form
                    with st.form(f"join_contest_{contest['contest_id']}"):
                        st.subheader("Create Your Team (7 Players)")
                        st.info(f"Select players from {match_info['teams'][0]} and {match_info['teams'][1]} only")
                        
                        team_name = st.text_input("Team Name", placeholder="Enter your team name", key=f"team_name_{contest['contest_id']}")
                        
                        # Player selection - only from playing teams
                        playing_teams = match_info['teams']
                        selected_players = []
                        total_cost = 0
                        
                        # Display players from both teams
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**{playing_teams[0]}**")
                            if playing_teams[0] in TEAMS_DATA:
                                for player in TEAMS_DATA[playing_teams[0]]['players']:
                                    key = f"{contest['contest_id']}_{player['name']}"
                                    if st.checkbox(f"{player['name']} - ₹{player['price']:,}", key=key):
                                        selected_players.append(player['name'])
                                        total_cost += player['price']
                        
                        with col2:
                            st.write(f"**{playing_teams[1]}**")
                            if playing_teams[1] in TEAMS_DATA:
                                for player in TEAMS_DATA[playing_teams[1]]['players']:
                                    key = f"{contest['contest_id']}_{player['name']}"
                                    if st.checkbox(f"{player['name']} - ₹{player['price']:,}", key=key):
                                        selected_players.append(player['name'])
                                        total_cost += player['price']
                        
                        # Budget display
                        st.write(f"**Selected Players:** {len(selected_players)}/7")
                        st.write(f"**Total Cost:** ₹{total_cost:,}")
                        st.write(f"**Budget:** ₹{TEAM_BUDGET:,}")
                        st.write(f"**Remaining:** ₹{TEAM_BUDGET - total_cost:,}")
                        
                        # Show selected players
                        if selected_players:
                            st.write("**Selected Players:**")
                            for i, player in enumerate(selected_players, 1):
                                st.write(f"{i}. {player}")
                        
                        # Captain and Vice-captain selection
                        captain = None
                        vice_captain = None
                        
                        if selected_players:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                captain = st.selectbox("Captain (2x points)", selected_players, key=f"captain_{contest['contest_id']}")
                            
                            with col2:
                                vice_captain_options = [p for p in selected_players if p != captain]
                                if vice_captain_options:
                                    vice_captain = st.selectbox("Vice-Captain (1.5x points)", vice_captain_options, key=f"vc_{contest['contest_id']}")
                        
                        join_submitted = st.form_submit_button("Join Contest")
                        
                        if join_submitted:
                            if len(selected_players) == 7 and total_cost <= TEAM_BUDGET and captain and vice_captain and team_name:
                                try:
                                    team_id = save_team(
                                        st.session_state.user_id,
                                        contest['contest_id'],
                                        team_name,
                                        selected_players,
                                        captain,
                                        vice_captain
                                    )
                                    if team_id:
                                        st.success(f"Successfully joined contest with team '{team_name}'!")
                                        st.rerun()
                                    else:
                                        st.error("You already have a team in this contest")
                                except Exception as e:
                                    st.error(f"Error joining contest: {str(e)}")
                            else:
                                if len(selected_players) != 7:
                                    st.error("Please select exactly 7 players")
                                elif total_cost > TEAM_BUDGET:
                                    st.error("Team cost exceeds budget limit")
                                elif not captain or not vice_captain:
                                    st.error("Please select both captain and vice-captain")
                                elif not team_name:
                                    st.error("Please enter a team name")
                
                st.markdown("---")
    else:
        st.info("No active contests available")

with tab3:
    st.subheader("My Teams")
    
    user_teams = get_user_teams(st.session_state.user_id)
    
    if not user_teams.empty:
        contests_df = get_contests()
        
        for idx, team in user_teams.iterrows():
            contest_info = contests_df[contests_df['contest_id'] == team['contest_id']]
            
            if not contest_info.empty:
                contest_info = contest_info.iloc[0]
                
                st.markdown(f"### {team['team_name']}")
                st.write(f"**Contest:** {contest_info['name']}")
                st.write(f"**Total Points:** {team['total_points']}")
                st.write(f"**Created:** {team['created_at']}")
                
                with st.expander("View Team Details"):
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
                        st.metric("Team Size", f"{len(players)} players")
                        st.metric("Status", "Active")
                
                st.markdown("---")
    else:
        st.info("You haven't joined any contests yet")

# Navigation
st.markdown("---")
st.markdown("### Quick Navigation")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 View Results", use_container_width=True):
        st.switch_page("pages/6_📊_Results.py")

with col2:
    if st.button("🏅 View Winners", use_container_width=True):
        st.switch_page("pages/8_🏅_Winners.py")

with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")