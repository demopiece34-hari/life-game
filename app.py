import streamlit as st
import json, os
from datetime import date
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Life Game ULTRA 🎯", layout="wide")

# ---------- SOUND ----------
st.markdown("""
<audio id="ding" src="https://www.soundjay.com/buttons/sounds/button-3.mp3"></audio>
<script>
function playSound(){
    document.getElementById("ding").play();
}
</script>
""", unsafe_allow_html=True)

# ---------- DATA ----------
DATA_FILE = "data.json"

def load():
    default = {
        "points": 0, "streak": 0, "last": "", "xp": 0,
        "avatar": "😎", "history": {}
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

# ---------- NAVIGATION ----------
menu = ["🏠 Dashboard","🎮 Missions","📊 Stats","🧑 Profile"]
choice = st.sidebar.radio("Navigation", menu)

# ---------- SIDEBAR ----------
level = data["xp"] // 100
st.sidebar.write(f"{data['avatar']} Level {level}")
st.sidebar.write(f"⚡ XP: {data['xp']}")
st.sidebar.write(f"💯 Points: {data['points']}")
st.sidebar.write(f"🔥 Streak: {data['streak']}")

# ---------- TASK GROUPS ----------
task_groups = {
    "Morning": ["Wake 5:30","Brush","Bath","Prayer","Washing"],
    "Learning": ["Reading","English","Python"],
    "Health": ["Water 2L","No Junk"],
    "Workout": ["Walking","Exercise","Kegel"],
    "Control": ["MA001","PN002"],
    "Entertainment": ["YouTube","Instagram","Movie"],
    "Weekend": ["Oil Bath"]
}

# ---------- DASHBOARD ----------
if choice == "🏠 Dashboard":
    st.title("🎯 LIFE GAME ULTRA")

    progress = data.get("last_score",0)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=progress,
        title={'text': "Today's Progress"},
        gauge={'axis': {'range':[0,100]}}
    ))
    st.plotly_chart(fig)

    st.success("🔥 Stay Consistent!")

# ---------- MISSIONS ----------
elif choice == "🎮 Missions":

    st.title("🎮 Daily Missions")

    done = 0
    total = 0

    for group, tasks in task_groups.items():
        with st.expander(group):
            for t in tasks:
                total += 1
                key = f"{today}_{t}"

                checked = st.checkbox(t, key=key)

                if checked:
                    st.markdown(f"✅ {t}")
                    st.markdown("<script>playSound()</script>", unsafe_allow_html=True)
                    done += 1

    score = int((done/total)*100)

    st.progress(score/100)
    st.write(f"🎯 Score: {score}")

    if st.button("💾 SAVE"):
        earn = done * 10
        data["xp"] += earn
        data["points"] += earn
        data["last"] = today
        data["last_score"] = score

        # history
        data["history"][today] = score

        save(data)
        st.success(f"🔥 +{earn} XP!")

# ---------- STATS ----------
elif choice == "📊 Stats":

    st.title("📊 Weekly Stats")

    history = data.get("history", {})

    if history:
        dates = list(history.keys())[-7:]
        scores = [history[d] for d in dates]

        fig = px.line(x=dates, y=scores, markers=True,
                      title="Last 7 Days Performance")

        st.plotly_chart(fig)
    else:
        st.info("No data yet")

# ---------- PROFILE ----------
elif choice == "🧑 Profile":

    st.title("🧑 Player Profile")

    avatars = ["😎","🔥","👑","💪","🤖"]

    selected = st.selectbox("Choose Avatar", avatars)

    if st.button("SAVE AVATAR"):
        data["avatar"] = selected
        save(data)
        st.success("Avatar Updated!")
