import streamlit as st
import pandas as pd
from utils.auth import initialize_auth, check_authentication
from utils.constants import FIXTURES_DATA, TEAMS_DATA
from utils.scoring import calculate_total_player_points, update_all_team_points
from utils.data_manager import save_performance, get_performances, get_contests, update_contest_status

st.set_page_config(page_title="Admin Panel", page_icon="⚙️", layout="wide")

# Initialize authentication
initialize_auth()

if not check_authentication():
    st.stop()

if not st.session_state.is_admin:
    st.error("Access denied. Admin privileges required.")
    st.stop()

# Persistent logout button
def show_logout_button():
    if st.session_state.get('authenticated', False):
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("🚪 Logout", type="secondary", key="logout_admin"):
                from utils.auth import logout
                logout()

show_logout_button()

st.title("⚙️ Admin Panel")

# Admin tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🔴 Match Control", "⚡ Live Scoring", "🏆 Contest Management", "👥 User Management"])

with tab1:
    st.subheader("Admin Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        try:
            users_df = pd.read_csv('data/users.csv')
            st.metric("Total Users", len(users_df))
        except:
            st.metric("Total Users", 0)
    
    with col2:
        contests_df = get_contests()
        active_contests = len(contests_df[contests_df['status'] == 'active']) if not contests_df.empty else 0
        st.metric("Active Contests", active_contests)
    
    with col3:
        try:
            teams_df = pd.read_csv('data/teams.csv')
            st.metric("Total Teams", len(teams_df))
        except:
            st.metric("Total Teams", 0)
    
    with col4:
        live_matches = len([f for f in FIXTURES_DATA if f['status'] == 'live'])
        st.metric("Live Matches", live_matches)
    
    # Recent activity
    st.subheader("Recent Activity")
    
    if not contests_df.empty:
        st.dataframe(contests_df.tail(10).reset_index(drop=True), use_container_width=True, hide_index=True)
    else:
        st.info("No contest data available")

with tab2:
    st.subheader("🔴 Match Control Center")
    st.info("📝 **New Feature**: Admins can now manually control match status")
    
    # Match status control
    st.markdown("### Match Status Management")
    
    # Filter matches
    status_filter = st.selectbox("Filter by Status", ["All", "upcoming", "live", "completed"])
    
    filtered_matches = FIXTURES_DATA.copy()
    if status_filter != "All":
        filtered_matches = [f for f in filtered_matches if f['status'] == status_filter]
    
    # Display matches with status control
    for match in filtered_matches:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**Match {match['match_no']}**: {match['teams'][0]} vs {match['teams'][1]}")
                st.write(f"🕐 {match['time']} ({match['day']})")
            
            with col2:
                # Current status
                status_color = {
                    'upcoming': '🟡',
                    'live': '🔴',
                    'completed': '🟢'
                }
                st.write(f"{status_color.get(match['status'], '⚪')} {match['status'].title()}")
            
            with col3:
                # Status change buttons
                if match['status'] == 'upcoming':
                    if st.button("🔴 Make Live", key=f"live_{match['match_id']}"):
                        # Update match status in FIXTURES_DATA
                        for i, fixture in enumerate(FIXTURES_DATA):
                            if fixture['match_id'] == match['match_id']:
                                FIXTURES_DATA[i]['status'] = 'live'
                                break
                        st.success(f"Match {match['match_no']} is now LIVE!")
                        st.rerun()
                
                elif match['status'] == 'live':
                    if st.button("🟢 Complete", key=f"complete_{match['match_id']}"):
                        # Update match status
                        for i, fixture in enumerate(FIXTURES_DATA):
                            if fixture['match_id'] == match['match_id']:
                                FIXTURES_DATA[i]['status'] = 'completed'
                                break
                        
                        # Update all team points for this match
                        update_all_team_points(match['match_id'])
                        st.success(f"Match {match['match_no']} completed!")
                        st.rerun()
            
            with col4:
                # Quick actions
                if match['status'] == 'live':
                    if st.button("📊 Score", key=f"score_{match['match_id']}"):
                        st.session_state.selected_match_for_scoring = match['match_id']
                        st.switch_page("pages/5_⚡_Live.py")
                
                elif match['status'] == 'completed':
                    if st.button("📈 Results", key=f"results_{match['match_id']}"):
                        st.switch_page("pages/6_📊_Results.py")
            
            st.markdown("---")

with tab3:
    st.subheader("⚡ Live Scoring System")
    
    # Match selection for scoring
    live_matches = [f for f in FIXTURES_DATA if f['status'] == 'live']
    
    if live_matches:
        match_options = []
        for fixture in live_matches:
            match_str = f"Match {fixture['match_no']}: {fixture['teams'][0]} vs {fixture['teams'][1]}"
            match_options.append((fixture['match_id'], match_str))
        
        selected_match = st.selectbox("Select Live Match for Scoring", options=match_options, format_func=lambda x: x[1])
        
        if selected_match:
            match_info = next((f for f in FIXTURES_DATA if f['match_id'] == selected_match[0]), None)
            
            if match_info:
                st.info(f"📊 Updating scores for: {match_info['teams'][0]} vs {match_info['teams'][1]}")
                
                # Get all players from both teams
                team1_players = TEAMS_DATA.get(match_info['teams'][0], {}).get('players', [])
                team2_players = TEAMS_DATA.get(match_info['teams'][1], {}).get('players', [])
                
                all_players = team1_players + team2_players
                
                # Player performance form
                with st.form("player_performance"):
                    st.subheader("Enter Player Performance")
                    
                    player_name = st.selectbox("Select Player", options=[p['name'] for p in all_players])
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("🏏 Batting")
                        runs = st.number_input("Runs", min_value=0, value=0)
                        balls_faced = st.number_input("Balls Faced", min_value=0, value=0)
                        fours = st.number_input("Fours", min_value=0, value=0)
                        sixes = st.number_input("Sixes", min_value=0, value=0)
                        is_out = st.checkbox("Is Out?")
                    
                    with col2:
                        st.subheader("🎳 Bowling")
                        wickets = st.number_input("Wickets", min_value=0, value=0)
                        overs_bowled = st.number_input("Overs Bowled", min_value=0.0, value=0.0, step=0.1)
                        runs_conceded = st.number_input("Runs Conceded", min_value=0, value=0)
                        maidens = st.number_input("Maiden Overs", min_value=0, value=0)
                    
                    with col3:
                        st.subheader("🥎 Fielding")
                        catches = st.number_input("Catches", min_value=0, value=0)
                        stumpings = st.number_input("Stumpings", min_value=0, value=0)
                        run_outs = st.number_input("Run Outs", min_value=0, value=0)
                    
                    submitted = st.form_submit_button("📊 Update Performance", type="primary")
                    
                    if submitted:
                        # Calculate points
                        performance_data = {
                            'runs': runs,
                            'balls_faced': balls_faced,
                            'fours': fours,
                            'sixes': sixes,
                            'is_out': is_out,
                            'wickets': wickets,
                            'overs_bowled': overs_bowled,
                            'runs_conceded': runs_conceded,
                            'maidens': maidens,
                            'catches': catches,
                            'stumpings': stumpings,
                            'run_outs': run_outs
                        }
                        
                        total_points = calculate_total_player_points(performance_data)
                        performance_data['total_points'] = total_points
                        
                        # Find player's team
                        player_team = None
                        for team_name, team_info in TEAMS_DATA.items():
                            if any(p['name'] == player_name for p in team_info['players']):
                                player_team = team_name
                                break
                        
                        # Save performance
                        if save_performance(selected_match[0], player_name, player_team, performance_data):
                            st.success(f"✅ Performance updated for {player_name}! Points: {total_points}")
                        else:
                            st.error("❌ Error saving performance")
                
                # Update all team points button
                if st.button("🔄 Update All Team Points", type="secondary"):
                    if update_all_team_points(selected_match[0]):
                        st.success("✅ All team points updated successfully!")
                    else:
                        st.error("❌ Error updating team points")
                
                # Current match performances
                st.subheader("📊 Current Match Performances")
                performances = get_performances(selected_match[0])
                
                if not performances.empty:
                    # Reset index to start from 1
                    performances_display = performances.reset_index(drop=True)
                    performances_display.index = performances_display.index + 1
                    st.dataframe(performances_display, use_container_width=True)
                else:
                    st.info("No performances recorded for this match yet")
    else:
        st.info("ℹ️ No live matches available for scoring")
        st.markdown("### 🔴 To start scoring:")
        st.markdown("1. Go to **Match Control** tab")
        st.markdown("2. Find an upcoming match")
        st.markdown("3. Click **🔴 Make Live** button")
        st.markdown("4. Return here to start scoring")

with tab4:
    st.subheader("🏆 Contest Management")
    
    contests_df = get_contests()
    
    if not contests_df.empty:
        # Contest status management
        st.subheader("Update Contest Status")
        
        # Reset index to start from 1
        contests_display = contests_df.reset_index(drop=True)
        contests_display.index = contests_display.index + 1
        
        for idx, contest in contests_df.iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{contest['name']}**")
                st.write(f"Entry Fee: ₹{contest['entry_fee']} | Prize Pool: ₹{contest['prize_pool']}")
            
            with col2:
                st.write(f"Status: {contest['status'].title()}")
            
            with col3:
                new_status = st.selectbox(
                    "Change Status",
                    ["active", "live", "completed", "cancelled"],
                    index=["active", "live", "completed", "cancelled"].index(contest['status']),
                    key=f"status_{contest['contest_id']}"
                )
                
                if st.button("Update", key=f"update_{contest['contest_id']}"):
                    if update_contest_status(contest['contest_id'], new_status):
                        st.success(f"Contest status updated to {new_status}")
                        st.rerun()
                    else:
                        st.error("Error updating contest status")
    else:
        st.info("No contests available")

with tab5:
    st.subheader("👥 User Management")
    
    try:
        users_df = pd.read_csv('data/users.csv')
        
        if not users_df.empty:
            # User statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Users", len(users_df))
                st.metric("Admin Users", len(users_df[users_df['is_admin'] == True]))
            
            with col2:
                st.metric("Regular Users", len(users_df[users_df['is_admin'] == False]))
                st.metric("New Users Today", 0)  # Would calculate based on created_at
            
            # User list
            st.subheader("All Users")
            
            # Reset index to start from 1
            users_display = users_df[['username', 'email', 'is_admin', 'created_at']].reset_index(drop=True)
            users_display.index = users_display.index + 1
            st.dataframe(users_display, use_container_width=True)
        else:
            st.info("No users found")
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")
        st.info("No users found")
