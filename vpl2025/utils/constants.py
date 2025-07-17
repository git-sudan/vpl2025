# Teams and Players Data - NO ROLES (all players can bat and bowl)
TEAMS_DATA = {
    "SKE Comrades": {
        "players": [
            {"name": "Rajadurai", "price": 1000},
            {"name": "Sham", "price": 930},
            {"name": "Surya SS", "price": 820},
            {"name": "Vicky Jr", "price": 430},
            {"name": "Elumalai", "price": 350},
            {"name": "Vignesh Raj M", "price": 350},
            {"name": "Imthiyas", "price": 310},
            {"name": "Suresh", "price": 300}
        ],
        "amount_spent": 4490,
        "balance_remaining": 10
    },
    "Wolf Pack": {
        "players": [
            {"name": "Manimaran", "price": 1000},
            {"name": "Stephen", "price": 600},
            {"name": "Gopal SKE", "price": 600},
            {"name": "Mugilan", "price": 740},
            {"name": "Abbu", "price": 430},
            {"name": "Presshan", "price": 420},
            {"name": "Ranjith Pandiyan", "price": 400},
            {"name": "Harris", "price": 310}
        ],
        "amount_spent": 4500,
        "balance_remaining": 0
    },
    "BMW Boys": {
        "players": [
            {"name": "Govardhan", "price": 1380},
            {"name": "Mad", "price": 420},
            {"name": "M.Vicky", "price": 400},
            {"name": "Vicky Rockers", "price": 580},
            {"name": "Sheik", "price": 680},
            {"name": "Anandh", "price": 410},
            {"name": "Vasanth", "price": 300},
            {"name": "Kumar", "price": 330}
        ],
        "amount_spent": 4500,
        "balance_remaining": 0
    },
    "Red Dragon": {
        "players": [
            {"name": "Vicky Stylist", "price": 920},
            {"name": "Rath", "price": 1320},
            {"name": "Bharani", "price": 540},
            {"name": "Agastin", "price": 350},
            {"name": "Gani", "price": 450},
            {"name": "Imran", "price": 300},
            {"name": "Ajees", "price": 300},
            {"name": "Vicky 7 Sigma", "price": 300}
        ],
        "amount_spent": 4490,
        "balance_remaining": 10
    },
    "SG": {
        "players": [
            {"name": "V Rajkumar", "price": 700},
            {"name": "Akau", "price": 500},
            {"name": "Gokul", "price": 1020},
            {"name": "Dinc", "price": 540},
            {"name": "Riyaz", "price": 430},
            {"name": "Ajith", "price": 420},
            {"name": "Jaz", "price": 300},
            {"name": "Jerry", "price": 400}
        ],
        "amount_spent": 4310,
        "balance_remaining": 190
    },
    "Wall Street Warriors": {
        "players": [
            {"name": "Jeevakan", "price": 700},
            {"name": "Ilaya", "price": 990},
            {"name": "Hari", "price": 960},
            {"name": "Vicky S Captain CC", "price": 460},
            {"name": "Tamizh SKE", "price": 350},
            {"name": "Raja Muniyappan", "price": 440},
            {"name": "Mohamed Ashik", "price": 300},
            {"name": "Vivek", "price": 300}
        ],
        "amount_spent": 4500,
        "balance_remaining": 0
    },
    "Friendz Titans": {
        "players": [
            {"name": "Sri", "price": 1000},
            {"name": "Sathiya", "price": 930},
            {"name": "Halith", "price": 720},
            {"name": "Suriya VKS", "price": 400},
            {"name": "Akash Randy", "price": 450},
            {"name": "Dhavuth", "price": 310},
            {"name": "Mappi", "price": 350},
            {"name": "Gopal", "price": 320}
        ],
        "amount_spent": 4480,
        "balance_remaining": 20
    },
    "Mufasa": {
        "players": [
            {"name": "Gopi", "price": 600},
            {"name": "Kamalesh", "price": 1050},
            {"name": "Mathi", "price": 760},
            {"name": "Saint Saravanan", "price": 500},
            {"name": "Thamizh Captain CC", "price": 620},
            {"name": "RDR Naveen", "price": 300},
            {"name": "Shan", "price": 300},
            {"name": "Suriya J", "price": 360}
        ],
        "amount_spent": 4490,
        "balance_remaining": 10
    },
    "Phoenix Strikers": {
        "players": [
            {"name": "Tamizhan", "price": 600},
            {"name": "Kirthick", "price": 1050},
            {"name": "Fazil", "price": 1020},
            {"name": "Pravin", "price": 560},
            {"name": "Rajadurai Rai", "price": 350},
            {"name": "Gautam", "price": 300},
            {"name": "Lakshmi", "price": 300},
            {"name": "Prasanna", "price": 320}
        ],
        "amount_spent": 4500,
        "balance_remaining": 0
    },
    "Clutch Knights": {
        "players": [
            {"name": "Alfar", "price": 700},
            {"name": "Azar", "price": 960},
            {"name": "Prasanth rio", "price": 950},
            {"name": "Chintu", "price": 350},
            {"name": "Bastin", "price": 410},
            {"name": "Karthikeyan R", "price": 410},
            {"name": "Rasool", "price": 320},
            {"name": "GopiR", "price": 360}
        ],
        "amount_spent": 4460,
        "balance_remaining": 40
    }
}

# Fixtures Data (mutable for admin control)
FIXTURES_DATA = [
    # Saturday Fixtures
    {"match_id": "M001", "match_no": 1, "teams": ["Clutch Knights", "Friendz Titans"], "time": "6:00 AM", "day": "Saturday", "status": "upcoming"},
    {"match_id": "M002", "match_no": 2, "teams": ["SKE Comrades", "SG"], "time": "6:25 AM", "day": "Saturday", "status": "upcoming"},
    # ... (rest of fixtures)
]

# Budget and team constraints
TEAM_BUDGET = 4500
TEAM_SIZE = 7  # 7 players per team
CAPTAIN_MULTIPLIER = 2.0
VICE_CAPTAIN_MULTIPLIER = 1.5
