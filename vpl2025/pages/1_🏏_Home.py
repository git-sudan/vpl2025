import streamlit as st
import pandas as pd
from utils.auth import check_authentication
from utils.constants import TEAMS_DATA, FIXTURES_DATA

st.set_page_config(page_title="Home", page_icon="🏏", layout="wide")

if not check_authentication():
    st.stop()

st.title("🏏 VPL Fantasy League - Home")

# User greeting
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(f"### Welcome back, **{st.session_state.username}**!")
with col2:
    if st.button("🚪 Logout"):
        from utils.auth import logout
        logout()

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

# Recent activity
st.markdown("### 🔄 Recent Activity")
st.info("🎯 New user registered: Welcome to VPL Fantasy League!")
st.info("🏆 Contest created for today's match")
st.info("⚡ Live scoring will begin soon")

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
    if st.button("📅 Check Fixtures", use_container_width=True):
        st.switch_page("pages/3_📅_Fixtures.py")
