import streamlit as st
import json, os, random, calendar
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

DATA_FILE = "data.json"

def get_secret(key, default):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default

LOGIN_USER = get_secret("LOGIN_USER", "hari")
LOGIN_PASS = get_secret("LOGIN_PASS", "9442176514")
RESET_PASS = get_secret("RESET_PASS", "h1a2r3i4s5h6")

def clamp(v, lo=0, hi=100):
    try:
        return max(lo, min(hi, int(v)))
    except Exception:
        return lo

def safe_progress(v):
    return max(0.0, min(float(v), 1.0))

def money_fmt(n):
    try:
        return f"₹{int(n)}"
    except Exception:
        return "₹0"

def compute_streak(history):
    streak = 0
    d = date.today()
    while str(d) in history:
        streak += 1
        d -= timedelta(days=1)
    return streak

def compute_days_since(start_str):
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d").date()
    except Exception:
        start = date.today()
    return (date.today() - start).days

def default_data():
    return {
        "points": 0,
        "xp": 0,
        "coins": 0,
        "gems": 0,
        "health": 70,
        "energy": 70,
        "focus": 70,
        "happiness": 70,
        "streak": 0,
        "best_streak": 0,
        "last": "",
        "avatar": "😎",
        "name": "Player",
        "title": "Newbie",
        "dream": "",
        "dream_steps": [],
        "career": "Student",
        "history": {},
        "day_logs": {},
        "badges": [],
        "achievements": [],
        "reasons": {},
        "start_date": str(date.today()),
        "final_submitted": {},
        "locked_days": [],
        "custom_tasks": [],
        "custom_task_xp": {},
        "theme": "Dark",
        "quote_mode": True,
        "strict_mode": True,
        "mobile_nav": False,
        "moods": {},
        "weekly_goals": {},
        "shop_owned": [],
        "equipped": {
            "avatar": "😎",
            "theme": "Dark",
            "title": "Newbie",
            "icon": "⭐",
            "effect": "Glow",
            "weapon": "Wooden Stick",
            "pet": "None",
            "wing": "None",
            "aura": "None",
            "clothes": "Casual"
        },
        "base_tier": 1,
        "base_name": "Small Room",
        "rewards_claimed": {
            "daily": "",
            "weekly": "",
            "monthly": "",
            "mystery": "",
            "spin": ""
        },
        "daily_generated": {},
        "control_tracker": {
            "MA001": {"fail_count": 0, "best_clean": 0, "current_clean": 0, "last_fail": ""},
            "PN002": {"fail_count": 0, "best_clean": 0, "current_clean": 0, "last_fail": ""}
        },
        "water_logs": {},
        "money": {
            "balance": 0,
            "income": [],
            "expense": []
        },
        "punishments": {},
        "punishment_done": {},
        "life_goals": {
            "relationships": "",
            "family": "",
            "health": "",
            "finance": "",
            "learning": ""
        },
        "life_wheel": {
            "Health": 50,
            "Finance": 50,
            "Learning": 50,
            "Relationships": 50,
            "Peace": 50
        },
        "mini_games_stats": {
            "memory_best": 0,
            "quiz_best": 0,
            "typing_best_wpm": 0
        },
        "boss_history": {},
        "flatline_days": 0,
        "recovery_days": 0,
        "selected_daily_goal": ""
    }

def load():
    base = default_data()
    if not os.path.exists(DATA_FILE):
        return base
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        return base
    for k, v in base.items():
        if k not in data:
            data[k] = v
    for k in ["points", "xp", "coins", "gems", "health", "energy", "focus", "happiness", "streak", "best_streak", "base_tier", "flatline_days", "recovery_days"]:
        data[k] = int(data.get(k, 0 if k not in ["health", "energy", "focus", "happiness"] else 70))
    return data

def save(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

def get_theme_css(theme):
    if theme == "Light":
        bg = "#f8fafc"
        text = "#0f172a"
        card = "rgba(0,0,0,0.06)"
    elif theme == "Purple":
        bg = "linear-gradient(135deg,#2e1065,#4c1d95)"
        text = "white"
        card = "rgba(255,255,255,0.10)"
    elif theme == "Green":
        bg = "linear-gradient(135deg,#052e16,#14532d)"
        text = "white"
        card = "rgba(255,255,255,0.10)"
    else:
        bg = "linear-gradient(135deg,#0f172a,#1e293b)"
        text = "white"
        card = "rgba(255,255,255,0.08)"
    return f"""
    <style>
    body {{background:{bg};color:{text};}}
    .card {{
        background:{card};
        padding:20px;
        border-radius:20px;
        backdrop-filter:blur(12px);
        margin-bottom:15px;
        animation:fade 0.6s;
    }}
    @keyframes fade {{
        from{{opacity:0;transform:translateY(20px);}}
        to{{opacity:1;}}
    }}
    @keyframes float {{
        0%{{transform:translateY(0)}}
        50%{{transform:translateY(-12px)}}
        100%{{transform:translateY(0)}}
    }}
    .stButton button {{
        background:linear-gradient(45deg,#6366f1,#8b5cf6);
        color:white;
        border-radius:10px;
        transition:0.3s;
    }}
    .stButton button:hover {{transform:scale(1.05);}}
    @media(max-width:768px){{
        .block-container{{padding:1rem;}}
        h1{{font-size:28px!important;}}
        h2{{font-size:22px!important;}}
        h3{{font-size:18px!important;}}
        .card{{padding:14px!important;border-radius:14px!important;}}
    }}
    </style>
    """

def motivation(score, strict=True):
    if score >= 90:
        return "🔥 Beast mode! Today you controlled your day."
    if score >= 70:
        return "💪 Good work. Small improvements daily create big change."
    if score >= 40:
        return "⚠️ Average day. Don’t quit, fix tomorrow."
    return "🚨 Reset your focus. One bad day is not the end." if not strict else "🚨 Strict mode: stop wasting time and come back stronger."

def generate_daily_content(today_str):
    rng = random.Random(today_str)
    side_pool = [
        "Read 20 Pages 📖",
        "Walk 20 Minutes 🚶",
        "Write Self Review ✍️",
        "Practice English 15 Min 🇬🇧",
        "Do 30 Push-ups 💪",
        "Deep Breathing 10 Min 🌬️",
        "Clean Room 🧹",
        "No Junk Food 🌮"
    ]
    secret_pool = [
        "No Social Media Today 🚫",
        "Wake 30 Min Early ⏰",
        "Meditation 15 Min 🧘",
        "Extra Study 1hr 🔥",
        "Journal 10 Lines 📒"
    ]
    challenge_pool = [
        "No Mobile for 1 Hour 📵",
        "100 Water Sips 💧",
        "5-Minute Plank Challenge 🏋️",
        "Cold Shower 🚿",
        "One Page Reading Sprint 📚"
    ]
    boss_pool = ["Lazy Monster 😴", "Porn Demon 👿", "Social Media Monster 📱", "Junk Food King 🍔", "Fear Dragon 🐉"]
    return {
        "side": rng.choice(side_pool),
        "secret": rng.choice(secret_pool),
        "challenge": rng.choice(challenge_pool),
        "boss": rng.choice(boss_pool)
    }

def ensure_daily_generated(data, today_str):
    data.setdefault("daily_generated", {})
    if today_str not in data["daily_generated"]:
        data["daily_generated"][today_str] = generate_daily_content(today_str)
        save(data)
    return data["daily_generated"][today_str]

def badge_rules():
    return {
        10: ("🪵", "Marakattai", 50),
        20: ("🥈", "Silver", 100),
        30: ("🥈", "Silver II", 150),
        40: ("💎", "Platinum", 200),
        50: ("💎", "Platinum II", 250),
        60: ("🔷", "Diamond", 300),
        70: ("👑", "Master", 400),
        80: ("🧠", "Elite", 500),
        90: ("⚡", "Elite Master", 700),
        100: ("🔥", "GOD MODE", 1000)
    }

def check_badges(data, level):
    unlocked = []
    for lvl, (icon, name, reward) in badge_rules().items():
        if level >= lvl and name not in data["badges"]:
            data["badges"].append(name)
            data["xp"] += reward
            data["points"] += reward
            data["coins"] += reward // 2
            unlocked.append((icon, name, reward))
    return unlocked

def combo_multiplier(streak):
    if streak >= 30:
        return 5, "Mega Combo ×5"
    if streak >= 7:
        return 3, "Combo ×3"
    if streak >= 3:
        return 2, "Combo ×2"
    return 1, "Combo ×1"

def level_from_days(days_passed):
    return min(100, int((days_passed / 365) * 100))

def rank_from_level(level):
    if level >= 100:
        return "GOD MODE"
    if level >= 80:
        return "Legend"
    if level >= 60:
        return "Master"
    if level >= 40:
        return "Elite"
    if level >= 20:
        return "Warrior"
    return "Beginner"

def world_zone(level):
    zones = [
        ("Forest", 1),
        ("Village", 10),
        ("City", 20),
        ("Mountain", 35),
        ("Space", 50),
        ("Heaven", 75),
        ("GOD Realm", 100)
    ]
    unlocked = [name for name, req in zones if level >= req]
    locked = [name for name, req in zones if level < req]
    return unlocked, locked, zones

def get_week_key(dt):
    return f"{dt.isocalendar().year}-W{dt.isocalendar().week:02d}"

def get_month_key(dt):
    return f"{dt.year}-{dt.month:02d}"

def claim_reward(data, reward_type, amount):
    if reward_type == "daily":
        data["coins"] += amount
        data["xp"] += amount // 2
    elif reward_type == "weekly":
        data["coins"] += amount * 2
        data["gems"] += 1
    elif reward_type == "monthly":
        data["coins"] += amount * 4
        data["gems"] += 3
        data["xp"] += amount
    elif reward_type == "mystery":
        pack = random.choice(["coins", "xp", "gems"])
        if pack == "coins":
            data["coins"] += amount * 3
        elif pack == "xp":
            data["xp"] += amount * 3
        else:
            data["gems"] += 2
    elif reward_type == "spin":
        prize = random.choice(["coins", "xp", "gems", "health"])
        if prize == "coins":
            data["coins"] += amount * 2
        elif prize == "xp":
            data["xp"] += amount * 2
        elif prize == "gems":
            data["gems"] += 1
        else:
            data["health"] = clamp(data["health"] + 5)
    save(data)

def generate_punishments_for_day(data, tomorrow_str, bad_task):
    pool = {
        "MA001": [
            "Extra Study 1hr 🔥", "Write Self Review ✍️", "No Social Media Today 🚫",
            "100 Push-ups 💪", "30 Min Walking 🚶", "Read 20 Pages 📖",
            "Meditation 20 Min 🧘", "Drink 3L Water 💧", "Room Cleaning 🧹", "Wake Up 30 Min Early ⏰"
        ],
        "PN002": [
            "Extra Study 30min 📚", "Clean Room 🧹", "Write Self Review ✍️",
            "No YouTube Today 📵", "Practice English 30 Min 🇬🇧", "Deep Breathing 20 Min 🌬️",
            "Exercise 45 Min 🏋️", "Journal Writing 📒", "No Mobile 1 Hour 📱❌", "Cold Shower 🚿"
        ]
    }
    fail_count = data["control_tracker"][bad_task]["fail_count"]
    task_count = min(2 + (fail_count // 3), 5)
    task_count = min(task_count, len(pool[bad_task]))
    data.setdefault("punishments", {})
    data["punishments"].setdefault(tomorrow_str, [])
    selected = random.sample(pool[bad_task], k=task_count)
    for t in selected:
        if t not in data["punishments"][tomorrow_str]:
            data["punishments"][tomorrow_str].append(t)

def weekly_average(history):
    if not history:
        return 0.0
    today = date.today()
    vals = []
    for i in range(7):
        d = str(today - timedelta(days=i))
        vals.append(history.get(d, 0))
    return sum(vals) / 7.0

def monthly_average(history):
    if not history:
        return 0.0
    today = date.today()
    vals = []
    for i in range(30):
        d = str(today - timedelta(days=i))
        vals.append(history.get(d, 0))
    return sum(vals) / 30.0

data = load()
today = date.today()
today_str = str(today)
days_passed = compute_days_since(data["start_date"])
level = level_from_days(days_passed)
rank = rank_from_level(level)
data["streak"] = compute_streak(data.get("history", {}))
data["best_streak"] = max(int(data.get("best_streak", 0)), int(data["streak"]))
data["recovery_days"] = int(data.get("control_tracker", {}).get("MA001", {}).get("current_clean", 0))
save(data)

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pwd")
    if st.button("LOGIN", key="login_btn"):
        if user == LOGIN_USER and pwd == LOGIN_PASS:
            st.session_state.login = True
            st.success("Login Success ⛓️‍💥")
            st.rerun()
        else:
            st.error("Wrong credentials 🔗")
    st.stop()

if "captcha_q" not in st.session_state:
    a = random.randint(10, 50)
    b = random.randint(10, 50)
    op = random.choice(["+", "-", "*"])
    ans = a + b if op == "+" else a - b if op == "-" else a * b
    st.session_state.captcha_q = f"{a} {op} {b}"
    st.session_state.captcha_ans = str(ans)

new_badges = check_badges(data, level)
if new_badges:
    save(data)
    for icon, name, reward in new_badges:
        st.balloons()
        st.success(f"🎉 {icon} {name} UNLOCKED!")
        st.info(f"💰 Reward: +{reward} XP & Points 🔥")

daily = ensure_daily_generated(data, today_str)

st.markdown(get_theme_css(data.get("theme", "Dark")), unsafe_allow_html=True)

menu = [
    "🏠 Dashboard",
    "🎮 Missions",
    "📊 Stats",
    "📅 Calendar",
    "📜 History",
    "📄 Report",
    "🎯 Dream",
    "🧑 Profile",
    "🏆 Badges",
    "🛒 Shop",
    "⚔️ Boss Fight",
    "🌍 World Map",
    "🏠 Base",
    "🚫 Control Tracker",
    "💧 Water Tracker",
    "💸 Money Tracker",
    "💖 Life System",
    "⚖️ Life Wheel",
    "🎲 Mini Games",
    "⚙️ Settings"
]

if data.get("mobile_nav", False):
    choice = st.sidebar.selectbox("Navigation", menu, key="main_navigation_mobile")
else:
    choice = st.sidebar.radio("Navigation", menu, key="main_navigation")

weekday = today.strftime("%A")

base_tasks = {
    "Morning": ["Wake 5:30", "Brush", "Bath", "Prayer", "Washing"],
    "Workout 💪": ["Walking (40min) 🚶", "Exercise (30min) 🏋️", "Kegel Exercise 🧠", "Breathing 🌬️"],
    "Learning 📚": ["Python (30min)", "English (15min)", "Reading (1hr)"],
    "Health 🥗": ["Water 2L 🌊", "No Junk Food 🌮"],
    "Control 🎯": ["MA001", "PN002"],
    "Limited Control ⏳": ["Instagram (20min)", "YouTube (20min)"]
}

if data.get("custom_tasks"):
    base_tasks["Custom ⭐"] = data["custom_tasks"]

if data.get("dream_steps"):
    base_tasks["Dream Steps 🎯"] = data["dream_steps"]

if today_str in data.get("punishments", {}) and not data.get("punishment_done", {}).get(today_str, False):
    base_tasks["Punishment Mission ⚠️"] = data["punishments"][today_str]

if weekday == "Saturday":
    base_tasks["Weekend"] = ["Movie 🎬"]

if weekday == "Sunday":
    base_tasks["Weekend"] = ["Oil Bath 🛁"]

task_xp = {
    "Wake 5:30": 10, "Brush": 5, "Bath": 5, "Prayer": 10, "Washing": 5,
    "Walking (40min) 🚶": 20, "Exercise (30min) 🏋️": 25, "Kegel Exercise 🧠": 15, "Breathing 🌬️": 10,
    "Python (30min)": 20, "English (15min)": 15, "Reading (1hr)": 15,
    "Water 2L 🌊": 10, "No Junk Food 🌮": 20,
    "Instagram (20min)": 5, "YouTube (20min)": 5,
    "Movie 🎬": 5, "Oil Bath 🛁": 5,
    "MA001": 30, "PN002": 30,
    "Extra Study 30min 📚": 30, "Extra Study 1hr 🔥": 60, "Clean Room 🧹": 20,
    "No Social Media Today 🚫": 40, "Write Self Review ✍️": 20, "No Mobile 1 Hour 📱❌": 30,
    "Read 20 Pages 📖": 30, "Practice English 30 Min 🇬🇧": 25, "Meditation 15 Min 🧘": 20,
    "Exercise 45 Min 🏋️": 35, "Journal Writing 📒": 20, "Cold Shower 🚿": 20,
    "100 Push-ups 💪": 40, "30 Min Walking 🚶": 20, "Meditation 20 Min 🧘": 25,
    "Drink 3L Water 💧": 20, "Wake Up 30 Min Early ⏰": 25, "No YouTube Today 📵": 30,
    "Deep Breathing 20 Min 🌬️": 20
}
task_xp.update(data.get("custom_task_xp", {}))

def render_metrics():
    today_score = data.get("history", {}).get(today_str, None)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("🔥 XP", data["xp"])
    col2.metric("🪙 Coins", data["coins"])
    col3.metric("💎 Gems", data["gems"])
    col4.metric("⚡ Streak", data["streak"])
    col5.metric("🏆 Rank", rank)
    col6.metric("❤️ Health", data["health"])
    if today_score is not None:
        st.info(motivation(today_score, data.get("strict_mode", True)))

def hero_card():
    st.markdown(f"""
    <div class='card'>
        <h1 style='text-align:center;font-size:70px;animation:float 3s infinite;'>{data['equipped'].get('avatar', data['avatar'])}</h1>
        <h2 style='text-align:center;'>{data['name']}</h2>
        <h3 style='text-align:center;'>Level {level}/100 • {rank}</h3>
        <p style='text-align:center;'>Title: {data['equipped'].get('title', data.get('title','Newbie'))}</p>
        <p style='text-align:center;'>Dream: {data.get("dream","")}</p>
        <p style='text-align:center;'>Remaining Days: {max(0,365-days_passed)}</p>
    </div>
    """, unsafe_allow_html=True)

def get_current_boss():
    if level >= 100 or len(data.get("history", {})) >= 365:
        return "Final GOD Boss 🔥", 90
    week_avg = weekly_average(data.get("history", {}))
    month_avg = monthly_average(data.get("history", {}))
    if week_avg < 60:
        return "Weekly Boss ⚔️", 70
    if month_avg < 65:
        return "Monthly Boss ⚔️", 75
    return daily["boss"], 70

if choice == "🏠 Dashboard":
    st.title("🎮 LIFE GAME GOD MODE")
    render_metrics()
    hero_card()

    c1, c2, c3, c4 = st.columns(4)
    daily_key = today_str
    week_key = get_week_key(today)
    month_key = get_month_key(today)

    if c1.button("Claim Daily Reward 🎁"):
        if data["rewards_claimed"]["daily"] != daily_key:
            base = 30 + data["streak"] * 5
            claim_reward(data, "daily", base)
            data["rewards_claimed"]["daily"] = daily_key
            save(data)
            st.success(f"Daily reward claimed! +{base} coins/xp")
            st.rerun()
        else:
            st.warning("Already claimed today.")

    if c2.button("Open Weekly Chest 🧰"):
        if data["rewards_claimed"]["weekly"] != week_key:
            claim_reward(data, "weekly", 50)
            data["rewards_claimed"]["weekly"] = week_key
            save(data)
            st.success("Weekly chest opened!")
            st.rerun()
        else:
            st.warning("Already claimed this week.")

    if c3.button("Open Monthly Chest 🎉"):
        if data["rewards_claimed"]["monthly"] != month_key:
            claim_reward(data, "monthly", 100)
            data["rewards_claimed"]["monthly"] = month_key
            save(data)
            st.success("Monthly chest opened!")
            st.rerun()
        else:
            st.warning("Already claimed this month.")

    if c4.button("Lucky Spin 🎡"):
        if data["rewards_claimed"]["spin"] != daily_key:
            claim_reward(data, "spin", 25)
            data["rewards_claimed"]["spin"] = daily_key
            save(data)
            st.success("Lucky spin reward added!")
            st.rerun()
        else:
            st.warning("Spin already used today.")

    st.markdown(f"""
    <div class='card'>
    <h3>Today's Boss: {get_current_boss()[0]}</h3>
    <p>Damage threshold: {get_current_boss()[1]}%</p>
    <p>Recovery Progress: {min(100, int((data['recovery_days'] / 365) * 100))}%</p>
    <p>Flatline Days: {data.get('flatline_days', 0)}</p>
    </div>
    """, unsafe_allow_html=True)

    if data.get("quote_mode", True):
        today_score = data.get("history", {}).get(today_str, None)
        if today_score is not None:
            st.info(motivation(today_score, data.get("strict_mode", True)))

    mood = st.selectbox("Today Mood", ["😄 Happy", "🙂 Good", "😐 Normal", "😞 Low"], key="today_mood")
    if st.button("Save Mood"):
        data["moods"][today_str] = mood
        save(data)
        st.success("Mood saved ✅")

    st.subheader("Quick Links")
    z1, z2, z3 = st.columns(3)
    z1.write(f"World Zone: {world_zone(level)[0][-1] if world_zone(level)[0] else 'Locked'}")
    z2.write(f"Rank: {rank}")
    z3.write(f"Combo: {combo_multiplier(data['streak'])[1]}")

elif choice == "🎮 Missions":
    st.title("🎮 Missions")

    secret_key = f"secret_revealed_{today_str}"
    if secret_key not in st.session_state:
        st.session_state[secret_key] = False

    side_mission = daily["side"]
    secret_mission = daily["secret"]
    daily_challenge = daily["challenge"]

    locked = today_str in data.get("locked_days", [])
    current_punishments = data.get("punishments", {}).get(today_str, [])
    if locked:
        st.error("🔒 Today already FINAL SAVED! Editing disabled ❌")

    if current_punishments and not data.get("punishment_done", {}).get(today_str, False):
        st.warning("⚠️ Punishment mission pending. Complete it properly.")

    done = 0
    total = 0
    missed = []
    completed = []
    category_scores = {}
    workout_tasks = ["Walking (40min) 🚶", "Exercise (30min) 🏋️", "Kegel Exercise 🧠", "Breathing 🌬️"]
    workout_done = 0
    study_tasks = ["Python (30min)", "English (15min)", "Reading (1hr)"]
    social_tasks = ["Instagram (20min)", "YouTube (20min)"]

    st.markdown(f"<div class='card'><b>Main Mission</b> — complete as much as possible today</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><b>Side Mission</b> — {side_mission}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'><b>Daily Challenge</b> — {daily_challenge}</div>", unsafe_allow_html=True)

    if st.button("Reveal Secret Mission 🔓", disabled=locked):
        st.session_state[secret_key] = True

    if st.session_state[secret_key]:
        st.markdown(f"<div class='card'><b>Secret Mission 🔒</b> — {secret_mission}</div>", unsafe_allow_html=True)

    for g, tasks in base_tasks.items():
        st.subheader(g)
        group_done = 0

        for t in tasks:
            total += 1

            if g == "Control 🎯":
                if data.get("strict_mode", True):
                    st.error("MA001 / PN002 tick means: I avoided porn/masturbation today.")
                else:
                    st.info("Control tracker: clean-day proof.")

            if g == "Punishment Mission ⚠️":
                st.warning(f"Punishment: {t}")

            key = f"task_{today_str}_{g}_{t}"
            checked = st.checkbox(t, key=key, disabled=locked)

            if checked:
                done += 1
                group_done += 1
                completed.append(t)
                if t in workout_tasks:
                    workout_done += 1
            else:
                missed.append(t)

        category_scores[g] = int((group_done / len(tasks)) * 100) if tasks else 0

    for extra_name, extra_task in [("Side Mission", side_mission), ("Daily Challenge", daily_challenge)]:
        total += 1
        checked = st.checkbox(extra_name + f" — {extra_task}", key=f"task_{today_str}_{extra_name}", disabled=locked)
        if checked:
            done += 1
            completed.append(extra_task)
        else:
            missed.append(extra_task)

    if st.session_state.get(secret_key, False):
        total += 1
        checked = st.checkbox(f"Secret Mission — {secret_mission}", key=f"task_{today_str}_SecretMission", disabled=locked)
        if checked:
            done += 1
            completed.append(secret_mission)
        else:
            missed.append(secret_mission)

    missed = list(dict.fromkeys(missed))
    score = int((done / total) * 100) if total else 0

    st.progress(score / 100)
    st.write(f"Score: {score}%")
    st.write(motivation(score, data.get("strict_mode", True)))

    st.subheader("Category Progress")
    for g, s in category_scores.items():
        st.write(f"{g}: {s}%")
        st.progress(safe_progress(s / 100))

    reasons_today = {}
    if missed:
        st.subheader("Missed Reasons")
        for i, t in enumerate(missed):
            r = st.text_input(f"{t}", key=f"reason_input_{today_str}_{i}_{t}", disabled=locked)
            if r:
                reasons_today[t] = r

    if st.button("SAVE", key="temp_save_btn", disabled=locked):
        st.success("✅ Progress Saved (Temporary)")

    st.markdown("---")
    st.subheader("Final Submit")

    current_hour = datetime.now().hour
    if locked:
        st.error("Today already FINAL SAVED!")
    elif current_hour >= 23:
        st.warning("Final save blocked after 11 PM.")
    else:
        st.write(f"🧠 Solve CAPTCHA: {st.session_state.captcha_q}")
        captcha_input = st.text_input("Enter Answer", key=f"captcha_input_{today_str}")
        if st.button("FINAL SAVE 💀", key="final_save_btn"):
            if captcha_input != st.session_state.captcha_ans:
                st.error("Wrong captcha ❌")
            else:
                final_score = score
                final_completed = completed[:]
                final_missed = missed[:]
                final_reasons = reasons_today.copy()

                data["history"][today_str] = final_score
                data.setdefault("day_logs", {})[today_str] = final_completed
                data["points"] += final_score
                data["xp"] += final_score

                mul, combo_text = combo_multiplier(data["streak"])
                reward_base = final_score * mul
                data["coins"] += reward_base
                data["gems"] += 1 if final_score == 100 else 0

                if workout_done == len(workout_tasks):
                    data["xp"] += 50
                    data["coins"] += 20

                if final_score == 100:
                    data["xp"] += 100
                    data["coins"] += 50
                    data["gems"] += 2

                penalty = 0
                for t in final_missed:
                    penalty += task_xp.get(t, 5)

                if data.get("difficulty") == "Soft":
                    penalty = int(penalty * 0.5)
                elif data.get("difficulty") == "Hard":
                    penalty = int(penalty * 1.5)

                data["xp"] -= penalty
                data["points"] -= penalty
                data["coins"] -= max(0, penalty // 2)

                tomorrow_str = str(today + timedelta(days=1))
                data.setdefault("control_tracker", default_data()["control_tracker"])

                for bad_task in ["MA001", "PN002"]:
                    if bad_task not in final_missed:
                        data["control_tracker"][bad_task]["current_clean"] += 1
                        data["control_tracker"][bad_task]["best_clean"] = max(
                            data["control_tracker"][bad_task]["best_clean"],
                            data["control_tracker"][bad_task]["current_clean"]
                        )
                        data["xp"] += 30
                        data["coins"] += 10
                    else:
                        data["control_tracker"][bad_task]["fail_count"] += 1
                        data["control_tracker"][bad_task]["current_clean"] = 0
                        data["control_tracker"][bad_task]["last_fail"] = today_str
                        data["xp"] -= 50
                        data["coins"] -= 20
                        generate_punishments_for_day(data, tomorrow_str, bad_task)

                if current_punishments:
                    data.setdefault("punishment_done", {})[today_str] = True
                    data["xp"] += 50
                    data["coins"] += 20

                data["xp"] = max(0, data["xp"])
                data["points"] = max(0, data["points"])
                data["coins"] = max(0, data["coins"])

                data["health"] = clamp(data["health"] + max(0, final_score // 10) - len(final_missed))
                data["energy"] = clamp(data["energy"] + max(0, workout_done * 3) - len(final_missed))
                data["focus"] = clamp(data["focus"] + max(0, len([t for t in final_completed if t in study_tasks]) * 5) - len([t for t in final_completed if t in social_tasks]) * 3)
                data["happiness"] = clamp(data["happiness"] + max(0, final_score // 20) - max(0, len(final_missed) // 2))

                data["reasons"][today_str] = {
                    "time": datetime.now().strftime("%H:%M"),
                    "tasks": final_reasons
                }

                if today_str not in data["locked_days"]:
                    data["locked_days"].append(today_str)

                data["streak"] = compute_streak(data["history"])
                data["best_streak"] = max(int(data.get("best_streak", 0)), int(data["streak"]))
                data["recovery_days"] = int(data["control_tracker"]["MA001"]["current_clean"])

                for m in [7, 30, 90, 180, 365]:
                    name = f"Recovery {m} Days"
                    if data["recovery_days"] >= m and name not in data["achievements"]:
                        data["achievements"].append(name)
                        data["gems"] += 1

                data["daily_generated"][today_str]["combo"] = combo_text

                save(data)
                st.success("FINAL SAVE DONE! Locked for today 🔒")
                for k in ["captcha_q", "captcha_ans"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()

elif choice == "📊 Stats":
    st.title("📊 Stats")
    MAX_XP = 10000
    data["xp"] = max(0, data["xp"])
    save(data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔥 XP", f"{data['xp']} / {MAX_XP}")
    col2.metric("⚡ Current Streak", data["streak"])
    col3.metric("🏆 Best Streak", data["best_streak"])
    col4.metric("🪙 Coins", data["coins"])

    st.progress(safe_progress(data["xp"] / MAX_XP))
    history = data.get("history", {})
    if history:
        st.subheader("All Time Growth")
        df = pd.DataFrame({"date": list(history.keys()), "score": list(history.values())})
        df["date"] = pd.to_datetime(df["date"])
        st.line_chart(df.set_index("date")["score"])

        st.subheader("Daily Performance")
        today_score = history.get(today_str, 0)
        st.bar_chart(pd.DataFrame({"label": ["Completed", "Pending"], "value": [today_score, 100 - today_score]}).set_index("label"))

        st.write(f"Weekly Average: {weekly_average(history):.1f}%")
        st.write(f"Monthly Average: {monthly_average(history):.1f}%")
        st.write(f"Best Day: {max(history, key=history.get)} → {max(history.values())}%")
        st.write(f"Worst Day: {min(history, key=history.get)} → {min(history.values())}%")

elif choice == "📅 Calendar":
    st.title("📅 Monthly Calendar View")
    history = data.get("history", {})
    cal = calendar.monthcalendar(today.year, today.month)
    month_name = calendar.month_name[today.month]

    heat_rows = []
    for week in cal:
        row = []
        for daynum in week:
            if daynum == 0:
                row.append("")
            else:
                d = date(today.year, today.month, daynum)
                row.append(history.get(str(d), 0))
        heat_rows.append(row)

    fig, ax = plt.subplots(figsize=(12, 4))
    arr = pd.DataFrame(heat_rows)
    im = ax.imshow(arr.astype(float))
    ax.set_title(f"{month_name} {today.year} Heatmap (Score)")
    ax.set_yticks(range(len(cal)))
    ax.set_xticks(range(7))
    ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    for i in range(len(cal)):
        for j in range(7):
            val = heat_rows[i][j]
            txt = "" if val == "" else str(val)
            ax.text(j, i, txt, ha="center", va="center", color="white" if val and val >= 60 else "black")
    fig.colorbar(im, ax=ax, fraction=0.02, pad=0.04)
    st.pyplot(fig)

elif choice == "📜 History":
    st.title("📜 History")
    if data.get("history"):
        for d, s in sorted(data["history"].items(), reverse=True):
            st.markdown(f"<div class='card'><b>{d}</b> — Score: {s}%</div>", unsafe_allow_html=True)
            if d in data["reasons"]:
                r = data["reasons"][d]
                st.write("Time:", r["time"])
                for t, rs in r["tasks"].items():
                    st.write(f"{t} → {rs}")

elif choice == "📄 Report":
    st.title("📄 Daily Report")
    score = data.get("history", {}).get(today_str, None)
    if score is not None:
        report = f"""Name: {data['name']}
Date: {today_str}
Level: {level}
Rank: {rank}
XP: {data['xp']}
Coins: {data['coins']}
Gems: {data['gems']}
Health: {data['health']}
Energy: {data['energy']}
Focus: {data['focus']}
Happiness: {data['happiness']}
Score: {score}
Streak: {data['streak']}
Best Streak: {data['best_streak']}
World Zone: {world_zone(level)[0][-1] if world_zone(level)[0] else 'Locked'}
Boss: {get_current_boss()[0]}
"""
        reasons = data.get("reasons", {}).get(today_str, {})
        if "tasks" in reasons:
            report += "\nMissed Tasks:\n"
            for t, r in reasons["tasks"].items():
                report += f"- {t} → {r}\n"
        st.text_area("Report", report, height=340)
        st.download_button("Download Report", report, f"report_{today_str}.txt")
    else:
        st.info("No final score for today yet.")

elif choice == "🎯 Dream":
    st.title("🎯 Dream Planner")
    dream = st.text_input("Your Dream", value=data.get("dream", ""))
    steps = st.text_area("Dream Steps (one per line)", value="\n".join(data.get("dream_steps", [])))
    if st.button("Save Dream"):
        data["dream"] = dream
        data["dream_steps"] = [x.strip() for x in steps.splitlines() if x.strip()]
        save(data)
        st.success("Dream saved ✅")
    st.write("Dream steps appear in Missions page as extra tasks.")

elif choice == "🧑 Profile":
    st.title("🧑 Profile")
    name = st.text_input("Name", value=data["name"])
    avatar_list = ["😎", "🔥", "👑", "💪", "🧠", "⚡", "🛡️", "🐉"]
    avatar = st.selectbox("Avatar", avatar_list, index=avatar_list.index(data["avatar"]) if data["avatar"] in avatar_list else 0)
    title = st.text_input("Title", value=data.get("equipped", {}).get("title", "Newbie"))
    career_list = ["Student", "Programmer", "Data Analyst", "AI Engineer", "Entrepreneur", "CEO"]
    career = st.selectbox("Career", career_list, index=career_list.index(data.get("career", "Student")) if data.get("career", "Student") in career_list else 0)
    dream = st.text_input("Dream", value=data.get("dream", ""))

    c1, c2, c3 = st.columns(3)
    c1.selectbox("Clothes", ["Casual", "Hoodie", "Suit", "Armor", "Royal"], index=0, key="clothes")
    c2.selectbox("Weapon", ["Wooden Stick", "Sword", "Laptop", "Staff", "Dragon Blade"], index=0, key="weapon")
    c3.selectbox("Pet", ["None", "Cat", "Dog", "Wolf", "Dragon"], index=0, key="pet")

    c4, c5, c6 = st.columns(3)
    c4.selectbox("Wing", ["None", "Angel Wings", "Dark Wings", "Phoenix Wings"], index=0, key="wing")
    c5.selectbox("Aura", ["None", "Glow", "Fire", "Lightning", "Shadow"], index=0, key="aura")
    c6.selectbox("Effect", ["Glow", "Spark", "Pulse", "Storm"], index=0, key="effect")

    if st.button("SAVE PROFILE"):
        data["name"] = name
        data["avatar"] = avatar
        data["title"] = title
        data["career"] = career
        data["dream"] = dream
        data["equipped"]["avatar"] = avatar
        data["equipped"]["title"] = title
        data["equipped"]["clothes"] = st.session_state.get("clothes", "Casual")
        data["equipped"]["weapon"] = st.session_state.get("weapon", "Wooden Stick")
        data["equipped"]["pet"] = st.session_state.get("pet", "None")
        data["equipped"]["wing"] = st.session_state.get("wing", "None")
        data["equipped"]["aura"] = st.session_state.get("aura", "None")
        data["equipped"]["effect"] = st.session_state.get("effect", "Glow")
        save(data)
        st.success("Profile saved ✅")

    st.subheader("Player System")
    st.write(f"Level: {level}")
    st.write(f"Rank: {rank}")
    st.write(f"Health: {data['health']}")
    st.write(f"Energy: {data['energy']}")
    st.write(f"Focus: {data['focus']}")
    st.write(f"Happiness: {data['happiness']}")
    st.write(f"Coins: {data['coins']}")
    st.write(f"Gems: {data['gems']}")

elif choice == "🏆 Badges":
    st.title("🏆 Badges & Achievements")
    for lvl, (icon, name, reward) in badge_rules().items():
        if name in data["badges"]:
            st.markdown(f"<div class='card'><h3>{icon} {name} (Level {lvl})</h3><p>UNLOCKED ✅</p><p>Reward: +{reward}</p></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='card'><h3>🔒 {name}</h3><p>Unlock at Level {lvl}</p><p>Reward: +{reward}</p></div>", unsafe_allow_html=True)

    st.subheader("Achievements")
    achievements = [
        ("Wake up 30 days", len([d for d, log in data.get("day_logs", {}).items() if "Wake 5:30" in log]), 30),
        ("100 workouts", sum(1 for log in data.get("day_logs", {}).values() if any(x in log for x in ["Walking (40min) 🚶", "Exercise (30min) 🏋️", "Kegel Exercise 🧠", "Breathing 🌬️"])), 100),
        ("50 books", sum(1 for log in data.get("day_logs", {}).values() if "Reading (1hr)" in log), 50),
        ("365 clean days", data["recovery_days"], 365),
        ("No junk 100 days", sum(1 for log in data.get("day_logs", {}).values() if "No Junk Food 🌮" in log), 100),
        ("Water challenge", sum(1 for v in data.get("water_logs", {}).values() if v >= 2), 30)
    ]
    for title_a, current, target in achievements:
        status = "✅" if current >= target else "🔒"
        st.write(f"{status} {title_a}: {current}/{target}")

elif choice == "🛒 Shop":
    st.title("🛒 Shop")
    items = [
        ("Avatar: Dragon", 200, ("avatar", "🐉")),
        ("Avatar: Ninja", 150, ("avatar", "🥷")),
        ("Theme: Purple", 200, ("theme", "Purple")),
        ("Theme: Green", 200, ("theme", "Green")),
        ("Title: Legend", 250, ("title", "Legend")),
        ("Title: Hero", 120, ("title", "Hero")),
        ("Icon: Star", 100, ("icon", "⭐")),
        ("Effect: Fire", 180, ("effect", "Fire")),
        ("Pet: Wolf", 220, ("pet", "Wolf")),
        ("Wing: Angel Wings", 300, ("wing", "Angel Wings")),
        ("Aura: Lightning", 280, ("aura", "Lightning"))
    ]
    for label, cost, reward in items:
        owned = label in data.get("shop_owned", [])
        cols = st.columns([3, 1, 1])
        cols[0].write(f"{label} — {money_fmt(cost)}")
        cols[1].write("Owned" if owned else "Available")
        if cols[2].button("Buy", key=f"buy_{label}", disabled=owned):
            if data["coins"] >= cost:
                data["coins"] -= cost
                data["shop_owned"].append(label)
                kind, value = reward
                if kind == "avatar":
                    data["equipped"]["avatar"] = value
                elif kind == "theme":
                    data["theme"] = value
                    data["equipped"]["theme"] = value
                elif kind == "title":
                    data["equipped"]["title"] = value
                    data["title"] = value
                else:
                    data["equipped"][kind] = value
                save(data)
                st.success("Purchased ✅")
                st.rerun()
            else:
                st.error("Not enough coins")

elif choice == "⚔️ Boss Fight":
    st.title("⚔️ Boss Fight")
    boss_name, threshold = get_current_boss()
    st.markdown(f"<div class='card'><h2>{boss_name}</h2><p>Defeat requirement: Score >= {threshold}%</p></div>", unsafe_allow_html=True)

    history = data.get("history", {})
    week_avg = weekly_average(history)
    month_avg = monthly_average(history)
    st.write(f"Weekly Average: {week_avg:.1f}%")
    st.write(f"Monthly Average: {month_avg:.1f}%")

    monsters = [
        ("Lazy Monster 😴", max(0, 100 - data["streak"] * 5)),
        ("Porn Demon 👿", max(0, 100 - data["control_tracker"]["MA001"]["current_clean"] * 10)),
        ("Social Media Monster 📱", max(0, 100 - sum(1 for d in history.values() if d >= 70) * 2)),
        ("Junk Food King 🍔", max(0, 100 - sum(1 for log in data.get("day_logs", {}).values() if "No Junk Food 🌮" in log) * 3)),
        ("Fear Dragon 🐉", max(0, 100 - data["focus"]))
    ]
    for name_b, hp in monsters:
        st.write(name_b)
        st.progress(safe_progress(hp / 100))
    if level >= 100:
        st.success("🔥 Final GOD Boss unlocked!")

elif choice == "🌍 World Map":
    st.title("🌍 World Map")
    unlocked, locked, zones = world_zone(level)
    for zone, req in zones:
        if level >= req:
            st.success(f"{zone} — Unlocked ✅ (Level {req})")
        else:
            st.warning(f"{zone} — Locked 🔒 (Level {req})")
    if unlocked:
        st.info(f"Current Zone: {unlocked[-1]}")

elif choice == "🏠 Base":
    st.title("🏠 Base Building")
    tiers = [
        ("Small Room", 1, 0),
        ("House", 2, 200),
        ("Villa", 3, 500),
        ("Mansion", 4, 1000),
        ("Castle", 5, 2000),
        ("Kingdom", 6, 5000)
    ]
    current = data.get("base_tier", 1)
    for name_b, tier, cost in tiers:
        if tier < current:
            st.success(f"{name_b} — Built")
        elif tier == current:
            st.info(f"{name_b} — Current Base")
        else:
            st.warning(f"{name_b} — Unlock cost {money_fmt(cost)}")
    if st.button("Upgrade Base"):
        next_tier = min(current + 1, len(tiers))
        next_cost = tiers[next_tier - 1][2]
        if data["coins"] >= next_cost and next_tier > current:
            data["coins"] -= next_cost
            data["base_tier"] = next_tier
            data["base_name"] = tiers[next_tier - 1][0]
            save(data)
            st.success("Base upgraded!")
            st.rerun()
        else:
            st.error("Not enough coins or already maxed")

elif choice == "🚫 Control Tracker":
    st.title("🚫 Control Tracker")
    st.info("MA001 = No Porn. PN002 = No Masturbation.")
    for key in ["MA001", "PN002"]:
        ct = data["control_tracker"][key]
        st.markdown(f"<div class='card'><h3>{key}</h3></div>", unsafe_allow_html=True)
        st.write(f"Fail Count: {ct['fail_count']}")
        st.write(f"Current Clean Days: {ct['current_clean']}")
        st.write(f"Best Clean Days: {ct['best_clean']}")
        st.write(f"Last Fail: {ct['last_fail'] or '—'}")
        st.progress(safe_progress(ct["current_clean"] / 365))

elif choice == "💧 Water Tracker":
    st.title("💧 Water Tracker")
    today_liters = st.slider("Today Water Intake (Liters)", 0.0, 5.0, float(data.get("water_logs", {}).get(today_str, 0.0)), 0.1)
    if st.button("Save Water"):
        data.setdefault("water_logs", {})[today_str] = float(today_liters)
        if today_liters >= 2.0:
            data["coins"] += 10
            data["xp"] += 10
        save(data)
        st.success("Water log saved ✅")
    st.write(f"Today: {data.get('water_logs', {}).get(today_str, 0.0)} L")
    st.progress(safe_progress(float(data.get("water_logs", {}).get(today_str, 0.0)) / 3.0))

elif choice == "💸 Money Tracker":
    st.title("💸 Money Tracker")
    bal = data["money"]["balance"]
    st.metric("Balance", money_fmt(bal))
    c1, c2 = st.columns(2)
    with c1:
        inc = st.number_input("Income amount", min_value=0, value=0, step=10)
        inc_note = st.text_input("Income note", key="inc_note")
        if st.button("Add Income"):
            data["money"]["balance"] += int(inc)
            data["money"]["income"].append({"date": today_str, "amount": int(inc), "note": inc_note})
            save(data)
            st.success("Income added ✅")
            st.rerun()
    with c2:
        exp = st.number_input("Expense amount", min_value=0, value=0, step=10)
        exp_note = st.text_input("Expense note", key="exp_note")
        if st.button("Add Expense"):
            data["money"]["balance"] -= int(exp)
            data["money"]["expense"].append({"date": today_str, "amount": int(exp), "note": exp_note})
            save(data)
            st.success("Expense added ✅")
            st.rerun()

elif choice == "💖 Life System":
    st.title("💖 Life System")
    lg = data["life_goals"]
    lg["relationships"] = st.text_input("Relationships Goal", value=lg.get("relationships", ""))
    lg["family"] = st.text_input("Family Goal", value=lg.get("family", ""))
    lg["health"] = st.text_input("Health Goal", value=lg.get("health", ""))
    lg["finance"] = st.text_input("Finance Goal", value=lg.get("finance", ""))
    lg["learning"] = st.text_input("Learning Goal", value=lg.get("learning", ""))
    if st.button("Save Life Goals"):
        data["life_goals"] = lg
        save(data)
        st.success("Life goals saved ✅")

    st.subheader("Recovery")
    st.write(f"Clean Days: {data['recovery_days']}")
    st.write(f"Flatline Days: {data.get('flatline_days', 0)}")
    st.write(f"Recovery Progress: {min(100, int((data['recovery_days'] / 365) * 100))}%")

elif choice == "⚖️ Life Wheel":
    st.title("⚖️ Life Wheel")
    lw = data.get("life_wheel", {})
    for k in ["Health", "Finance", "Learning", "Relationships", "Peace"]:
        lw[k] = st.slider(k, 0, 100, int(lw.get(k, 50)))
    if st.button("Save Life Wheel"):
        data["life_wheel"] = lw
        save(data)
        st.success("Life wheel saved ✅")
    df = pd.DataFrame({"Category": list(lw.keys()), "Score": list(lw.values())})
    st.bar_chart(df.set_index("Category")["Score"])

elif choice == "🎲 Mini Games":
    st.title("🎲 Mini Games")
    tabs = st.tabs(["Memory", "Quiz", "Typing", "Focus Timer", "Breathing"])
    with tabs[0]:
        st.subheader("Memory Game")
        seq_key = f"memory_seq_{today_str}"
        if seq_key not in st.session_state:
            st.session_state[seq_key] = random.sample(["🍎", "⭐", "🔥", "💧", "🐉", "🌙"], 4)
        st.write("Remember:", " ".join(st.session_state[seq_key]))
        guess = st.text_input("Type the sequence without spaces", key=f"memory_guess_{today_str}")
        if st.button("Check Memory"):
            target = "".join(st.session_state[seq_key])
            if guess.strip() == target:
                st.success("Correct! +20 coins")
                data["coins"] += 20
                data["mini_games_stats"]["memory_best"] = max(data["mini_games_stats"]["memory_best"], 1)
                save(data)
            else:
                st.error("Wrong")
    with tabs[1]:
        st.subheader("Quiz")
        q = random.choice([
            ("What is 2 + 2?", "4"),
            ("What color is the sky?", "blue"),
            ("How many days in a week?", "7")
        ])
        ans = st.text_input(q[0], key=f"quiz_{today_str}")
        if st.button("Check Quiz"):
            if ans.strip().lower() == q[1]:
                st.success("Correct! +15 XP")
                data["xp"] += 15
                data["mini_games_stats"]["quiz_best"] = max(data["mini_games_stats"]["quiz_best"], 1)
                save(data)
            else:
                st.error("Wrong answer")
    with tabs[2]:
        st.subheader("Typing Speed")
        sentence = "I will control my habits and build a strong life."
        st.write(sentence)
        if "typing_start" not in st.session_state:
            st.session_state.typing_start = None
        if st.button("Start Typing Test"):
            st.session_state.typing_start = datetime.now()
        typed = st.text_input("Type here", key=f"type_{today_str}")
        if st.button("Submit Typing"):
            if st.session_state.typing_start:
                elapsed = max(1, (datetime.now() - st.session_state.typing_start).total_seconds())
                wpm = int((len(typed.split()) / elapsed) * 60)
                st.success(f"{wpm} WPM")
                data["mini_games_stats"]["typing_best_wpm"] = max(data["mini_games_stats"]["typing_best_wpm"], wpm)
                data["coins"] += max(0, wpm // 2)
                save(data)
    with tabs[3]:
        st.subheader("Focus Timer")
        mins = st.select_slider("Choose minutes", options=[5, 10, 15, 20, 25, 30, 45, 60], value=15)
        if "focus_start" not in st.session_state:
            st.session_state.focus_start = None
            st.session_state.focus_mins = None
        if st.button("Start Focus Session"):
            st.session_state.focus_start = datetime.now()
            st.session_state.focus_mins = mins
        if st.session_state.focus_start:
            elapsed = (datetime.now() - st.session_state.focus_start).total_seconds() / 60
            remaining = max(0, st.session_state.focus_mins - elapsed)
            st.write(f"Remaining: {remaining:.1f} min")
            if remaining <= 0:
                st.success("Focus session complete! +20 XP")
                data["xp"] += 20
                data["focus"] = clamp(data["focus"] + 5)
                save(data)
                st.session_state.focus_start = None
    with tabs[4]:
        st.subheader("Breathing Challenge")
        if st.button("Complete 4-4-4-4 Breathing"):
            data["energy"] = clamp(data["energy"] + 5)
            data["happiness"] = clamp(data["happiness"] + 5)
            data["xp"] += 10
            save(data)
            st.success("Breathing challenge completed ✅")

elif choice == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.markdown("<div class='card'>Adjust theme, mode, and reset data.</div>", unsafe_allow_html=True)

    data["theme"] = st.selectbox("Theme", ["Dark", "Light", "Purple", "Green"], index=["Dark", "Light", "Purple", "Green"].index(data.get("theme", "Dark")))
    data["mobile_nav"] = st.checkbox("Mobile Navigation", value=data.get("mobile_nav", False))
    data["quote_mode"] = st.checkbox("Coach Quotes", value=data.get("quote_mode", True))
    data["strict_mode"] = st.checkbox("Strict Mode", value=data.get("strict_mode", True))
    difficulty_options = ["Soft", "Normal", "Hard"]
    current_diff = data.get("difficulty", "Normal")
    difficulty = st.selectbox("Difficulty", difficulty_options, index=difficulty_options.index(current_diff) if current_diff in difficulty_options else 1)
    data["difficulty"] = difficulty

    if st.button("Save Settings"):
        save(data)
        st.success("Settings saved ✅")
        st.rerun()

    st.markdown("---")
    pwd = st.text_input("Enter Reset Password", type="password")
    confirm = st.checkbox("Confirm reset all data")
    if st.button("RESET ALL DATA 💀"):
        if confirm and pwd == RESET_PASS:
            reset_data = default_data()
            with open(DATA_FILE, "w") as f:
                json.dump(reset_data, f, indent=2)
            st.session_state.clear()
            st.success("Full reset done 💀")
            st.rerun()
        else:
            st.error("Wrong password or not confirmed")
