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

# ---------- UI STYLE + ANIMATION ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:#e2e8f0;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:#020617;
}

/* CARD */
.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:18px;
    backdrop-filter: blur(10px);
    border:1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    margin-bottom:15px;
    animation: fadeInUp 0.6s ease;
}

.card:hover {
    transform: translateY(-5px) scale(1.02);
    transition: 0.3s;
}

/* BUTTON */
.stButton button {
    border-radius:12px;
    background: linear-gradient(45deg,#6366f1,#8b5cf6);
    color:white;
    font-weight:600;
}

.stButton button:hover {
    transform: scale(1.05);
}

/* CHECKBOX */
.stCheckbox {
    background: rgba(255,255,255,0.03);
    padding:6px;
    border-radius:10px;
}

/* PROGRESS */
.stProgress > div > div {
    background: linear-gradient(90deg,#22c55e,#4ade80);
}

/* BADGE */
.badge {
    display:inline-block;
    padding:6px 12px;
    border-radius:20px;
    background:linear-gradient(45deg,#f59e0b,#ef4444);
    color:white;
    margin:5px;
    animation: popIn 0.4s ease;
}

/* ANIMATIONS */
@keyframes fadeInUp {
    from {opacity:0; transform: translateY(20px);}
    to {opacity:1; transform: translateY(0);}
}

@keyframes popIn {
    0% {transform: scale(0.5); opacity:0;}
    100% {transform: scale(1); opacity:1;}
}

@keyframes float {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-10px);}
    100% {transform: translateY(0px);}
}
</style>
""", unsafe_allow_html=True)

# ---------- NAV ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","🧑 Profile","⚙️ Settings"]
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
    "Entertainment": ["YouTube","Instagram","Movie"],
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

    # Avatar + Profile
    st.markdown(f"""
    <div class='card'>
        <h1 style='text-align:center; font-size:60px; animation: float 3s infinite;'>
        {data['avatar']}
        </h1>
        <h2 style='text-align:center;'>{data['name']}</h2>
        <p style='text-align:center;'>Level: {level}</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats Cards
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='card'>💯 Points<br><h2>{data['points']}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'>🔥 Streak<br><h2>{data['streak']}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'>⚡ XP<br><h2>{data['xp']}</h2></div>", unsafe_allow_html=True)

    # XP Progress
    st.markdown(f"""
    <div class='card'>
        Level Progress 🚀
        <progress value="{xp_current}" max="100" style="width:100%"></progress>
        <p>{xp_current}/100 XP</p>
    </div>
    """, unsafe_allow_html=True)

    # Chart
    history = data.get("history", {})
    if history:
        dates = list(history.keys())[-5:]
        scores = [history[d] for d in dates]

        fig = px.line(x=dates, y=scores, markers=True)
        fig.update_layout(template="plotly_dark", transition_duration=800)
        st.plotly_chart(fig, use_container_width=True)

# ---------- MISSIONS ----------
elif choice == "🎮 Missions":

    st.title("🎮 Daily Missions")

    done = 0
    total = 0
    completed_tasks = []

    for group, tasks in task_groups.items():
        st.markdown(f"### {group}")
        cols = st.columns(3)

        for i, t in enumerate(tasks):
            total += 1
            key = f"{today}_{t}"
            if cols[i % 3].checkbox(t, key=key):
                done += 1
                completed_tasks.append(t)

    score = int((done/total)*100)
    st.progress(score/100)
    st.write(f"🎯 Score: {score}")

    if score == 100:
        st.balloons()
        st.snow()

    if st.button("💾 SAVE"):

        earn = sum(task_points.get(t, 10) for t in completed_tasks)

        data["xp"] += earn
        data["points"] += earn
        data["history"][today] = score

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

        if score == 100 and "🏆 PERFECT DAY" not in data["badges"]:
            data["badges"].append("🏆 PERFECT DAY")

        save(data)
        st.success(f"🔥 +{earn} XP Saved!")

# ---------- STATS ----------
elif choice == "📊 Stats":

    st.title("📊 Weekly Stats")

    history = data.get("history", {})

    if history:
        dates = list(history.keys())[-7:]
        scores = [history[d] for d in dates]

        fig = px.area(x=dates, y=scores)
        fig.update_layout(template="plotly_dark", transition_duration=800)
        st.plotly_chart(fig, use_container_width=True)

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    st.title("🧑 Profile")

    name = st.text_input("Enter Name", value=data["name"])
    avatar = st.selectbox("Avatar", ["😎","🔥","👑","💪","🤖"])

    if st.button("SAVE PROFILE"):
        data["name"] = name
        data["avatar"] = avatar
        save(data)
        st.success("Updated!")

    st.subheader("🏆 Badges")

    for b in data["badges"]:
        st.markdown(f"<span class='badge'>{b}</span>", unsafe_allow_html=True)

# ---------- SETTINGS ----------
elif choice == "⚙️ Settings":

    st.title("⚙️ Settings")

    password = st.text_input("Enter Password", type="password")

    if st.button("RESET ALL DATA"):
        if password == "h1a2r3i4s5h6":
            save({
                "points":0,"streak":0,"last":"",
                "xp":0,"avatar":"😎","name":"Player",
                "history":{},"badges":[]
            })
            st.success("✅ RESET DONE")
        else:
            st.error("❌ Wrong Password")
