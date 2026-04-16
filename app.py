import streamlit as st
import json, os
import random
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

# ---------- LOGIN ----------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        if user == "hari" and pwd == "9442176514":
            st.session_state.login = True
            st.success("Login Success ⛓️‍💥")
        else:
            st.error("Wrong credentials 🔗")
    st.stop()

# ---------- DATA ----------
DATA_FILE = "data.json"

def load():
    default = {
        "points": 0,
        "xp": 0,
        "ma001_last": "",
        "ma001_strict": True,
        "streak": 0,
        "last": "",
        "avatar": "😎",
        "name": "Player",
        "dream": "",
        "history": {},
        "badges": [],
        "reasons": {},
        "start_date": str(date.today()),
        "final_submitted": {},
        "locked_days": [],
    }

    if not os.path.exists(DATA_FILE):
        return default

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        return default

    for k in default:
        if k not in data:
            data[k] = default[k]

    return data

def save(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f)

data = load()
today = date.today()
today_str = str(today)

# ---------- CAPTCHA ----------
if "captcha_q" not in st.session_state:
    a = random.randint(10, 50)
    b = random.randint(10, 50)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        ans = a + b
    elif op == "-":
        ans = a - b
    else:
        ans = a * b

    st.session_state.captcha_q = f"{a} {op} {b}"
    st.session_state.captcha_ans = str(ans)

# ---------- LEVEL ----------
days_passed = (today - datetime.strptime(data["start_date"], "%Y-%m-%d").date()).days
level = min(100, int((days_passed / 365) * 100))
remaining_days = max(0, 365 - days_passed)

# ---------- BADGES ----------
BADGE_RULES = {
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

def check_badges():
    unlocked = []
    for lvl, (icon, name, reward) in BADGE_RULES.items():
        if level >= lvl and name not in data["badges"]:
            data["badges"].append(name)
            data["xp"] += reward
            data["points"] += reward
            unlocked.append((icon, name, reward))
    return unlocked

new_badges = check_badges()

if new_badges:
    save(data)
    for icon, name, reward in new_badges:
        st.balloons()
        st.success(f"🎉 {icon} {name} UNLOCKED!")
        st.info(f"💰 Reward: +{reward} XP & Points 🔥")

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","📜 History","📄 Report","🧑 Profile","🏆 Badges","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- TASK GROUPS ----------
weekday = today.strftime("%A")

task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath","Prayer","Washing"],
    "Workout 💪": ["Walking (40min) 🚶","Exercise (30min) 🏋️","Kegel Exercise 🧠","Breathing 🌬️"],
    "Learning 📚": ["Python (30min)","English (15min)","Reading (1hr)"],
    "Health 🥗": ["Water 2L 🌊","No Junk Food 🌮"],
    "Control 🎯": ["MA001","PN002"],
    "Limited Control ⏳": ["Instagram (20min)","YouTube (20min)"]
}

if weekday == "Saturday":
    task_groups["Weekend"] = ["Movie 🎬"]

if weekday == "Sunday":
    task_groups["Weekend"] = ["Oil Bath 🛁"]

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":
    st.title("🎯 LIFE GAME")

    st.markdown(f"""
    <div style='text-align:center'>
    <h1>{data['avatar']}</h1>
    <h2>{data['name']}</h2>
    <h3>Level {level}/100</h3>
    <p>Remaining Days: {remaining_days}</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- MISSIONS ----------
elif choice == "🎮 Missions":
    st.title("🎮 Missions")

    done = 0
    total = 0
    missed = []

    locked = today_str in data.get("locked_days", [])

    for g, tasks in task_groups.items():
        st.subheader(g)

        for t in tasks:
            total += 1

            if st.checkbox(t, key=f"{today_str}_{t}", disabled=locked):
                done += 1
            else:
                missed.append(t)

    score = int((done / total) * 100) if total else 0
    st.progress(score / 100)
    st.write(f"Score: {score}%")

    if st.button("FINAL SAVE 💀"):
        if st.text_input("Captcha") == st.session_state.captcha_ans:

            data["history"][today_str] = score
            data["xp"] += score
            data["points"] += score

            data["locked_days"].append(today_str)
            save(data)

            st.success("Saved 🔒")
            st.rerun()
        else:
            st.error("Wrong captcha ❌")

# ---------- STATS ----------
elif choice == "📊 Stats":
    st.title("📊 Stats")

    history = data.get("history", {})

    if history:
        dates = list(history.keys())
        scores = list(history.values())
        st.line_chart(scores)

# ---------- HISTORY ----------
elif choice == "📜 History":
    for d, s in data["history"].items():
        st.write(f"{d} → {s}%")

# ---------- PROFILE ----------
elif choice == "🧑 Profile":
    name = st.text_input("Name", value=data["name"])
    avatar = st.selectbox("Avatar", ["😎","🔥","👑","💪"])

    if st.button("SAVE"):
        data["name"] = name
        data["avatar"] = avatar
        save(data)
        st.success("Saved ✅")

# ---------- BADGES ----------
elif choice == "🏆 Badges":
    st.title("🏆 Badges")

    for lvl, (icon, name, reward) in BADGE_RULES.items():
        if name in data["badges"]:
            st.success(f"{icon} {name} unlocked")
        else:
            st.warning(f"🔒 Unlock at level {lvl}")

# ---------- SETTINGS ----------
elif choice == "⚙️ Settings":
    pwd = st.text_input("Password", type="password")
    confirm = st.checkbox("Confirm reset")

    if st.button("RESET"):
        if confirm and pwd == "h1a2r3i4s5h6":
            save(load())
            st.success("Reset Done 💀")
            st.rerun()
        else:
            st.error("Wrong / not confirmed ❌")
