import streamlit as st
import json
import os
from datetime import date
import plotly.graph_objects as go

# ---------- CONFIG ----------
st.set_page_config(page_title="Life Game 🎯", layout="wide")

# ---------- CUSTOM CSS (GAMING UI) ----------
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}
.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #22c55e;
}
.card {
    padding: 15px;
    border-radius: 15px;
    background: #1e293b;
    box-shadow: 0px 0px 10px #22c55e;
}
</style>
""", unsafe_allow_html=True)

# ---------- FILE ----------
DATA_FILE = "data.json"

# ---------- LOAD ----------
def load():
    if not os.path.exists(DATA_FILE):
        return {"points": 0, "streak": 0, "last": "", "xp": 0}
    return json.load(open(DATA_FILE))

def save(d):
    json.dump(d, open(DATA_FILE, "w"))

data = load()

today = str(date.today())

# ---------- TASKS ----------
tasks = [
    "Wake 5:30","Brush","Bath","Prayer","Washing",
    "Reading","English","Python",
    "Water 2L","No Junk",
    "Walking","Exercise","Kegel",
    "MA001","PN002",
    "YouTube","Instagram","Movie",
    "Oil Bath"
]

# ---------- TITLE ----------
st.markdown('<div class="big-title">🎯 LIFE GAME PRO</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.header("🏆 PLAYER")

level = data["xp"] // 100
st.sidebar.write(f"🎮 Level: {level}")
st.sidebar.write(f"⚡ XP: {data['xp']}")
st.sidebar.write(f"💯 Points: {data['points']}")
st.sidebar.write(f"🔥 Streak: {data['streak']}")

# ---------- TASK UI ----------
st.subheader("🎮 Daily Missions")

cols = st.columns(3)

done = 0
status = {}

for i, t in enumerate(tasks):
    with cols[i % 3]:
        c = st.checkbox(t)
        status[t] = c
        if c:
            done += 1

total = len(tasks)
progress = done / total
score = int(progress * 100)

# ---------- CIRCULAR GRAPH ----------
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=score,
    title={'text': "Completion %"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "#22c55e"}
    }
))

st.plotly_chart(fig, use_container_width=True)

st.progress(progress)

# ---------- STATUS ----------
if score == 100:
    st.success("🚀 LEVEL UP! PERFECT DAY!")
elif score < 50:
    st.error("❌ GAME OVER!")

# ---------- SAVE ----------
if st.button("💾 SAVE PROGRESS"):

    if data["last"] != today:
        data["streak"] += 1
    data["last"] = today

    earn = done * 10
    data["points"] += earn
    data["xp"] += earn

    save(data)

    st.success(f"🔥 +{earn} XP Earned!")

# ---------- REWARDS ----------
st.subheader("🎁 Rewards")

if data["points"] >= 100:
    st.success("😴 Rest Day Unlocked")
if data["points"] >= 300:
    st.success("🎉 Fun Day Unlocked")
if data["points"] >= 500:
    st.success("📚 Skip Study Day")
if data["points"] >= 1000:
    st.success("🏖️ Full Relax Day")

# ---------- MOTIVATION ----------
st.subheader("💡 Motivation")

if score == 100:
    st.write("🔥 YOU ARE UNSTOPPABLE")
elif score > 70:
    st.write("💪 GREAT JOB")
else:
    st.write("⚡ TRY HARDER TOMORROW")
