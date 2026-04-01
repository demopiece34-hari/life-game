import streamlit as st
import json, os
from datetime import date, datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

# ---------- LOGIN ----------
if "login" not in st.session_state:
    st.session_state.login = False

def login_ui():
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        if user == "hari" and pwd == "9442176514":
            st.session_state.login = True
            st.success("Welcome 😈")
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
        "reasons": {},
        "start_date": str(date.today())
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
today = date.today()
today_str = str(today)

# ---------- UI ----------
st.markdown("<style>body{background:#0f172a;color:white}</style>", unsafe_allow_html=True)

# ---------- NAV (ADDED REPORT OPTION) ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","📜 History","📄 Report","🧑 Profile","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- LEVEL ----------
days_passed = (today - datetime.strptime(data["start_date"], "%Y-%m-%d").date()).days
level = int((days_passed / 365) * 100)

# ---------- TASKS ----------
weekday = today.strftime("%A")

task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath"],
    "Learning": ["Reading","Python"],
    "Workout": ["Walking","Exercise"],
    "Limited Control": ["Instagram (20 min)","YouTube (20 min)"]
}

if weekday == "Sunday":
    task_groups["Weekend"] = ["Oil Bath (Sunday Only)"]

if weekday == "Saturday":
    task_groups["Weekend"] = task_groups.get("Weekend", []) + ["Movie (Saturday Only)"]

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":
    st.title("🎯 LIFE GAME GOD MODE")

# ---------- MISSIONS ----------
elif choice == "🎮 Missions":

    st.title("🎮 Missions")

    done=0
    total=0
    completed=[]
    missed=[]

    for g,tasks in task_groups.items():
        st.subheader(g)
        for t in tasks:
            total+=1
            key=f"{today_str}_{t}"
            if st.checkbox(t,key=key):
                completed.append(t)
                done+=1
            else:
                missed.append(t)

    score=int((done/total)*100)
    st.progress(score/100)
    st.write("Score:",score)

    reasons_today={}
    if missed:
        st.subheader("Missed Reason")
        for t in missed:
            r=st.text_input(f"{t}")
            if r:
                reasons_today[t]=r

    if st.button("SAVE"):
        data["history"][today_str]=score
        data["points"]+=score

        data["reasons"][today_str]={
            "time":str(datetime.now().strftime("%H:%M")),
            "tasks":reasons_today
        }

        data["last"]=today_str
        save(data)
        st.success("Saved")

# ---------- STATS ----------
elif choice == "📊 Stats":

    history=data.get("history",{})

    if history:
        dates=list(history.keys())
        scores=list(history.values())

        st.plotly_chart(px.line(x=dates,y=scores))

        st.subheader("Daily Circle")
        st.plotly_chart(px.pie(values=scores,names=dates))

        st.subheader("Year Circle")
        st.plotly_chart(px.pie(values=scores,names=dates,hole=0.5))

# ---------- HISTORY ----------
elif choice == "📜 History":

    for d,s in data["history"].items():
        st.write(d,"Score:",s)
        if d in data["reasons"]:
            r=data["reasons"][d]
            st.write("Time:",r["time"])
            for t,rs in r["tasks"].items():
                st.write(t,"→",rs)

# ---------- 🆕 REPORT SYSTEM ----------
elif choice == "📄 Report":

    st.title("📄 Daily Report")

    if today_str in data["history"]:
        score = data["history"][today_str]
        reasons = data["reasons"].get(today_str, {})

        report = f"""
LIFE GAME DAILY REPORT 😈
Date: {today_str}

Score: {score}

"""

        if "tasks" in reasons:
            report += "\nMissed Tasks Reasons:\n"
            for t, r in reasons["tasks"].items():
                report += f"- {t} → {r}\n"

        st.text_area("Report Preview", report, height=300)

        st.download_button(
            label="⬇️ Download Report",
            data=report,
            file_name=f"report_{today_str}.txt",
            mime="text/plain"
        )
    else:
        st.info("No report for today")

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    name=st.text_input("Name",value=data["name"])

    if st.button("SAVE"):
        data["name"]=name
        save(data)

# ---------- SETTINGS ----------
elif choice == "⚙️ Settings":

    pwd=st.text_input("Password",type="password")

    if st.button("RESET"):
        if pwd=="h1a2r3i4s5h6":
            save({
                "points":0,"streak":0,"last":"",
                "xp":0,"avatar":"😎","name":"Player",
                "history":{},"badges":[],"reasons":{},
                "start_date":str(date.today())
            })
            st.success("Reset")
