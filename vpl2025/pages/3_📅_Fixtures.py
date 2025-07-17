# Fixed Fixtures Page - Add Persistent Logout & Fix Indexing
import streamlit as st
import pandas as pd
from utils.auth import check_authentication
from utils.constants import FIXTURES_DATA

st.set_page_config(page_title="Fixtures", page_icon="📅", layout="wide")

# Persistent logout button
def show_logout_button():
    if st.session_state.get('authenticated', False):
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("🚪 Logout", type="secondary", key="logout_fixtures"):
                from utils.auth import logout
                logout()

if not check_authentication():
    st.stop()

# Show logout button
show_logout_button()

st.title("📅 Match Fixtures")

# Filter options
col1, col2 = st.columns(2)

with col1:
    day_filter = st.selectbox("Filter by Day", ["All", "Saturday", "Sunday"])

with col2:
    status_filter = st.selectbox("Filter by Status", ["All", "upcoming", "live", "completed"])

# Apply filters
filtered_fixtures = FIXTURES_DATA.copy()

if day_filter != "All":
    filtered_fixtures = [f for f in filtered_fixtures if f['day'] == day_filter]

if status_filter != "All":
    filtered_fixtures = [f for f in filtered_fixtures if f['status'] == status_filter]

# Display fixtures
st.markdown("### 🏏 Match Schedule")

# Group by day
saturday_matches = [f for f in filtered_fixtures if f['day'] == 'Saturday']
sunday_matches = [f for f in filtered_fixtures if f['day'] == 'Sunday']

if saturday_matches:
    st.markdown("#### 📅 Saturday Matches")
    
    # Create DataFrame for Saturday matches with proper indexing
    saturday_data = []
    for i, match in enumerate(saturday_matches, 1):
        saturday_data.append({
            'S.No': i,
            'Match No': match['match_no'],
            'Teams': f"{match['teams'][0]} vs {match['teams'][1]}",
            'Time': match['time'],
            'Status': match['status'].title()
        })
    
    if saturday_data:
        df_saturday = pd.DataFrame(saturday_data)
        st.dataframe(df_saturday, use_container_width=True, hide_index=True)
    
    # Expandable details for each match
    st.markdown("#### 📋 Match Details")
    for i, match in enumerate(saturday_matches, 1):
        with st.expander(f"🏏 Match {i}: {match['teams'][0]} vs {match['teams'][1]} - {match['time']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Match Number:** {match['match_no']}")
                st.write(f"**Teams:** {match['teams'][0]} vs {match['teams'][1]}")
                st.write(f"**Time:** {match['time']}")
            
            with col2:
                st.write(f"**Day:** {match['day']}")
                st.write(f"**Status:** {match['status'].title()}")
                st.write(f"**Match ID:** {match['match_id']}")
            
            with col3:
                if match['status'] == 'upcoming':
                    if st.button(f"Create Contest", key=f"contest_{match['match_id']}"):
                        st.switch_page("pages/4_🏆_Contests.py")
                elif match['status'] == 'live':
                    if st.button(f"Live Scoring", key=f"live_{match['match_id']}"):
                        st.switch_page("pages/5_⚡_Live.py")
                elif match['status'] == 'completed':
                    if st.button(f"View Results", key=f"results_{match['match_id']}"):
                        st.switch_page("pages/6_📊_Results.py")

if sunday_matches:
    st.markdown("#### 📅 Sunday Matches")
    
    # Create DataFrame for Sunday matches with proper indexing
    sunday_data = []
    for i, match in enumerate(sunday_matches, 1):
        sunday_data.append({
            'S.No': i,
            'Match No': match['match_no'],
            'Teams': f"{match['teams'][0]} vs {match['teams'][1]}",
            'Time': match['time'],
            'Status': match['status'].title()
        })
    
    if sunday_data:
        df_sunday = pd.DataFrame(sunday_data)
        st.dataframe(df_sunday, use_container_width=True, hide_index=True)
    
    # Expandable details for each match
    st.markdown("#### 📋 Match Details")
    for i, match in enumerate(sunday_matches, 1):
        with st.expander(f"🏏 Match {i}: {match['teams'][0]} vs {match['teams'][1]} - {match['time']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Match Number:** {match['match_no']}")
                st.write(f"**Teams:** {match['teams'][0]} vs {match['teams'][1]}")
                st.write(f"**Time:** {match['time']}")
            
            with col2:
                st.write(f"**Day:** {match['day']}")
                st.write(f"**Status:** {match['status'].title()}")
                st.write(f"**Match ID:** {match['match_id']}")
            
            with col3:
                if match['status'] == 'upcoming':
                    if st.button(f"Create Contest", key=f"contest_{match['match_id']}"):
                        st.switch_page("pages/4_🏆_Contests.py")
                elif match['status'] == 'live':
                    if st.button(f"Live Scoring", key=f"live_{match['match_id']}"):
                        st.switch_page("pages/5_⚡_Live.py")
                elif match['status'] == 'completed':
                    if st.button(f"View Results", key=f"results_{match['match_id']}"):
                        st.switch_page("pages/6_📊_Results.py")

# Show message if no matches found
if not saturday_matches and not sunday_matches:
    st.info("No matches found for the selected filters")

# Match statistics
st.markdown("### 📊 Tournament Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Matches", len(FIXTURES_DATA))

with col2:
    upcoming_count = len([f for f in FIXTURES_DATA if f['status'] == 'upcoming'])
    st.metric("Upcoming", upcoming_count)

with col3:
    live_count = len([f for f in FIXTURES_DATA if f['status'] == 'live'])
    st.metric("Live", live_count)

with col4:
    completed_count = len([f for f in FIXTURES_DATA if f['status'] == 'completed'])
    st.metric("Completed", completed_count)

# Time slots analysis
st.markdown("### ⏰ Time Slots Distribution")

time_slots = {}
for match in FIXTURES_DATA:
    time_slot = match['time']
    time_slots[time_slot] = time_slots.get(time_slot, 0) + 1

# Create DataFrame for time slots
time_data = []
for i, (time, count) in enumerate(sorted(time_slots.items()), 1):
    time_data.append({
        'S.No': i,
        'Time Slot': time,
        'Number of Matches': count
    })

if time_data:
    df_time = pd.DataFrame(time_data)
    st.dataframe(df_time, use_container_width=True, hide_index=True)

# Day-wise distribution
st.markdown("### 📅 Day-wise Distribution")

day_stats = {}
for match in FIXTURES_DATA:
    day = match['day']
    day_stats[day] = day_stats.get(day, 0) + 1

col1, col2 = st.columns(2)

with col1:
    st.metric("Saturday Matches", day_stats.get('Saturday', 0))

with col2:
    st.metric("Sunday Matches", day_stats.get('Sunday', 0))

# Quick navigation
st.markdown("### 🎮 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏆 Create Contest", use_container_width=True):
        st.switch_page("pages/4_🏆_Contests.py")

with col2:
    if st.button("⚡ Live Scoring", use_container_width=True):
        st.switch_page("pages/5_⚡_Live.py")

with col3:
    if st.button("📊 View Results", use_container_width=True):
        st.switch_page("pages/6_📊_Results.py")

# Footer
st.markdown("---")
st.markdown("""
### 📋 Tournament Information:
- **Total Matches**: 49 matches across 2 days
- **Format**: T20 Cricket Tournament
- **Teams**: 10 teams participating
- **Schedule**: Saturday & Sunday matches
- **Playoff Format**: Position-based eliminations
""")