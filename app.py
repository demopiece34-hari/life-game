import streamlit as st
import json
import os
from datetime import date

# ---------- CONFIG ----------
st.set_page_config(page_title="Life Game 🎯", layout="wide")

# ---------- FILE ----------
DATA_FILE = "data.json"

# ---------- LOAD DATA ----------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "points": 0,
            "streak": 0,
            "last_date": "",
            "history": {}
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# ---------- TASK LIST ----------
tasks = [
    "Wake up 5:30", "Brush", "Bathing", "Prayer", "Washing",
    "Reading 1hr", "English 30min", "Python 30min",
    "Drink 2L Water", "No Junk Food",
    "Walking 1hr", "Exercise 30min", "Kegel 15min",
    "MA001", "PN002",
    "YouTube 20min", "Instagram 10min", "Movie (Weekly)",
    "Oil Bath"
]

today = str(date.today())

# ---------- UI TITLE ----------
st.title("🎯 Life Game Dashboard")
st.markdown("### 🔥 Level Up Your Life!")

# ---------- SIDEBAR ----------
st.sidebar.header("🏆 Player Stats")

st.sidebar.write(f"💯 Total Points: {data['points']}")
st.sidebar.write(f"🔥 Streak: {data['streak']} days")

# ---------- DAILY TASKS ----------
st.subheader("📋 Daily Missions")

completed = 0
total = len(tasks)

task_status = {}

cols = st.columns(3)

for i, task in enumerate(tasks):
    with cols[i % 3]:
        checked = st.checkbox(task, key=task)
        task_status[task] = checked
        if checked:
            completed += 1

# ---------- PROGRESS ----------
progress = completed / total
score = int(progress * 100)

st.subheader("🎮 Progress")

st.progress(progress)

st.markdown(f"### 🧿 Score: {score}/100")

# ---------- GAME STATUS ----------
if score == 100:
    st.success("🚀 LEVEL UP! Perfect Day!")
elif score < 50:
    st.error("❌ Game Over! Try Again!")

# ---------- SAVE BUTTON ----------
if st.button("💾 Save Progress"):
    
    # streak logic
    if data["last_date"] != today:
        if data["last_date"]:
            data["streak"] += 1
        else:
            data["streak"] = 1
    
    data["last_date"] = today

    # points
    earned = completed * 10
    data["points"] += earned

    # history
    data["history"][today] = {
        "score": score,
        "completed": completed
    }

    save_data(data)

    st.success(f"✅ Saved! You earned {earned} points!")

# ---------- REWARDS ----------
st.subheader("🎁 Rewards")

rewards = []

if data["points"] >= 100:
    rewards.append("😴 Rest Day (Skip Exercise)")
if data["points"] >= 300:
    rewards.append("🎉 Free Entertainment Day")
if data["points"] >= 500:
    rewards.append("📚 No Study Day")
if data["points"] >= 1000:
    rewards.append("🏖️ Full Relax Day")

if rewards:
    for r in rewards:
        st.success(r)
else:
    st.info("Keep grinding to unlock rewards 🔥")

# ---------- MOTIVATION ----------
st.subheader("💡 Motivation")

if score == 100:
    st.write("🔥 You are unstoppable!")
elif score > 70:
    st.write("💪 Great job, keep pushing!")
else:
    st.write("⚡ You can do better tomorrow!")

