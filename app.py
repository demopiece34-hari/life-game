import streamlit as st
import json, os
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
            st.success("Welcome 😈")
        else:
            st.error("Wrong credentials")
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

# ---------- LEVEL SYSTEM (365 DAYS → LEVEL 100) ----------
days_passed = (today - datetime.strptime(data["start_date"], "%Y-%m-%d").date()).days
level = min(100, int((days_passed / 365) * 100))

# ---------- UI STYLE ----------
st.markdown("""
<style>
body {background:linear-gradient(135deg,#0f172a,#1e293b);color:white;}

.card {
    background:rgba(255,255,255,0.08);
    padding:20px;
    border-radius:20px;
    backdrop-filter:blur(10px);
    margin-bottom:15px;
    animation:fade 0.5s;
}

@keyframes fade {
    from{opacity:0;transform:translateY(20px);}
    to{opacity:1;}
}

@keyframes float {
    0%{transform:translateY(0)}
    50%{transform:translateY(-10px)}
    100%{transform:translateY(0)}
}

@keyframes slide {
    from{opacity:0;transform:translateX(-30px);}
    to{opacity:1;}
}

.stButton button {
    background:linear-gradient(45deg,#6366f1,#8b5cf6);
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","📜 History","📄 Report","🧑 Profile","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- TASKS ----------
weekday = today.strftime("%A")

task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath"],
    "Learning": ["Reading","Python"],
    "Health": ["Water 2L","No Junk"],
    "Control": ["MA001","PN002"],
    "Workout": ["Walking","Exercise"],
    "Limited Control": ["Instagram (20 min)","YouTube (20 min)"],
    "Weekend": ["Movie (Saturday)","Oil Bath (Sunday)"]  # ALWAYS SHOW
}

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":

    st.title("🎯 LIFE GAME")

    st.markdown(f"""
    <div class='card'>
    <h1 style='text-align:center;font-size:70px;animation:float 3s infinite;'>😎</h1>
    <h2 style='text-align:center;'>{data['name']}</h2>
    <h3 style='text-align:center;'>Level {level}/100</h3>
    </div>
    """, unsafe_allow_html=True)

    # Daily circle graph
    if today_str in data["history"]:
        score = data["history"][today_str]
        st.plotly_chart(px.pie(values=[score,100-score],names=["Done","Remaining"]))

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
            if st.checkbox(t,key=f"{today_str}_{t}"):
                done+=1
                completed.append(t)
            else:
                missed.append(t)

    score=int((done/total)*100)
    st.progress(score/100)

    reasons_today={}
    if missed:
        st.subheader("Missed Reasons")
        for t in missed:
            r=st.text_input(f"{t}")
            if r:
                reasons_today[t]=r

    if st.button("SAVE"):
        data["history"][today_str]=score
        data["points"]+=score
        data["xp"]+=score  # ADD XP SYSTEM

        data["reasons"][today_str]={
            "time":datetime.now().strftime("%H:%M"),
            "tasks":reasons_today
        }

        save(data)
        st.success("Saved 😈")

# ---------- STATS ----------
elif choice == "📊 Stats":

    history=data.get("history",{})

    if history:
        dates=list(history.keys())
        scores=list(history.values())

        st.plotly_chart(px.line(x=dates,y=scores,title="Performance"))

        # DAILY CIRCLE (TASK BASED)
        today_score = history.get(today_str,0)
        st.subheader("Daily Task Circle")
        st.plotly_chart(px.pie(values=[today_score,100-today_score],names=["Done","Missed"]))

        # YEARLY PROGRESS (365 BASE)
        yearly = [s for s in scores]
        st.subheader("Year Circle (365 Days)")
        st.plotly_chart(px.pie(values=yearly,names=dates,hole=0.5))

# ---------- HISTORY ----------
elif choice == "📜 History":

    for d,s in data["history"].items():
        st.markdown(f"<div class='card' style='animation:slide 0.5s'>{d} - Score: {s}</div>", unsafe_allow_html=True)

        if d in data["reasons"]:
            r=data["reasons"][d]
            st.write("Time:",r["time"])

            for t,rs in r["tasks"].items():
                st.write(t,"→",rs)

# ---------- REPORT ----------
elif choice == "📄 Report":

    st.title("📄 Daily Report")

    if today_str in data["history"]:
        score=data["history"][today_str]
        reasons=data["reasons"].get(today_str,{})

        report=f"""
🔥 LIFE GAME REPORT 😈

Date: {today_str}
Level: {level}
Points: {data['points']}

Score: {score}

"""

        if "tasks" in reasons:
            report+="Missed Tasks:\n"
            for t,r in reasons["tasks"].items():
                report+=f"{t} → {r}\n"

        st.text_area("Report",report,height=300)
        st.download_button("Download",report,f"report_{today_str}.txt")

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    st.title("🧑🏻‍🦱 Profile")

    name=st.text_input("Name",value=data["name"])
    avatar=st.selectbox("Avatar",["😎","🔥","👑","💪"])

    st.markdown(f"### Preview: {avatar} {name}")

    if st.button("SAVE"):
        data["name"]=name
        data["avatar"]=avatar
        save(data)

# ---------- SETTINGS ----------
elif choice == "⚙️ Settings":

    st.markdown("<div class='card' style='animation:fade 1s'>⚙️ Settings Panel</div>",unsafe_allow_html=True)

    pwd=st.text_input("Password",type="password")

    if st.button("RESET"):
        if pwd=="h1a2r3i4s5h6":
            save({
                "points":0,"streak":0,"last":"",
                "xp":0,"avatar":"😎","name":"Player",
                "history":{},"reasons":{},
                "start_date":str(date.today())
            })
            st.success("Reset Done")
