import streamlit as st
import json, os, random
from datetime import date, datetime, timedelta
import plotly.express as px

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
            st.success("Login Success 🔥")
            st.rerun()
        else:
            st.error("Wrong credentials ❌")
    st.stop()

# ---------- DATA ----------
DATA_FILE = "data.json"

def default_data():
    return {
        "points": 0,
        "xp": 0,
        "ma001_last": "",
        "streak": 0,
        "avatar": "😎",
        "name": "Player",
        "dream": "",
        "history": {},
        "badges": [],
        "reasons": {},
        "start_date": str(date.today()),
        "locked_days": []
    }

def load():
    if not os.path.exists(DATA_FILE):
        return default_data()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except:
        return default_data()

    # fill missing keys
    d = default_data()
    for k in d:
        if k not in data:
            data[k] = d[k]
    return data

def save(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f)

data = load()
today = date.today()
today_str = str(today)

# ---------- CAPTCHA ----------
if "captcha" not in st.session_state:
    a, b = random.randint(10, 30), random.randint(10, 30)
    st.session_state.captcha = (f"{a} + {b}", str(a + b))

# ---------- LEVEL ----------
days_passed = (today - datetime.strptime(data["start_date"], "%Y-%m-%d").date()).days
level = min(100, int((days_passed / 365) * 100))

# ---------- BADGES ----------
BADGES = {
    10: ("🪵", "Starter", 50),
    30: ("🥈", "Silver", 150),
    50: ("💎", "Platinum", 250),
    70: ("👑", "Master", 400),
    100: ("🔥", "GOD MODE", 1000)
}

for lvl, (icon, name, reward) in BADGES.items():
    if level >= lvl and name not in data["badges"]:
        data["badges"].append(name)
        data["xp"] += reward
        data["points"] += reward
        st.success(f"{icon} {name} unlocked! +{reward} XP 🔥")
        save(data)

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","📜 History","🧑 Profile","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- TASKS ----------
task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath","Prayer"],
    "Workout": ["Walking","Exercise","Breathing"],
    "Learning": ["Python","English","Reading"],
    "Health": ["Water","No Junk"],
    "Control": ["MA001","PN002"]
}

task_xp = {
    "Wake 5:30":10,"Brush":5,"Bath":5,"Prayer":10,
    "Walking":20,"Exercise":25,"Breathing":10,
    "Python":20,"English":15,"Reading":15,
    "Water":10,"No Junk":20
}

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":
    st.title("🎯 LIFE GAME")

    st.markdown(f"""
    <div style='text-align:center'>
    <h1>{data['avatar']}</h1>
    <h2>{data['name']}</h2>
    <h3>Level {level}</h3>
    </div>
    """, unsafe_allow_html=True)

# ---------- MISSIONS ----------
elif choice == "🎮 Missions":
    st.title("🎮 Missions")

    locked = today_str in data["locked_days"]
    done, total = 0, 0
    missed = []

    for g, tasks in task_groups.items():
        st.subheader(g)
        for t in tasks:
            total += 1
            val = st.checkbox(t, key=t, disabled=locked)

            if val:
                done += 1
            else:
                missed.append(t)

    score = int((done/total)*100)
    st.progress(score/100)
    st.write(f"Score: {score}%")

    if st.button("FINAL SAVE"):
        q, ans = st.session_state.captcha
        user_ans = st.text_input(f"Solve: {q}")

        if user_ans == ans:
            data["history"][today_str] = score
            data["xp"] += score
            data["points"] += score

            # penalty
            for t in missed:
                data["xp"] -= task_xp.get(t,5)

            data["locked_days"].append(today_str)
            save(data)

            st.success("Saved & Locked 🔒")
            del st.session_state["captcha"]
            st.rerun()
        else:
            st.error("Wrong captcha ❌")

# ---------- STATS ----------
elif choice == "📊 Stats":
    st.title("📊 Stats")

    history = data["history"]

    if history:
        st.plotly_chart(px.line(x=list(history.keys()), y=list(history.values())))

# ---------- HISTORY ----------
elif choice == "📜 History":
    for d,s in data["history"].items():
        st.write(f"{d} → {s}%")

# ---------- PROFILE ----------
elif choice == "🧑 Profile":
    name = st.text_input("Name", value=data["name"])
    avatar = st.selectbox("Avatar",["😎","🔥","👑","💪"])

    if st.button("Save"):
        data["name"] = name
        data["avatar"] = avatar
        save(data)
        st.success("Saved ✅")

# ---------- SETTINGS ----------
elif choice == "⚙️ Settings":
    if st.button("RESET"):
        save(default_data())
        st.success("Reset Done 💀")
        st.rerun()
