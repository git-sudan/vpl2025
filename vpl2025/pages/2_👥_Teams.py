# Fixed Teams Page - Remove Roles & Add Persistent Logout
import streamlit as st
import pandas as pd
from utils.auth import check_authentication
from utils.constants import TEAMS_DATA

st.set_page_config(page_title="Teams", page_icon="👥", layout="wide")

# Persistent logout button
def show_logout_button():
    if st.session_state.get('authenticated', False):
        col1, col2 = st.columns([9, 1])
        with col2:
            if st.button("🚪 Logout", type="secondary", key="logout_teams"):
                from utils.auth import logout
                logout()

if not check_authentication():
    st.stop()

# Show logout button
show_logout_button()

st.title("👥 Teams & Players")

# Team selection
selected_team = st.selectbox("Select Team", list(TEAMS_DATA.keys()))

if selected_team:
    team_data = TEAMS_DATA[selected_team]
    
    # Team overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Players", len(team_data['players']))
    
    with col2:
        st.metric("Budget Used", f"₹{team_data['amount_spent']:,}")
    
    with col3:
        st.metric("Balance", f"₹{team_data['balance_remaining']:,}")
    
    # Players table - Start indexing from 1
    st.markdown("### 👥 Squad")
    
    players_data = []
    for i, player in enumerate(team_data['players'], 1):
        players_data.append({
            'S.No': i,
            'Player Name': player['name'],
            'Price': f"₹{player['price']:,}",
            'Fantasy Points': 0  # Would be calculated from performances
        })
    
    df_players = pd.DataFrame(players_data)
    st.dataframe(df_players, use_container_width=True, hide_index=True)
    
    # Player price distribution
    st.markdown("### 💰 Price Distribution")
    
    prices = [player['price'] for player in team_data['players']]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🏆 Most Expensive", f"₹{max(prices):,}")
    
    with col2:
        st.metric("💵 Cheapest", f"₹{min(prices):,}")
    
    with col3:
        st.metric("📊 Average Price", f"₹{sum(prices)//len(prices):,}")
    
    with col4:
        st.metric("🔢 Total Value", f"₹{sum(prices):,}")
    
    # Top players by price
    st.markdown("### 🌟 Top Players by Price")
    
    sorted_players = sorted(team_data['players'], key=lambda x: x['price'], reverse=True)
    
    for i, player in enumerate(sorted_players[:5], 1):
        st.write(f"{i}. **{player['name']}** - ₹{player['price']:,}")

# All teams overview
st.markdown("### 🏆 All Teams Overview")

all_teams_data = []
for i, (team_name, team_info) in enumerate(TEAMS_DATA.items(), 1):
    most_expensive = max(team_info['players'], key=lambda x: x['price'])
    cheapest = min(team_info['players'], key=lambda x: x['price'])
    
    all_teams_data.append({
        'S.No': i,
        'Team': team_name,
        'Players': len(team_info['players']),
        'Budget Used': f"₹{team_info['amount_spent']:,}",
        'Balance': f"₹{team_info['balance_remaining']:,}",
        'Most Expensive': f"{most_expensive['name']} (₹{most_expensive['price']:,})",
        'Cheapest': f"{cheapest['name']} (₹{cheapest['price']:,})"
    })

df_all_teams = pd.DataFrame(all_teams_data)
st.dataframe(df_all_teams, use_container_width=True, hide_index=True)

# Player search functionality
st.markdown("### 🔍 Player Search")

search_term = st.text_input("Search for a player", placeholder="Enter player name...")

if search_term:
    found_players = []
    for team_name, team_data in TEAMS_DATA.items():
        for player in team_data['players']:
            if search_term.lower() in player['name'].lower():
                found_players.append({
                    'Player Name': player['name'],
                    'Team': team_name,
                    'Price': f"₹{player['price']:,}"
                })
    
    if found_players:
        st.markdown("### 🎯 Search Results")
        search_df = pd.DataFrame(found_players)
        # Add index starting from 1
        search_df.index = range(1, len(search_df) + 1)
        st.dataframe(search_df, use_container_width=True)
    else:
        st.info("No players found matching your search")

# All players sorted by price
st.markdown("### 💎 All Players by Price")

all_players = []
for team_name, team_data in TEAMS_DATA.items():
    for player in team_data['players']:
        all_players.append({
            'Player Name': player['name'],
            'Team': team_name,
            'Price': player['price'],
            'Price Display': f"₹{player['price']:,}"
        })

# Sort by price descending
all_players.sort(key=lambda x: x['Price'], reverse=True)

# Create DataFrame with proper indexing
all_players_data = []
for i, player in enumerate(all_players, 1):
    all_players_data.append({
        'Rank': i,
        'Player Name': player['Player Name'],
        'Team': player['Team'],
        'Price': player['Price Display']
    })

df_all_players = pd.DataFrame(all_players_data)
st.dataframe(df_all_players, use_container_width=True, hide_index=True)

# Statistics
st.markdown("### 📊 Tournament Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_players = sum(len(team_data['players']) for team_data in TEAMS_DATA.values())
    st.metric("Total Players", total_players)

with col2:
    all_prices = [player['price'] for team_data in TEAMS_DATA.values() for player in team_data['players']]
    st.metric("Highest Price", f"₹{max(all_prices):,}")

with col3:
    st.metric("Lowest Price", f"₹{min(all_prices):,}")

with col4:
    st.metric("Average Price", f"₹{sum(all_prices)//len(all_prices):,}")

# Footer
st.markdown("---")
st.markdown("""
### 📋 Player Information:
- **All players can bat and bowl** - No role restrictions
- **Price range**: ₹300 to ₹1,380
- **Total players**: 80 players across 10 teams
- **Budget per team**: ₹4,500 for 7 players
""")