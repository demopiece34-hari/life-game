import streamlit as st
import json, os
from datetime import date, datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

# ---------- LOGIN SYSTEM ----------
if "login" not in st.session_state:
    st.session_state.login = False

def login_ui():
    st.title("🔐 Login System")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        if user == "hari" and pwd == "1234":
            st.session_state.login = True
            st.success("Login Success 😈")
        else:
            st.error("Wrong credentials")

if not st.session_state.login:
    login_ui()
    st.stop()

# ---------- DATA ----------
DATA_FILE = "data.json"

def load():
    default = {
        "points": 0,
        "streak": 0,
        "last": "",
        "xp": 0,
        "avatar": "😎",
        "name": "Player",
        "history": {},
        "badges": [],
        "reasons": {}
    }
    if not os.path.exists(DATA_FILE):
        return default
    data = json.load(open(DATA_FILE))
    for k in default:
        if k not in data:
            data[k] = default[k]
    return data

def save(d):
    json.dump(d, open(DATA_FILE, "w"))

data = load()
today = str(date.today())

# ---------- SOUND EFFECT ----------
def play_sound():
    st.markdown("""
    <audio autoplay>
    <source src="https://www.soundjay.com/buttons/sounds/button-3.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

# ---------- UI STYLE ----------
st.markdown("""<style>
body {background: linear-gradient(135deg,#0f172a,#1e293b); color:#e2e8f0;}
.card {background: rgba(255,255,255,0.05); padding:20px; border-radius:18px;}
.badge {padding:5px 10px; border-radius:20px; background:red; color:white;}
</style>""", unsafe_allow_html=True)

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","📜 History","🧑 Profile","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- SIDEBAR ----------
level = data["xp"] // 100
xp_current = data["xp"] % 100

st.sidebar.markdown(f"# {data['avatar']} {data['name']}")
st.sidebar.write(f"🏆 Level: {level}")
st.sidebar.progress(xp_current / 100)
st.sidebar.write(f"⚡ XP: {data['xp']}")
st.sidebar.write(f"💯 Points: {data['points']}")
st.sidebar.write(f"🔥 Streak: {data['streak']}")

# ---------- TASKS ----------
task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath","Prayer","Washing"],
    "Learning": ["Reading","English","Python"],
    "Health": ["Water 2L","No Junk"],
    "Workout": ["Walking","Exercise","Kegel"],
    "Control": ["MA001","PN002"],
    "Limited Control": [
        "Instagram (20 min only)",
        "YouTube (20 min only)",
        "Movie (Weekly Once)"
    ],
    "Weekend": ["Oil Bath"]
}

task_points = {
    "Wake 5:30": 20,
    "Python": 25,
    "Exercise": 20,
    "No Junk": 15
}

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":
    st.title("🎯 LIFE GAME GOD MODE 😈")

# ---------- MISSIONS ----------
elif choice == "🎮 Missions":

    st.title("🎮 Daily Missions")

    done = 0
    total = 0
    completed_tasks = []
    missed_tasks = []

    for group, tasks in task_groups.items():
        st.subheader(group)
        for t in tasks:
            total += 1
            key = f"{today}_{t}"
            if st.checkbox(t, key=key):
                done += 1
                completed_tasks.append(t)
            else:
                missed_tasks.append(t)

    score = int((done/total)*100)
    st.progress(score/100)
    st.write(f"🎯 Score: {score}")

    # ---------- MISSED TASK REASON ----------
    reasons_today = {}

    if missed_tasks:
        st.subheader("❗ Missed Task Reasons")
        for t in missed_tasks:
            reason = st.text_input(f"Why missed: {t}")
            if reason:
                reasons_today[t] = reason

    # ---------- SAVE ----------
    if st.button("💾 SAVE"):

        earn = sum(task_points.get(t, 10) for t in completed_tasks)

        data["xp"] += earn
        data["points"] += earn
        data["history"][today] = score

        # store reasons
        data["reasons"][today] = {
            "time": str(datetime.now().time()),
            "tasks": reasons_today
        }

        # streak
        last = data.get("last", "")
        if last:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
            if date.today() == last_date + timedelta(days=1):
                data["streak"] += 1
            else:
                data["streak"] = 1
        else:
            data["streak"] = 1

        data["last"] = today

        save(data)
        play_sound()
        st.success(f"🔥 +{earn} XP Saved!")

# ---------- HISTORY ----------
elif choice == "📜 History":

    st.title("📜 History")

    if data["history"]:
        for d, score in data["history"].items():
            st.markdown(f"### 📅 {d} - Score: {score}")

            if d in data["reasons"]:
                r = data["reasons"][d]
                st.write(f"⏰ Time: {r['time']}")

                for task, reason in r["tasks"].items():
                    st.write(f"❌ {task} → {reason}")

    else:
        st.info("No history")

# ---------- STATS ----------
elif choice == "📊 Stats":

    history = data.get("history", {})

    if history:
        dates = list(history.keys())[-7:]
        scores = [history[d] for d in dates]

        fig = px.area(x=dates, y=scores)
        st.plotly_chart(fig)

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    name = st.text_input("Enter Name", value=data["name"])
    avatar = st.selectbox("Avatar", ["😎","🔥","👑","💪","🤖"])

    if st.button("SAVE PROFILE"):
        data["name"] = name
        data["avatar"] = avatar
        save(data)
        st.success("Updated!")

# ---------- SETTINGS ----------
elif choice == "⚙️ Settings":

    password = st.text_input("Enter Password", type="password")

    if st.button("RESET"):
        if password == "h1a2r3i4s5h6":
            save({
                "points":0,"streak":0,"last":"",
                "xp":0,"avatar":"😎","name":"Player",
                "history":{},"badges":[],"reasons":{}
            })
            st.success("Reset Done")
        else:
            st.error("Wrong Password")
