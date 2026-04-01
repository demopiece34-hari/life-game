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
        "streak": 0,
        "last": "",
        "avatar": "😎",
        "name": "Player",
        "dream": "",
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

# ---------- LEVEL ----------
days_passed = (today - datetime.strptime(data["start_date"], "%Y-%m-%d").date()).days
level = min(100, int((days_passed / 365) * 100))
remaining_days = max(0, 365 - days_passed)

# ---------- UI STYLE ----------
st.markdown("""
<style>
body {background:linear-gradient(135deg,#0f172a,#1e293b);color:white;}

.card {
    background:rgba(255,255,255,0.08);
    padding:20px;
    border-radius:20px;
    backdrop-filter:blur(12px);
    margin-bottom:15px;
    animation:fade 0.6s;
}

@keyframes fade {
    from{opacity:0;transform:translateY(20px);}
    to{opacity:1;}
}

@keyframes float {
    0%{transform:translateY(0)}
    50%{transform:translateY(-12px)}
    100%{transform:translateY(0)}
}

.stButton button {
    background:linear-gradient(45deg,#6366f1,#8b5cf6);
    color:white;
    border-radius:10px;
    transition:0.3s;
}
.stButton button:hover {
    transform:scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","📜 History","📄 Report","🧑 Profile","⚙️ Settings"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- TASKS ----------
weekday = today.strftime("%A")

task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath"," Prayer","Washing"],
    "Learning": ["Python (30min)","English (15min)","Reading (1hr)"],
    "Health": ["Water 2L 🌊","No Junk Food 🌮"],
    "Control": ["MA001","PN002"],
    "Limited Control": ["Instagram (20min)","YouTube (20min)"]
}

if weekday == "Saturday":
    task_groups["Weekend"] = ["Movie 🎬"]

if weekday == "Sunday":
    task_groups["Weekend"] = ["Oil Bath 🛁"]

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":

    st.title("🎯 LIFE GAME")

    st.markdown(f"""
    <div class='card'>
    <h1 style='text-align:center;font-size:70px;animation:float 3s infinite;'>😎</h1>
    <h2 style='text-align:center;'>{data['name']}</h2>
    <h3 style='text-align:center;'>Level {level}/100</h3>
    <p style='text-align:center;'>🎯 Remaining Days: {remaining_days}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ---------- DATE & DAY (BOTTOM CENTER) ----------
    current_day = today.strftime("%A")
    current_date = today.strftime("%d-%m-%Y")

    st.markdown(f"""
    <div style='
        position:fixed;
        bottom:10px;
        left:50%;
        transform:translateX(-50%);
        background:rgba(255,255,255,0.08);
        padding:10px 20px;
        border-radius:15px;
        backdrop-filter:blur(10px);
        text-align:center;
        font-size:14px;
        animation:fade 1s;
    '>
        📅 {current_day} | {current_date}
    </div>
    """, unsafe_allow_html=True)
    
# ---------- MISSIONS ----------
elif choice == "🎮 Missions":

    st.title("🎮 Missions")

    done=0
    total=0
    missed=[]
    completed=[]

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
    st.write(f"Score: {score}%")

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
        data["xp"]+=score

        data["reasons"][today_str]={
            "time":datetime.now().strftime("%H:%M"),
            "tasks":reasons_today
        }

        save(data)
        st.success(f"Successfully Saved +{score} Points 🔥")

# ---------- STATS ----------
elif choice == "📊 Stats":

    st.title("📊 Stats")

    history=data.get("history",{})

    if history:
        dates=list(history.keys())
        scores=list(history.values())

        st.plotly_chart(px.line(x=dates,y=scores,title="📈 Growth"))

        today_score = history.get(today_str,0)

        st.subheader("Daily Performance")
        st.plotly_chart(px.pie(
            values=[today_score,100-today_score],
            names=["Completed","Pending"]
        ))

# ---------- HISTORY ----------
elif choice == "📜 History":

    for d,s in data["history"].items():
        st.markdown(f"<div class='card'>{d} - Score: {s}</div>",unsafe_allow_html=True)

        if d in data["reasons"]:
            r=data["reasons"][d]
            st.write("Time:",r["time"])

            for t,rs in r["tasks"].items():
                st.write(f"{t} → {rs}")

# ---------- REPORT ----------
elif choice == "📄 Report":

    st.title("📄 📊 Daily Report 📈")

    if today_str in data["history"]:
        score=data["history"][today_str]
        reasons=data["reasons"].get(today_str,{})

        report=f"""
Name: {data['name']}
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
        st.download_button("Download Report",report,f"report_{today_str}.txt")

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    st.title("🧑 Profile")

    name=st.text_input("Name",value=data["name"])
    avatar=st.selectbox("Avatar",["😎","🔥","👑","💪"])
    dream=st.text_input("Dream",value=data.get("dream",""))

    st.markdown(f"### Preview: {avatar} {name}")

    if st.button("SAVE"):
        data["name"]=name
        data["avatar"]=avatar
        data["dream"]=dream
        save(data)
        st.success("Profile Saved ✅")

# ---------- SETTINGS ----------
elif choice == "⚙️ Settings":

    st.markdown("<div class='card'>⚙️ Settings Panel</div>", unsafe_allow_html=True)

    pwd = st.text_input("Enter Password", type="password")

    # ⚠️ CONFIRM CHECKBOX (NEW ADD)
    confirm = st.checkbox("⚠️ Are you sure you want to reset ALL data?")

    if st.button("RESET ALL DATA 💀"):

        if not confirm:
            st.warning("⚠️ Please confirm reset")
        
        elif pwd == "h1a2r3i4s5h6":

            # 🔥 FULL RESET DATA
            reset_data = {
                "points": 0,
                "xp": 0,
                "streak": 0,
                "last": "",
                "avatar": "😎",
                "name": "Player",
                "dream": "",
                "history": {},
                "reasons": {},
                "start_date": str(date.today())
            }

            # 💾 SAVE CLEAN FILE
            with open(DATA_FILE, "w") as f:
                json.dump(reset_data, f)

            # 🔥 CLEAR SESSION
            st.session_state.clear()

            st.success("💀 FULL RESET DONE")
            st.warning("🔄 Reloading App...")

            st.rerun()

        else:
            st.error("❌ Wrong Password")
            
