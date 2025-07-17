import streamlit as st
import pandas as pd
from utils.auth import initialize_auth, check_authentication
from utils.data_manager import initialize_data_files
from utils.constants import TEAMS_DATA, FIXTURES_DATA

# Page configuration
st.set_page_config(
    page_title="VPL Fantasy League",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication FIRST
initialize_auth()

# Initialize data files
initialize_data_files()

# Persistent logout button function
def show_logout_button():
    if st.session_state.get('authenticated', False):
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("🚪 Logout", type="secondary", key="logout_home"):
                from utils.auth import logout
                logout()

# Main app logic
def main():
    # Check authentication
    if not check_authentication():
        st.stop()
    
    # Show logout button
    show_logout_button()
    
    # Main header
    st.title("🏏 VPL Fantasy League")
    st.subheader("TURF 32 Premier League Season 3")
    
    # Welcome message
    st.markdown(f"### Welcome back, **{st.session_state.username}**!")
    
    # Quick stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Teams", len(TEAMS_DATA))
    
    with col2:
        st.metric("🏆 Total Matches", len(FIXTURES_DATA))
    
    with col3:
        st.metric("👥 Team Size", "7 Players")
    
    with col4:
        st.metric("💰 Budget", "₹4,500")
    
    # Today's matches
    st.markdown("### 📅 Today's Matches")
    today_matches = [f for f in FIXTURES_DATA if f['status'] == 'upcoming'][:5]
    
    if today_matches:
        for match in today_matches:
            with st.expander(f"🏏 Match {match['match_no']}: {match['teams'][0]} vs {match['teams'][1]} - {match['time']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Time:** {match['time']}")
                    st.write(f"**Day:** {match['day']}")
                with col2:
                    st.write(f"**Status:** {match['status'].title()}")
                    if st.button(f"Create Contest", key=f"contest_{match['match_id']}"):
                        st.switch_page("pages/4_🏆_Contests.py")
    else:
        st.info("No matches scheduled for today")
    
    # Quick navigation
    st.markdown("### 🎮 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏆 Join Contest", use_container_width=True):
            st.switch_page("pages/4_🏆_Contests.py")
    
    with col2:
        if st.button("📊 View Results", use_container_width=True):
            st.switch_page("pages/6_📊_Results.py")
    
    with col3:
        if st.button("🏅 View Winners", use_container_width=True):
            st.switch_page("pages/8_🏅_Winners.py")
    
    # Footer
    st.markdown("---")
    st.markdown("### 🎯 How to Play")
    st.markdown("""
    1. **Create Team**: Select 7 players within budget (all players can bat and bowl)
    2. **Choose Leaders**: Pick 1 captain (2x points) and 1 vice-captain (1.5x points)
    3. **Join Contest**: Enter contests and compete
    4. **Track Performance**: Monitor live scores and points
    5. **Win Prizes**: Top performers get rewards
    """)

if __name__ == "__main__":
    main()