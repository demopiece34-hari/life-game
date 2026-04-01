import streamlit as st
import json, os
from datetime import date, datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Life Game GOD MODE 😈", layout="wide")

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
        "badges": []
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

# ---------- UI ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}
.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:20px;
    backdrop-filter: blur(10px);
    margin-bottom:15px;
}
.card:hover { transform:scale(1.03); transition:0.3s;}
.stButton button {
    border-radius:15px;
    background: linear-gradient(45deg,#ff416c,#ff4b2b);
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","🧑 Profile"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- SIDEBAR ----------
level = data["xp"] // 100
xp_current = data["xp"] % 100

st.sidebar.markdown(f"# {data['avatar']} {data['name']}")
st.sidebar.write(f"🏆 Level: {level}")
st.sidebar.progress(xp_current/100)
st.sidebar.write(f"🔥 Streak: {data['streak']}")

# ---------- TASKS ----------
task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath"],
    "Learning": ["Reading","Python"],
    "Workout": ["Walking","Exercise"],
}

task_points = {"Wake 5:30":20,"Python":25,"Exercise":20}

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":

    st.title("🎯 LIFE GAME")

    st.markdown(f"""
    <h1 style='text-align:center; font-size:80px; animation: float 3s infinite;'>
    {data['avatar']}
    </h1>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    col1.markdown(f"<div class='card'>💯 {data['points']}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'>🔥 {data['streak']}</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'>⚡ {data['xp']}</div>", unsafe_allow_html=True)

# ---------- MISSIONS ----------
elif choice == "🎮 Missions":

    st.title("🎮 Missions")

    done=0
    total=0
    completed=[]

    for group,tasks in task_groups.items():
        st.subheader(group)
        cols = st.columns(3)

        for i,t in enumerate(tasks):
            total+=1
            key=f"{today}_{t}"
            if cols[i%3].checkbox(t,key=key):
                done+=1
                completed.append(t)

    score=int((done/total)*100)
    st.progress(score/100)
    st.write(score)

    if st.button("SAVE"):

        earn=sum(task_points.get(t,10) for t in completed)

        data["xp"]+=earn
        data["points"]+=earn
        data["history"][today]=score

        # streak
        last=data.get("last","")
        if last:
            last_date=datetime.strptime(last,"%Y-%m-%d").date()
            if date.today()==last_date+timedelta(days=1):
                data["streak"]+=1
            else:
                data["streak"]=1
        else:
            data["streak"]=1

        data["last"]=today
        save(data)

        st.success(f"+{earn} XP")

# ---------- STATS ----------
elif choice == "📊 Stats":

    history=data["history"]

    if history:
        dates=list(history.keys())[-7:]
        scores=[history[d] for d in dates]

        fig=px.area(x=dates,y=scores)
        st.plotly_chart(fig)

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    name=st.text_input("Name",value=data["name"])
    avatar=st.selectbox("Avatar",["😎","🔥","👑","💪"])

    if st.button("SAVE"):
        data["name"]=name
        data["avatar"]=avatar
        save(data)
        st.success("Saved")
