import streamlit as st
import pandas as pd
from utils.auth import initialize_auth, check_authentication
from utils.data_manager import get_contests, get_leaderboard
from utils.constants import FIXTURES_DATA

st.set_page_config(page_title="Winners", page_icon="🏅", layout="wide")

# Initialize authentication
initialize_auth()

if not check_authentication():
    st.stop()

# Persistent logout button
def show_logout_button():
    if st.session_state.get('authenticated', False):
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("🚪 Logout", type="secondary", key="logout_winners"):
                from utils.auth import logout
                logout()

show_logout_button()

st.title("🏅 Contest Winners")
st.subheader("Hall of Fame - VPL Fantasy League Champions")

# Get all contests
contests_df = get_contests()

if not contests_df.empty:
    # Filter completed contests
    completed_contests = contests_df[contests_df['status'] == 'completed']
    
    if not completed_contests.empty:
        st.markdown("### 🏆 Completed Contests")
        
        # Display completed contests with winners
        for idx, contest in completed_contests.iterrows():
            match_info = next((f for f in FIXTURES_DATA if f['match_id'] == contest['match_id']), None)
            
            if match_info:
                st.markdown(f"#### {contest['name']}")
                st.write(f"**Match:** {match_info['teams'][0]} vs {match_info['teams'][1]}")
                st.write(f"**Prize Pool:** ₹{contest['prize_pool']}")
                
                # Get leaderboard for this contest
                leaderboard = get_leaderboard(contest['contest_id'])
                
                if not leaderboard.empty:
                    # Display top 3 winners
                    st.markdown("##### 🥇 Top 3 Winners:")
                    
                    top3 = leaderboard.head(3)
                    
                    for i, (_, winner) in enumerate(top3.iterrows()):
                        if i == 0:
                            st.success(f"🥇 **1st Place:** {winner['username']} - Team: {winner['team_name']} - Points: {winner['total_points']}")
                        elif i == 1:
                            st.info(f"🥈 **2nd Place:** {winner['username']} - Team: {winner['team_name']} - Points: {winner['total_points']}")
                        elif i == 2:
                            st.warning(f"🥉 **3rd Place:** {winner['username']} - Team: {winner['team_name']} - Points: {winner['total_points']}")
                    
                    # Show full leaderboard in expander
                    with st.expander("View Full Leaderboard"):
                        # Create display dataframe
                        display_df = leaderboard[['rank', 'username', 'team_name', 'total_points']].copy()
                        display_df.columns = ['Rank', 'Username', 'Team Name', 'Total Points']
                        
                        # Add medals for top 3
                        display_df.loc[display_df['Rank'] == 1, 'Rank'] = "🥇 1st"
                        display_df.loc[display_df['Rank'] == 2, 'Rank'] = "🥈 2nd"
                        display_df.loc[display_df['Rank'] == 3, 'Rank'] = "🥉 3rd"
                        
                        st.dataframe(display_df, use_container_width=True, hide_index=True)
                        
                        # Prize distribution
                        st.markdown("##### 💰 Prize Distribution:")
                        total_prize = contest['prize_pool']
                        
                        if len(leaderboard) >= 3:
                            first_prize = total_prize * 0.5
                            second_prize = total_prize * 0.3
                            third_prize = total_prize * 0.2
                            
                            st.write(f"🥇 **1st Place:** ₹{first_prize:.0f}")
                            st.write(f"🥈 **2nd Place:** ₹{second_prize:.0f}")
                            st.write(f"🥉 **3rd Place:** ₹{third_prize:.0f}")
                        elif len(leaderboard) == 2:
                            first_prize = total_prize * 0.7
                            second_prize = total_prize * 0.3
                            
                            st.write(f"🥇 **1st Place:** ₹{first_prize:.0f}")
                            st.write(f"🥈 **2nd Place:** ₹{second_prize:.0f}")
                        elif len(leaderboard) == 1:
                            st.write(f"🥇 **Winner takes all:** ₹{total_prize:.0f}")
                else:
                    st.info("No participants in this contest")
                
                st.markdown("---")
    
    # Show live contests
    live_contests = contests_df[contests_df['status'] == 'live']
    
    if not live_contests.empty:
        st.markdown("### 🔴 Live Contests")
        
        for idx, contest in live_contests.iterrows():
            match_info = next((f for f in FIXTURES_DATA if f['match_id'] == contest['match_id']), None)
            
            if match_info:
                st.markdown(f"#### {contest['name']} - LIVE")
                st.write(f"**Match:** {match_info['teams'][0]} vs {match_info['teams'][1]}")
                
                # Get current standings
                leaderboard = get_leaderboard(contest['contest_id'])
                
                if not leaderboard.empty:
                    st.markdown("##### 📊 Current Standings:")
                    
                    # Show top 5 current leaders
                    top5 = leaderboard.head(5)
                    
                    for i, (_, leader) in enumerate(top5.iterrows()):
                        if i == 0:
                            st.success(f"🔥 **Leading:** {leader['username']} - {leader['team_name']} - {leader['total_points']} pts")
                        else:
                            st.write(f"**{i+1}.** {leader['username']} - {leader['team_name']} - {leader['total_points']} pts")
                    
                    with st.expander("View Full Live Standings"):
                        display_df = leaderboard[['rank', 'username', 'team_name', 'total_points']].copy()
                        display_df.columns = ['Rank', 'Username', 'Team Name', 'Total Points']
                        st.dataframe(display_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No participants in this contest")
                
                st.markdown("---")
    
    # Show upcoming contests
    upcoming_contests = contests_df[contests_df['status'] == 'active']
    
    if not upcoming_contests.empty:
        st.markdown("### 📅 Upcoming Contests")
        
        for idx, contest in upcoming_contests.iterrows():
            match_info = next((f for f in FIXTURES_DATA if f['match_id'] == contest['match_id']), None)
            
            if match_info:
                st.markdown(f"#### {contest['name']}")
                st.write(f"**Match:** {match_info['teams'][0]} vs {match_info['teams'][1]}")
                st.write(f"**Entry Fee:** ₹{contest['entry_fee']} | **Prize Pool:** ₹{contest['prize_pool']}")
                
                # Get current participants
                leaderboard = get_leaderboard(contest['contest_id'])
                
                if not leaderboard.empty:
                    st.write(f"**Participants:** {len(leaderboard)}/{contest['max_participants']}")
                    
                    with st.expander("View Participants"):
                        display_df = leaderboard[['username', 'team_name']].copy()
                        display_df.columns = ['Username', 'Team Name']
                        display_df.index = range(1, len(display_df) + 1)
                        st.dataframe(display_df, use_container_width=True)
                else:
                    st.write("**Participants:** 0")
                    st.info("No participants yet - join now!")
                
                st.markdown("---")
    
    # Overall statistics
    st.markdown("### 📈 Overall Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_contests = len(contests_df)
        st.metric("Total Contests", total_contests)
    
    with col2:
        completed_count = len(completed_contests)
        st.metric("Completed", completed_count)
    
    with col3:
        live_count = len(live_contests)
        st.metric("Live", live_count)
    
    with col4:
        total_prizes = contests_df['prize_pool'].sum()
        st.metric("Total Prizes", f"₹{total_prizes:,}")
    
    # Hall of Fame - Most wins
    if not completed_contests.empty:
        st.markdown("### 🏛️ Hall of Fame")
        
        # Get all winners from completed contests
        all_winners = []
        for _, contest in completed_contests.iterrows():
            leaderboard = get_leaderboard(contest['contest_id'])
            if not leaderboard.empty:
                winner = leaderboard.iloc[0]
                all_winners.append({
                    'username': winner['username'],
                    'contest_name': contest['name'],
                    'points': winner['total_points']
                })
        
        if all_winners:
            winners_df = pd.DataFrame(all_winners)
            
            # Count wins per user
            win_counts = winners_df['username'].value_counts()
            
            st.markdown("#### 🏆 Most Contest Wins:")
            for i, (username, wins) in enumerate(win_counts.head(5).items()):
                if i == 0:
                    st.success(f"🏆 **Champion:** {username} - {wins} win(s)")
                else:
                    st.write(f"**{i+1}.** {username} - {wins} win(s)")
            
            # Highest single contest score
            if all_winners:
                highest_score = max(all_winners, key=lambda x: x['points'])
                st.markdown("#### 🎯 Highest Single Contest Score:")
                st.info(f"**{highest_score['username']}** - {highest_score['points']} points in {highest_score['contest_name']}")

else:
    st.info("No contests available yet")
    st.markdown("### 🎯 How Contest Winners Are Determined")
    st.markdown("""
    1. **Points Calculation**: Based on player performance in matches
    2. **Captain Bonus**: Captain gets 2x points
    3. **Vice-Captain Bonus**: Vice-captain gets 1.5x points
    4. **Final Ranking**: Teams ranked by total points after match completion
    5. **Prize Distribution**: 
       - 1st Place: 50% of prize pool
       - 2nd Place: 30% of prize pool
       - 3rd Place: 20% of prize pool
    """)

# Navigation buttons
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏆 Join Contest", use_container_width=True):
        st.switch_page("pages/4_🏆_Contests.py")

with col2:
    if st.button("📊 View Results", use_container_width=True):
        st.switch_page("pages/6_📊_Results.py")

with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")